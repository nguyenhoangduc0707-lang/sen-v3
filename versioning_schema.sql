-- SEN V3 — Data Versioning Schema
-- ===================================
-- Phiên bản hóa toàn bộ prompt và bộ tham số LLM.
-- Cho phép truy vết, so sánh, và rollback giữa các chu kỳ Bayesian.
--
-- Chạy: psql -U sen -d sen_v3 -f versioning_schema.sql

-- ── Extensions ────────────────────────────────────────────────────────────────

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- dùng cho content hash

-- ── Bảng 1: prompt_templates ──────────────────────────────────────────────────
-- Lưu nội dung prompt theo phiên bản.
-- Mỗi lần chỉnh sửa prompt → tạo version mới, KHÔNG update version cũ.

CREATE TABLE IF NOT EXISTS prompt_templates (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            TEXT        NOT NULL,               -- vd: "product_review_vi"
    platform        TEXT        NOT NULL,               -- tiktok | shopee | accesstrade
    version         INTEGER     NOT NULL DEFAULT 1,
    content         TEXT        NOT NULL,               -- nội dung prompt
    content_hash    TEXT        NOT NULL,               -- SHA256 để detect trùng
    variables       JSONB       NOT NULL DEFAULT '[]',  -- ["product_name", "price"]
    is_active       BOOLEAN     NOT NULL DEFAULT FALSE, -- chỉ 1 version active/name/platform
    created_by      TEXT        NOT NULL DEFAULT 'system',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deprecated_at   TIMESTAMPTZ,
    notes           TEXT,                               -- ghi chú thay đổi

    UNIQUE (name, platform, version)
);

-- Đảm bảo chỉ 1 version active cho mỗi (name, platform)
CREATE UNIQUE INDEX IF NOT EXISTS idx_prompt_one_active
    ON prompt_templates (name, platform)
    WHERE is_active = TRUE;

CREATE INDEX IF NOT EXISTS idx_prompt_name_platform
    ON prompt_templates (name, platform, version DESC);

COMMENT ON TABLE prompt_templates IS
    'Lịch sử toàn bộ phiên bản prompt. Không xoá, chỉ deprecate.';


-- ── Bảng 2: llm_param_sets ────────────────────────────────────────────────────
-- Lưu bộ tham số LLM (temperature, top_p, ...) theo phiên bản.
-- ParameterExplorerAgent ghi kết quả Bayesian vào đây.

CREATE TABLE IF NOT EXISTS llm_param_sets (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            TEXT        NOT NULL,               -- vd: "bayesian_cycle_7"
    model           TEXT        NOT NULL,               -- gemini-flash | gpt-4o
    version         INTEGER     NOT NULL DEFAULT 1,
    params          JSONB       NOT NULL,               -- {"temperature": 0.7, "top_p": 0.9}
    score_avg       NUMERIC(5,4),                       -- điểm trung bình từ BlindComparator
    score_min       NUMERIC(5,4),
    score_max       NUMERIC(5,4),
    sample_count    INTEGER     NOT NULL DEFAULT 0,     -- số lần đánh giá
    is_active       BOOLEAN     NOT NULL DEFAULT FALSE,
    source          TEXT        NOT NULL DEFAULT 'manual', -- manual | bayesian | posthoc
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    notes           TEXT,

    UNIQUE (name, model, version)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_params_one_active
    ON llm_param_sets (name, model)
    WHERE is_active = TRUE;

CREATE INDEX IF NOT EXISTS idx_params_score
    ON llm_param_sets (model, score_avg DESC NULLS LAST);

COMMENT ON TABLE llm_param_sets IS
    'Lịch sử bộ tham số LLM. ParameterExplorerAgent ghi sau mỗi chu kỳ Bayesian.';


-- ── Bảng 3: content_versions ──────────────────────────────────────────────────
-- Lưu từng phiên bản nội dung được sinh ra.
-- Liên kết với prompt và param để truy vết đầy đủ.

CREATE TABLE IF NOT EXISTS content_versions (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id         UUID        NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    prompt_id       UUID        REFERENCES prompt_templates(id),
    param_set_id    UUID        REFERENCES llm_param_sets(id),
    model_used      TEXT        NOT NULL,
    content         TEXT        NOT NULL,
    content_hash    TEXT        NOT NULL,               -- detect nội dung trùng
    word_count      INTEGER     GENERATED ALWAYS AS (
                        array_length(string_to_array(trim(content), ' '), 1)
                    ) STORED,
    grader_score    NUMERIC(5,4),                       -- kết quả từ Grader
    comparator_rank INTEGER,                            -- xếp hạng từ BlindComparator
    is_winner       BOOLEAN     NOT NULL DEFAULT FALSE, -- phiên bản thắng A/B test
    is_fallback     BOOLEAN     NOT NULL DEFAULT FALSE, -- dùng model fallback
    latency_ms      INTEGER,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_content_task    ON content_versions (task_id);
CREATE INDEX IF NOT EXISTS idx_content_winner  ON content_versions (is_winner, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_content_prompt  ON content_versions (prompt_id);

COMMENT ON TABLE content_versions IS
    'Mỗi lần LLM sinh nội dung → 1 bản ghi. Liên kết đầy đủ prompt + param.';


-- ── Bảng 4: version_comparisons ───────────────────────────────────────────────
-- Kết quả so sánh A/B từ BlindComparator.

CREATE TABLE IF NOT EXISTS version_comparisons (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id         UUID        NOT NULL REFERENCES tasks(id),
    winner_id       UUID        NOT NULL REFERENCES content_versions(id),
    loser_id        UUID        NOT NULL REFERENCES content_versions(id),
    rubric_used     TEXT        NOT NULL DEFAULT 'rubric_affiliate.json',
    score_diff      NUMERIC(5,4),                       -- winner_score - loser_score
    reasoning       TEXT,                               -- giải thích của LLM judge
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_comparison_task ON version_comparisons (task_id);


-- ── View: prompt_performance ───────────────────────────────────────────────────
-- Tổng hợp hiệu quả của từng prompt version → dùng trong Dashboard.

CREATE OR REPLACE VIEW prompt_performance AS
SELECT
    pt.id           AS prompt_id,
    pt.name,
    pt.platform,
    pt.version,
    pt.is_active,
    pt.created_at,
    COUNT(cv.id)            AS total_generated,
    COUNT(cv.id) FILTER (WHERE cv.is_winner)    AS total_wins,
    ROUND(
        COUNT(cv.id) FILTER (WHERE cv.is_winner)::NUMERIC
        / NULLIF(COUNT(cv.id), 0) * 100, 2
    )                       AS win_rate_pct,
    ROUND(AVG(cv.grader_score)::NUMERIC, 4)     AS avg_grader_score,
    ROUND(AVG(cv.latency_ms)::NUMERIC, 0)       AS avg_latency_ms
FROM prompt_templates pt
LEFT JOIN content_versions cv ON cv.prompt_id = pt.id
GROUP BY pt.id, pt.name, pt.platform, pt.version, pt.is_active, pt.created_at
ORDER BY pt.name, pt.platform, pt.version DESC;

COMMENT ON VIEW prompt_performance IS
    'Hiệu quả từng prompt version: win_rate, grader_score, latency.';


-- ── View: param_performance ───────────────────────────────────────────────────
-- So sánh hiệu quả các bộ tham số LLM qua các chu kỳ Bayesian.

CREATE OR REPLACE VIEW param_performance AS
SELECT
    ps.id           AS param_set_id,
    ps.name,
    ps.model,
    ps.version,
    ps.is_active,
    ps.params,
    ps.score_avg,
    ps.sample_count,
    ps.source,
    ps.created_at,
    COUNT(cv.id)    AS contents_generated,
    ROUND(AVG(cv.grader_score)::NUMERIC, 4)     AS actual_grader_avg,
    COUNT(cv.id) FILTER (WHERE cv.is_winner)    AS wins
FROM llm_param_sets ps
LEFT JOIN content_versions cv ON cv.param_set_id = ps.id
GROUP BY ps.id, ps.name, ps.model, ps.version,
         ps.is_active, ps.params, ps.score_avg, ps.sample_count,
         ps.source, ps.created_at
ORDER BY ps.model, ps.score_avg DESC NULLS LAST;

COMMENT ON VIEW param_performance IS
    'So sánh hiệu quả các bộ param qua các chu kỳ Bayesian.';
