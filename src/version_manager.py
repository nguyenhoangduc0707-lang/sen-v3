"""
SEN V3 — Version Manager
==========================
CRUD cho prompt_templates và llm_param_sets.
Đảm bảo nguyên tắc immutability: không bao giờ UPDATE nội dung,
chỉ tạo version mới và deprecate version cũ.

Dùng trong:
  - ParameterExplorerAgent: lưu kết quả Bayesian mỗi chu kỳ
  - PostHocAnalyzer: đọc lịch sử để rút ra ràng buộc mới
  - Admin Dashboard API: xem, so sánh, activate version
"""

import hashlib
import logging
from dataclasses import dataclass
from typing import Optional

import asyncpg

logger = logging.getLogger(__name__)


# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass
class PromptVersion:
    id:           str
    name:         str
    platform:     str
    version:      int
    content:      str
    variables:    list
    is_active:    bool
    created_at:   str
    notes:        Optional[str] = None


@dataclass
class ParamSetVersion:
    id:           str
    name:         str
    model:        str
    version:      int
    params:       dict
    score_avg:    Optional[float]
    sample_count: int
    is_active:    bool
    source:       str
    created_at:   str
    notes:        Optional[str] = None


@dataclass
class PerformanceSummary:
    id:              str
    name:            str
    version:         int
    is_active:       bool
    total_generated: int
    win_rate_pct:    Optional[float]
    avg_grader_score: Optional[float]
    avg_latency_ms:  Optional[float]


# ── Version Manager ───────────────────────────────────────────────────────────

class VersionManager:
    """
    Quản lý vòng đời prompt và param theo nguyên tắc:
      - Không bao giờ xoá hoặc sửa version đã tồn tại
      - Tạo version mới khi cần thay đổi
      - Chỉ 1 version được đánh dấu is_active tại một thời điểm
    """

    def __init__(self, db_pool: asyncpg.Pool):
        self._db = db_pool

    # ── PROMPT TEMPLATES ──────────────────────────────────────────────────────

    async def create_prompt_version(
        self,
        name:       str,
        platform:   str,
        content:    str,
        variables:  list  = None,
        notes:      str   = None,
        created_by: str   = "system",
        auto_activate: bool = False,
    ) -> PromptVersion:
        """
        Tạo phiên bản prompt mới.
        Tự động tăng version number dựa trên version cao nhất hiện có.
        Nếu content giống hệt version trước → raise ValueError (tránh duplicate).
        """
        variables = variables or []
        content_hash = _sha256(content)

        async with self._db.acquire() as conn:
            # Kiểm tra trùng nội dung
            existing = await conn.fetchrow(
                """
                SELECT id, version FROM prompt_templates
                WHERE name = $1 AND platform = $2 AND content_hash = $3
                """,
                name, platform, content_hash,
            )
            if existing:
                raise ValueError(
                    f"Prompt '{name}/{platform}' đã có version {existing['version']} "
                    "với nội dung giống hệt. Không tạo duplicate."
                )

            # Lấy version tiếp theo
            max_ver = await conn.fetchval(
                """
                SELECT COALESCE(MAX(version), 0)
                FROM prompt_templates
                WHERE name = $1 AND platform = $2
                """,
                name, platform,
            )
            new_version = max_ver + 1

            row = await conn.fetchrow(
                """
                INSERT INTO prompt_templates
                    (name, platform, version, content, content_hash, variables, notes, created_by)
                VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7, $8)
                RETURNING id::text, created_at::text
                """,
                name, platform, new_version, content, content_hash,
                _to_jsonb(variables), notes, created_by,
            )

            prompt = PromptVersion(
                id          = row["id"],
                name        = name,
                platform    = platform,
                version     = new_version,
                content     = content,
                variables   = variables,
                is_active   = False,
                created_at  = row["created_at"],
                notes       = notes,
            )

            if auto_activate:
                await self._activate_prompt(conn, prompt.id, name, platform)
                prompt.is_active = True

        logger.info(
            f"[VersionManager] Prompt '{name}/{platform}' v{new_version} tạo thành công."
        )
        return prompt

    async def activate_prompt(self, prompt_id: str) -> bool:
        """Đặt version này là active, tự động deactivate version cũ."""
        async with self._db.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT name, platform FROM prompt_templates WHERE id = $1",
                prompt_id,
            )
            if not row:
                return False
            await self._activate_prompt(conn, prompt_id, row["name"], row["platform"])
        logger.info(f"[VersionManager] Prompt {prompt_id} đã được activate.")
        return True

    async def get_active_prompt(self, name: str, platform: str) -> Optional[PromptVersion]:
        """Lấy prompt đang active cho (name, platform)."""
        async with self._db.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id::text, name, platform, version, content,
                       variables, is_active, created_at::text, notes
                FROM prompt_templates
                WHERE name = $1 AND platform = $2 AND is_active = TRUE
                """,
                name, platform,
            )
        if not row:
            return None
        return _row_to_prompt(row)

    async def list_prompt_versions(
        self, name: str, platform: str
    ) -> list[PromptVersion]:
        """Lấy toàn bộ lịch sử version của một prompt."""
        async with self._db.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id::text, name, platform, version, content,
                       variables, is_active, created_at::text, notes
                FROM prompt_templates
                WHERE name = $1 AND platform = $2
                ORDER BY version DESC
                """,
                name, platform,
            )
        return [_row_to_prompt(r) for r in rows]

    async def get_prompt_performance(
        self, name: str, platform: str
    ) -> list[PerformanceSummary]:
        """Đọc view prompt_performance — dùng cho Dashboard."""
        async with self._db.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT prompt_id::text AS id, name, version, is_active,
                       total_generated, win_rate_pct, avg_grader_score, avg_latency_ms
                FROM prompt_performance
                WHERE name = $1 AND platform = $2
                """,
                name, platform,
            )
        return [
            PerformanceSummary(
                id               = r["id"],
                name             = r["name"],
                version          = r["version"],
                is_active        = r["is_active"],
                total_generated  = r["total_generated"] or 0,
                win_rate_pct     = float(r["win_rate_pct"]) if r["win_rate_pct"] else None,
                avg_grader_score = float(r["avg_grader_score"]) if r["avg_grader_score"] else None,
                avg_latency_ms   = float(r["avg_latency_ms"]) if r["avg_latency_ms"] else None,
            )
            for r in rows
        ]

    # ── LLM PARAM SETS ────────────────────────────────────────────────────────

    async def save_param_version(
        self,
        name:         str,
        model:        str,
        params:       dict,
        score_avg:    Optional[float] = None,
        score_min:    Optional[float] = None,
        score_max:    Optional[float] = None,
        sample_count: int             = 0,
        source:       str             = "bayesian",
        notes:        str             = None,
        auto_activate: bool           = False,
    ) -> ParamSetVersion:
        """
        Lưu kết quả một chu kỳ Bayesian Optimization.
        Gọi bởi ParameterExplorerAgent sau mỗi vòng đánh giá.
        """
        async with self._db.acquire() as conn:
            max_ver = await conn.fetchval(
                """
                SELECT COALESCE(MAX(version), 0)
                FROM llm_param_sets
                WHERE name = $1 AND model = $2
                """,
                name, model,
            )
            new_version = max_ver + 1

            row = await conn.fetchrow(
                """
                INSERT INTO llm_param_sets
                    (name, model, version, params, score_avg, score_min, score_max,
                     sample_count, source, notes)
                VALUES ($1, $2, $3, $4::jsonb, $5, $6, $7, $8, $9, $10)
                RETURNING id::text, created_at::text
                """,
                name, model, new_version,
                _to_jsonb(params),
                score_avg, score_min, score_max,
                sample_count, source, notes,
            )

            ps = ParamSetVersion(
                id           = row["id"],
                name         = name,
                model        = model,
                version      = new_version,
                params       = params,
                score_avg    = score_avg,
                sample_count = sample_count,
                is_active    = False,
                source       = source,
                created_at   = row["created_at"],
                notes        = notes,
            )

            if auto_activate:
                await self._activate_params(conn, ps.id, name, model)
                ps.is_active = True

        logger.info(
            f"[VersionManager] Params '{name}/{model}' v{new_version} "
            f"score={score_avg} lưu thành công."
        )
        return ps

    async def get_active_params(
        self, name: str, model: str
    ) -> Optional[ParamSetVersion]:
        """Lấy bộ tham số đang active cho (name, model)."""
        async with self._db.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id::text, name, model, version, params,
                       score_avg, sample_count, is_active, source,
                       created_at::text, notes
                FROM llm_param_sets
                WHERE name = $1 AND model = $2 AND is_active = TRUE
                """,
                name, model,
            )
        if not row:
            return None
        return _row_to_params(row)

    async def get_best_params(self, model: str) -> Optional[ParamSetVersion]:
        """
        Lấy bộ tham số có score_avg cao nhất cho model.
        PostHocAnalyzer dùng để so sánh với chu kỳ mới nhất.
        """
        async with self._db.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id::text, name, model, version, params,
                       score_avg, sample_count, is_active, source,
                       created_at::text, notes
                FROM llm_param_sets
                WHERE model = $1 AND score_avg IS NOT NULL
                ORDER BY score_avg DESC
                LIMIT 1
                """,
                model,
            )
        if not row:
            return None
        return _row_to_params(row)

    async def list_param_versions(
        self, name: str, model: str
    ) -> list[ParamSetVersion]:
        """Lịch sử toàn bộ param versions — dùng để so sánh chu kỳ Bayesian."""
        async with self._db.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT id::text, name, model, version, params,
                       score_avg, sample_count, is_active, source,
                       created_at::text, notes
                FROM llm_param_sets
                WHERE name = $1 AND model = $2
                ORDER BY version DESC
                """,
                name, model,
            )
        return [_row_to_params(r) for r in rows]

    # ── CONTENT VERSIONS ──────────────────────────────────────────────────────

    async def save_content_version(
        self,
        task_id:      str,
        content:      str,
        model_used:   str,
        prompt_id:    Optional[str] = None,
        param_set_id: Optional[str] = None,
        is_fallback:  bool          = False,
        latency_ms:   Optional[int] = None,
    ) -> str:
        """
        Lưu nội dung vừa sinh bởi LLM.
        Trả về content_version_id để Grader/Comparator cập nhật score sau.
        """
        content_hash = _sha256(content)

        async with self._db.acquire() as conn:
            cv_id = await conn.fetchval(
                """
                INSERT INTO content_versions
                    (task_id, prompt_id, param_set_id, model_used,
                     content, content_hash, is_fallback, latency_ms)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id::text
                """,
                task_id, prompt_id, param_set_id, model_used,
                content, content_hash, is_fallback, latency_ms,
            )
        return cv_id

    async def update_grader_score(self, content_version_id: str, score: float):
        """Grader gọi sau khi chấm điểm."""
        async with self._db.acquire() as conn:
            await conn.execute(
                "UPDATE content_versions SET grader_score = $1 WHERE id = $2",
                score, content_version_id,
            )

    async def mark_winner(self, content_version_id: str, rank: int = 1):
        """BlindComparator gọi để đánh dấu version thắng."""
        async with self._db.acquire() as conn:
            await conn.execute(
                """
                UPDATE content_versions
                SET is_winner = TRUE, comparator_rank = $1
                WHERE id = $2
                """,
                rank, content_version_id,
            )

    # ── Private helpers ───────────────────────────────────────────────────────

    @staticmethod
    async def _activate_prompt(
        conn: asyncpg.Connection, prompt_id: str, name: str, platform: str
    ):
        await conn.execute(
            """
            UPDATE prompt_templates
            SET is_active = FALSE
            WHERE name = $1 AND platform = $2 AND is_active = TRUE
            """,
            name, platform,
        )
        await conn.execute(
            "UPDATE prompt_templates SET is_active = TRUE WHERE id = $1",
            prompt_id,
        )

    @staticmethod
    async def _activate_params(
        conn: asyncpg.Connection, param_id: str, name: str, model: str
    ):
        await conn.execute(
            """
            UPDATE llm_param_sets
            SET is_active = FALSE
            WHERE name = $1 AND model = $2 AND is_active = TRUE
            """,
            name, model,
        )
        await conn.execute(
            "UPDATE llm_param_sets SET is_active = TRUE WHERE id = $1",
            param_id,
        )


# ── Helpers ───────────────────────────────────────────────────────────────────

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def _to_jsonb(obj) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False)

def _row_to_prompt(row) -> PromptVersion:
    import json
    return PromptVersion(
        id         = row["id"],
        name       = row["name"],
        platform   = row["platform"],
        version    = row["version"],
        content    = row["content"],
        variables  = json.loads(row["variables"]) if isinstance(row["variables"], str) else row["variables"],
        is_active  = row["is_active"],
        created_at = row["created_at"],
        notes      = row.get("notes"),
    )

def _row_to_params(row) -> ParamSetVersion:
    import json
    return ParamSetVersion(
        id           = row["id"],
        name         = row["name"],
        model        = row["model"],
        version      = row["version"],
        params       = json.loads(row["params"]) if isinstance(row["params"], str) else dict(row["params"]),
        score_avg    = float(row["score_avg"]) if row["score_avg"] else None,
        sample_count = row["sample_count"],
        is_active    = row["is_active"],
        source       = row["source"],
        created_at   = row["created_at"],
        notes        = row.get("notes"),
    )
