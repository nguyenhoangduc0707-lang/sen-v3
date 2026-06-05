"""
SEN V3 — Versioning API (FastAPI)
===================================
Endpoints cho Admin Dashboard quản lý prompt và param versions.

Mount vào FastAPI app chính:
    from versioning_api import router as versioning_router
    app.include_router(versioning_router, prefix="/api/v1/versions")
"""

import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from version_manager import VersionManager

router = APIRouter(tags=["versioning"])

# ── Dependency: DB pool ───────────────────────────────────────────────────────
# Thay bằng dependency injection thực tế của project

async def get_vm() -> VersionManager:
    pool = await asyncpg.create_pool("postgresql://sen:changeme@localhost/sen_v3")
    return VersionManager(pool)


# ── Request models ────────────────────────────────────────────────────────────

class CreatePromptRequest(BaseModel):
    name:          str
    platform:      str
    content:       str
    variables:     list[str] = []
    notes:         Optional[str] = None
    auto_activate: bool = False

class ActivateRequest(BaseModel):
    id: str

class SaveParamRequest(BaseModel):
    name:          str
    model:         str
    params:        dict
    score_avg:     Optional[float] = None
    score_min:     Optional[float] = None
    score_max:     Optional[float] = None
    sample_count:  int = 0
    source:        str = "bayesian"
    notes:         Optional[str] = None
    auto_activate: bool = False


# ── Prompt endpoints ──────────────────────────────────────────────────────────

@router.post("/prompts")
async def create_prompt(
    req: CreatePromptRequest,
    vm:  VersionManager = Depends(get_vm),
):
    """Tạo prompt version mới."""
    try:
        prompt = await vm.create_prompt_version(
            name          = req.name,
            platform      = req.platform,
            content       = req.content,
            variables     = req.variables,
            notes         = req.notes,
            auto_activate = req.auto_activate,
        )
        return {"ok": True, "data": prompt}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/prompts/{name}/{platform}")
async def list_prompts(
    name:     str,
    platform: str,
    vm:       VersionManager = Depends(get_vm),
):
    """Lịch sử toàn bộ version của một prompt."""
    versions = await vm.list_prompt_versions(name, platform)
    return {"ok": True, "data": versions}


@router.get("/prompts/{name}/{platform}/active")
async def get_active_prompt(
    name:     str,
    platform: str,
    vm:       VersionManager = Depends(get_vm),
):
    """Lấy prompt đang active."""
    prompt = await vm.get_active_prompt(name, platform)
    if not prompt:
        raise HTTPException(status_code=404, detail="Không có prompt active.")
    return {"ok": True, "data": prompt}


@router.get("/prompts/{name}/{platform}/performance")
async def prompt_performance(
    name:     str,
    platform: str,
    vm:       VersionManager = Depends(get_vm),
):
    """
    Hiệu quả từng version: win_rate, grader_score, latency.
    Dùng để chọn version tốt nhất và deprecate phần còn lại.
    """
    data = await vm.get_prompt_performance(name, platform)
    return {"ok": True, "data": data}


@router.post("/prompts/activate")
async def activate_prompt(
    req: ActivateRequest,
    vm:  VersionManager = Depends(get_vm),
):
    """Activate một prompt version cụ thể (deactivate version cũ tự động)."""
    ok = await vm.activate_prompt(req.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Prompt ID không tồn tại.")
    return {"ok": True, "message": f"Prompt {req.id} đã được activate."}


# ── Param endpoints ───────────────────────────────────────────────────────────

@router.post("/params")
async def save_params(
    req: SaveParamRequest,
    vm:  VersionManager = Depends(get_vm),
):
    """
    Lưu kết quả một chu kỳ Bayesian Optimization.
    ParameterExplorerAgent gọi endpoint này sau mỗi vòng.
    """
    ps = await vm.save_param_version(
        name          = req.name,
        model         = req.model,
        params        = req.params,
        score_avg     = req.score_avg,
        score_min     = req.score_min,
        score_max     = req.score_max,
        sample_count  = req.sample_count,
        source        = req.source,
        notes         = req.notes,
        auto_activate = req.auto_activate,
    )
    return {"ok": True, "data": ps}


@router.get("/params/{name}/{model}")
async def list_params(
    name:  str,
    model: str,
    vm:    VersionManager = Depends(get_vm),
):
    """Lịch sử toàn bộ param versions — so sánh chu kỳ Bayesian."""
    versions = await vm.list_param_versions(name, model)
    return {"ok": True, "data": versions}


@router.get("/params/{name}/{model}/active")
async def get_active_params(
    name:  str,
    model: str,
    vm:    VersionManager = Depends(get_vm),
):
    """Bộ tham số đang active cho (name, model)."""
    ps = await vm.get_active_params(name, model)
    if not ps:
        raise HTTPException(status_code=404, detail="Không có param set active.")
    return {"ok": True, "data": ps}


@router.get("/params/best/{model}")
async def best_params(
    model: str,
    vm:    VersionManager = Depends(get_vm),
):
    """Bộ tham số có score cao nhất — PostHocAnalyzer dùng làm baseline."""
    ps = await vm.get_best_params(model)
    if not ps:
        raise HTTPException(status_code=404, detail="Chưa có dữ liệu score.")
    return {"ok": True, "data": ps}


# ── Compare endpoint ──────────────────────────────────────────────────────────

@router.get("/compare/params/{model}")
async def compare_param_cycles(
    model:     str,
    last_n:    int = Query(5, ge=2, le=20),
    vm:        VersionManager = Depends(get_vm),
):
    """
    So sánh N chu kỳ Bayesian gần nhất của một model.
    Trả về dữ liệu để vẽ biểu đồ tiến hóa score trên Dashboard.
    """
    # Lấy tất cả param sets có score, nhóm theo name, lấy last_n version/name
    import asyncpg as apg
    pool = await apg.create_pool("postgresql://sen:changeme@localhost/sen_v3")
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT name, version, score_avg, score_min, score_max,
                   sample_count, source, created_at::text,
                   params->>'temperature' AS temperature,
                   params->>'top_p'       AS top_p
            FROM llm_param_sets
            WHERE model = $1 AND score_avg IS NOT NULL
            ORDER BY name, version DESC
            LIMIT $2
            """,
            model, last_n * 5,
        )

    data = [
        {
            "name":        r["name"],
            "version":     r["version"],
            "score_avg":   float(r["score_avg"]),
            "score_min":   float(r["score_min"]) if r["score_min"] else None,
            "score_max":   float(r["score_max"]) if r["score_max"] else None,
            "sample_count":r["sample_count"],
            "source":      r["source"],
            "temperature": float(r["temperature"]) if r["temperature"] else None,
            "top_p":       float(r["top_p"]) if r["top_p"] else None,
            "created_at":  r["created_at"],
        }
        for r in rows
    ]
    return {"ok": True, "model": model, "data": data}
