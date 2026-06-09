"""
Optimizer module - Tối ưu hóa tỉ lệ chuyển đổi (conversion rate) dựa trên data nội bộ.

Mục tiêu: Sau khi có data (tasks đã hoàn thành), hệ thống PHẢI biết cách chọn giờ đăng tốt nhất
cho từng fanpage/theme để tối ưu engagement / conversion (proxy = số task COMPLETED thành công).

Sử dụng data nội bộ từ Task queue:
- status = COMPLETED → coi là "thành công" (proxy cho conversion cao).
- Phân tích theo fanpage_key, theme, giờ trong ngày.
- Trả về top giờ tốt nhất để schedule.

Cách dùng:
from src.optimizer import PostingOptimizer
opt = PostingOptimizer()
best_hours = opt.get_best_posting_hours(fanpage_key="ai_tech", theme="ai_tech", top_n=5, days_back=30)

Nếu chưa có data (page mới), fallback về best_posting_times trong config.

Data chất lượng tốt hơn sẽ được user bổ sung sau (sales, clicks, etc.).
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any, Optional

from src.task_queue_db import TaskQueueDB
from sqlalchemy import text


class PostingOptimizer:
    def __init__(self):
        self.q = TaskQueueDB()
        self.fanpages = self._load_fanpages_config()

    def _load_fanpages_config(self) -> Dict[str, Any]:
        config_path = os.path.join("config", "fanpages.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_historical_performance(self, fanpage_key: str, theme: Optional[str] = None, days_back: int = 30) -> Dict[int, int]:
        """
        Lấy data nội bộ: đếm số task COMPLETED theo giờ (0-23) trong N ngày gần nhất.
        Đây là proxy cho "tỉ lệ chuyển đổi" / engagement thành công.
        """
        since = (datetime.utcnow() - timedelta(days=days_back)).isoformat()

        query = text("""
            SELECT 
                strftime('%H', json_extract(payload, '$.scheduled_at')) as hour,
                COUNT(*) as success_count
            FROM tasks
            WHERE 
                worker_name = 'facebook_autoposter'
                AND status = 'COMPLETED'
                AND json_extract(payload, '$.fanpage_key') = :fanpage_key
                AND created_at >= :since
                AND json_extract(payload, '$.scheduled_at') IS NOT NULL
            GROUP BY strftime('%H', json_extract(payload, '$.scheduled_at'))
            ORDER BY success_count DESC
        """)

        params = {"fanpage_key": fanpage_key, "since": since}

        if theme:
            # Rebuild with theme filter
            base_query = """
                SELECT 
                    strftime('%H', json_extract(payload, '$.scheduled_at')) as hour,
                    COUNT(*) as success_count
                FROM tasks
                WHERE 
                    worker_name = 'facebook_autoposter'
                    AND status = 'COMPLETED'
                    AND json_extract(payload, '$.fanpage_key') = :fanpage_key
                    AND created_at >= :since
                    AND json_extract(payload, '$.scheduled_at') IS NOT NULL
                    AND json_extract(payload, '$.theme') = :theme
                GROUP BY strftime('%H', json_extract(payload, '$.scheduled_at'))
                ORDER BY success_count DESC
            """
            query = text(base_query)
            params["theme"] = theme
            params["fanpage_key"] = fanpage_key  # ensure it's set

        performance: Dict[int, int] = defaultdict(int)

        try:
            with self.q.engine.connect() as conn:
                result = conn.execute(query, params)
                for row in result:
                    if row[0] is not None:
                        hour = int(row[0])
                        performance[hour] = row[1]
        except Exception as e:
            print(f"[Optimizer] Lỗi query historical data: {e}")
            # Fallback: trả về rỗng, sẽ dùng config

        return dict(performance)

    def get_best_posting_hours(
        self,
        fanpage_key: str,
        theme: Optional[str] = None,
        top_n: int = 5,
        days_back: int = 30,
        fallback_to_config: bool = True
    ) -> List[int]:
        """
        Trả về danh sách giờ tốt nhất (sorted theo performance cao nhất) để đăng bài.

        Ưu tiên:
        1. Data nội bộ thực tế (số COMPLETED cao ở giờ nào).
        2. Nếu chưa có data → fallback về best_posting_times trong config/fanpages.json.

        Đây là "tối ưu tỉ lệ chuyển đổi bằng mọi giá" dựa trên data có sẵn.
        """
        historical = self.get_historical_performance(fanpage_key, theme, days_back)

        if historical:
            # Sắp xếp theo success_count giảm dần
            sorted_hours = sorted(historical.items(), key=lambda x: x[1], reverse=True)
            best_hours = [hour for hour, count in sorted_hours[:top_n]]
            print(f"[Optimizer] Dùng data nội bộ cho {fanpage_key}/{theme or 'any'}: top {best_hours}")
            return best_hours

        # Fallback config
        if fallback_to_config and fanpage_key in self.fanpages:
            cfg = self.fanpages[fanpage_key]
            config_times = cfg.get("best_posting_times", [8, 12, 18, 20])
            print(f"[Optimizer] Chưa có data nội bộ cho {fanpage_key} → dùng config best times: {config_times}")
            return config_times[:top_n]

        # Ultimate fallback
        print(f"[Optimizer] Không có data và config cho {fanpage_key} → dùng mặc định")
        return [8, 12, 18, 20][:top_n]

    def get_performance_report(self, days_back: int = 30) -> Dict[str, Any]:
        """
        Báo cáo tổng hợp để user thấy rõ "tối ưu được bao nhiêu".
        """
        report = {}
        for key in self.fanpages.keys():
            perf = self.get_historical_performance(key, days_back=days_back)
            total_success = sum(perf.values())
            report[key] = {
                "total_successful_posts": total_success,
                "best_hours": sorted(perf.items(), key=lambda x: x[1], reverse=True)[:5] if perf else [],
                "has_data": bool(perf)
            }
        return report

    def optimize_and_update_best_times(self, fanpage_key: str, theme: Optional[str] = None, days_back: int = 30, min_samples: int = 5) -> List[int]:
        """
        Tự động tối ưu: Lấy giờ tốt nhất từ data nội bộ (số task COMPLETED).
        Đây là cách hệ thống "biết tối ưu tỉ lệ chuyển đổi" từ data nội bộ.
        Nếu có đủ dữ liệu, trả về top giờ. 
        Gợi ý cập nhật config nếu tốt hơn.
        """
        historical = self.get_historical_performance(fanpage_key, theme, days_back)
        if len(historical) >= min_samples:
            sorted_hours = [h for h, c in sorted(historical.items(), key=lambda x: x[1], reverse=True)]
            print(f"[Optimizer] Đủ data nội bộ ({len(historical)} giờ có samples). Giờ tối ưu từ data: {sorted_hours[:7]}")
            # Gợi ý update config
            if fanpage_key in self.fanpages:
                current = self.fanpages[fanpage_key].get("best_posting_times", [])
                if sorted_hours[:7] != current[:7]:
                    print(f"[Optimizer] Gợi ý cập nhật best_posting_times cho {fanpage_key} thành: {sorted_hours[:7]}")
            return sorted_hours[:7]
        else:
            print(f"[Optimizer] Chưa đủ data nội bộ (chỉ {len(historical)} giờ, cần >= {min_samples}). Dùng best_posting_times từ config.")
            if fanpage_key in self.fanpages:
                return self.fanpages[fanpage_key].get("best_posting_times", [8,12,18,20])
            return [8,12,18,20]

# Ví dụ dùng:
if __name__ == "__main__":
    opt = PostingOptimizer()
    print("Best hours for ai_tech:", opt.get_best_posting_hours("ai_tech", "ai_tech"))
    print("\nPerformance report:")
    print(json.dumps(opt.get_performance_report(), indent=2, default=str))
    print("\nAuto optimize for ai_tech:")
    print(opt.optimize_and_update_best_times("ai_tech", "ai_tech"))
