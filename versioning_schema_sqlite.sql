-- ============================================
-- Data Versioning Schema for SQLite
-- B?ng l?u l?ch s? prompt templates
-- ============================================

-- 1. Prompt Templates table
CREATE TABLE IF NOT EXISTS prompt_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    system_prompt TEXT NOT NULL,
    user_prompt TEXT NOT NULL,
    is_active INTEGER DEFAULT 0,
    created_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activated_at TIMESTAMP,
    UNIQUE(name, version)
);

-- Index for active prompt
CREATE INDEX IF NOT EXISTS idx_prompt_active ON prompt_templates(is_active);

-- 2. LLM Parameter Sets table (Bayesian optimization cycles)
CREATE TABLE IF NOT EXISTS llm_param_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    cycle INTEGER NOT NULL,
    temperature REAL,
    top_p REAL,
    top_k INTEGER,
    max_tokens INTEGER,
    frequency_penalty REAL,
    presence_penalty REAL,
    score_avg REAL,
    score_min REAL,
    score_max REAL,
    tested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_params_model_cycle ON llm_param_sets(model, cycle);

-- 3. Content Versions table (m?i l?n LLM sinh content)
CREATE TABLE IF NOT EXISTS content_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER NOT NULL,
    param_set_id INTEGER,
    content TEXT NOT NULL,
    score REAL,
    grader_feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prompt_id) REFERENCES prompt_templates(id),
    FOREIGN KEY (param_set_id) REFERENCES llm_param_sets(id)
);

CREATE INDEX IF NOT EXISTS idx_content_prompt ON content_versions(prompt_id);
CREATE INDEX IF NOT EXISTS idx_content_score ON content_versions(score);

-- 4. Version Comparisons table (A/B testing results)
CREATE TABLE IF NOT EXISTS version_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    variant_a_id INTEGER NOT NULL,
    variant_b_id INTEGER NOT NULL,
    winner_id INTEGER,
    score_a REAL,
    score_b REAL,
    difference REAL,
    significant INTEGER DEFAULT 0,
    compared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variant_a_id) REFERENCES content_versions(id),
    FOREIGN KEY (variant_b_id) REFERENCES content_versions(id)
);

-- ============================================
-- VIEWS for Dashboard
-- ============================================

-- Prompt performance view
CREATE VIEW IF NOT EXISTS prompt_performance AS
SELECT 
    p.id,
    p.name,
    p.version,
    p.is_active,
    COUNT(c.id) as total_generations,
    AVG(c.score) as avg_score,
    MAX(c.score) as max_score,
    MIN(c.score) as min_score,
    p.created_at
FROM prompt_templates p
LEFT JOIN content_versions c ON p.id = c.prompt_id
GROUP BY p.id, p.name, p.version, p.is_active, p.created_at;

-- Parameter performance view
CREATE VIEW IF NOT EXISTS param_performance AS
SELECT 
    model,
    cycle,
    AVG(score_avg) as avg_cycle_score,
    COUNT(*) as test_count,
    MAX(score_avg) as best_score
FROM llm_param_sets
GROUP BY model, cycle;

-- ============================================
-- Triggers for auto versioning
-- ============================================

-- Trigger to deactivate old prompt when new one activated
CREATE TRIGGER IF NOT EXISTS trigger_deactivate_old_prompt
AFTER UPDATE OF is_active ON prompt_templates
WHEN NEW.is_active = 1
BEGIN
    UPDATE prompt_templates 
    SET is_active = 0 
    WHERE id != NEW.id AND is_active = 1;
END;

-- ============================================
-- Sample data
-- ============================================

-- Insert default prompt
INSERT OR IGNORE INTO prompt_templates (name, version, system_prompt, user_prompt, is_active, created_by)
VALUES ('default_v1', 1, 
'You are a helpful marketing assistant for SEN V3 platform.',
'Generate engaging content for: {topic}',
1, 'system');

-- Insert default param set
INSERT OR IGNORE INTO llm_param_sets (model, cycle, temperature, top_p, top_k, max_tokens, score_avg)
VALUES ('gemini-1.5-flash', 1, 0.7, 0.9, 40, 2048, 0.0);

SELECT '? Versioning schema created successfully!' as status;
