"""
SEN V3 — Ví dụ tích hợp VersionManager
=========================================
Minh họa cách ParameterExplorerAgent và ContentCreationAgent
sử dụng VersionManager để lưu và đọc versions.
"""

import asyncio
import asyncpg
from version_manager import VersionManager


async def demo():
    pool = await asyncpg.create_pool("postgresql://sen:changeme@localhost/sen_v3")
    vm   = VersionManager(pool)

    # ── 1. Tạo prompt version đầu tiên ───────────────────────────────────────
    print("=== Tạo prompt v1 ===")
    p1 = await vm.create_prompt_version(
        name          = "product_review_vi",
        platform      = "tiktok",
        content       = (
            "Viết review sản phẩm {product_name} giá {price}VND "
            "theo phong cách TikTok ngắn gọn, hấp dẫn. "
            "Độ dài 150-200 từ. Kết thúc bằng call-to-action và affiliate link."
        ),
        variables     = ["product_name", "price"],
        notes         = "Prompt khởi tạo ban đầu",
        auto_activate = True,
    )
    print(f"  → Prompt {p1.name} v{p1.version} | active={p1.is_active}")

    # ── 2. Cập nhật prompt (tạo v2) ───────────────────────────────────────────
    print("\n=== Cập nhật prompt v2 ===")
    p2 = await vm.create_prompt_version(
        name          = "product_review_vi",
        platform      = "tiktok",
        content       = (
            "Với vai trò KOL TikTok, viết review {product_name} (giá {price}VND). "
            "Mở đầu bằng hook gây tò mò. Nêu 3 ưu điểm nổi bật. "
            "Độ dài 180-220 từ. Kết bằng CTA mạnh và link affiliate."
        ),
        variables     = ["product_name", "price"],
        notes         = "Thêm hook và cấu trúc 3 ưu điểm — thử nghiệm chu kỳ 2",
        auto_activate = True,   # tự động deactivate v1
    )
    print(f"  → Prompt {p2.name} v{p2.version} | active={p2.is_active}")

    # ── 3. Xem lịch sử ────────────────────────────────────────────────────────
    print("\n=== Lịch sử prompt versions ===")
    history = await vm.list_prompt_versions("product_review_vi", "tiktok")
    for h in history:
        active_mark = "✓ ACTIVE" if h.is_active else "  archived"
        print(f"  v{h.version} [{active_mark}] — {h.notes}")

    # ── 4. ParameterExplorerAgent lưu kết quả Bayesian ────────────────────────
    print("\n=== ParameterExplorerAgent: lưu chu kỳ Bayesian 1 ===")
    ps1 = await vm.save_param_version(
        name          = "bayesian_tiktok",
        model         = "gemini-flash",
        params        = {"temperature": 0.8, "top_p": 0.9, "max_tokens": 512},
        score_avg     = 0.72,
        score_min     = 0.65,
        score_max     = 0.81,
        sample_count  = 20,
        source        = "bayesian",
        notes         = "Chu kỳ 1 — khởi tạo ngẫu nhiên",
        auto_activate = True,
    )
    print(f"  → Params v{ps1.version} | score_avg={ps1.score_avg}")

    print("\n=== ParameterExplorerAgent: lưu chu kỳ Bayesian 2 (tốt hơn) ===")
    ps2 = await vm.save_param_version(
        name          = "bayesian_tiktok",
        model         = "gemini-flash",
        params        = {"temperature": 0.65, "top_p": 0.85, "max_tokens": 512},
        score_avg     = 0.79,
        score_min     = 0.71,
        score_max     = 0.88,
        sample_count  = 20,
        source        = "bayesian",
        notes         = "Chu kỳ 2 — Bayesian hội tụ về temperature thấp hơn",
        auto_activate = True,   # tốt hơn → activate
    )
    print(f"  → Params v{ps2.version} | score_avg={ps2.score_avg}")

    # ── 5. PostHocAnalyzer đọc best params ────────────────────────────────────
    print("\n=== PostHocAnalyzer: lấy best params làm baseline ===")
    best = await vm.get_best_params("gemini-flash")
    print(f"  → Best: v{best.version} | score={best.score_avg} | params={best.params}")

    # ── 6. ContentCreationAgent lưu nội dung với truy vết đầy đủ ─────────────
    print("\n=== ContentCreationAgent: lưu content version ===")
    task_id  = "00000000-0000-0000-0000-000000000001"  # UUID giả cho demo
    cv_id = await vm.save_content_version(
        task_id      = task_id,
        content      = "Review Airpods Pro 2: Âm thanh cực đỉnh, chống ồn siêu tốt...",
        model_used   = "gemini-flash",
        prompt_id    = p2.id,
        param_set_id = ps2.id,
        latency_ms   = 1240,
    )
    print(f"  → ContentVersion ID: {cv_id}")

    # Grader chấm điểm
    await vm.update_grader_score(cv_id, score=0.84)
    print("  → Grader score: 0.84 ✓")

    # BlindComparator chọn winner
    await vm.mark_winner(cv_id, rank=1)
    print("  → Đánh dấu is_winner=True ✓")

    print("\n✅ Demo hoàn thành — toàn bộ chuỗi có thể truy vết trong PostgreSQL.")
    await pool.close()


if __name__ == "__main__":
    asyncio.run(demo())
