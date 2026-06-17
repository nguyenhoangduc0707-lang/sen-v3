import json
import random
from typing import List, Dict, Any, Tuple

class BlindComparator:
    """
    Blind Comparator Agent - So sánh mù giữa các phiên bản nội dung (A/B testing)
    Dựa trên rubric_affiliate.json theo tài liệu kiến trúc SEN V3.
    """

    def __init__(self, rubric_path: str = "config/rubric_affiliate.json"):
        self.rubric = self._load_rubric(rubric_path)

    def _load_rubric(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[BlindComparator] {path} not found, using defaults.")
            return {
                "criteria": [
                    {"name": "clarity", "weight": 25, "description": "Rõ ràng, dễ hiểu"},
                    {"name": "persuasiveness", "weight": 30, "description": "Tính thuyết phục"},
                    {"name": "engagement", "weight": 25, "description": "Thu hút người đọc"},
                    {"name": "cta_effectiveness", "weight": 20, "description": "Hiệu quả kêu gọi hành động"}
                ]
            }

    def compare(self, versions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        So sánh mù giữa nhiều phiên bản nội dung.

        Args:
            versions: [{"id": "v1", "content": "..."}, ...]

        Returns:
            {
                "winner_id": str,
                "scores": dict,
                "ranking": list
            }
        """
        if len(versions) < 2:
            return {"error": "Need at least 2 versions to compare"}

        # Shuffle for true blind comparison
        shuffled = versions.copy()
        random.shuffle(shuffled)

        scores = {}
        for v in shuffled:
            scores[v["id"]] = self._evaluate(v["content"])

        # Rank by total weighted score
        ranking = sorted(
            [{"id": vid, "total": s["total"], "details": s["details"]} 
             for vid, s in scores.items()],
            key=lambda x: x["total"],
            reverse=True
        )

        return {
            "winner_id": ranking[0]["id"],
            "scores": scores,
            "ranking": ranking
        }

    def _evaluate(self, content: str) -> Dict[str, Any]:
        """Score a single piece of content against the rubric (0-100 weighted)."""
        results = {}
        total = 0.0

        for criterion in self.rubric.get("criteria", []):
            name = criterion["name"]
            weight = criterion["weight"]

            if name == "clarity":
                # Simple heuristic: shorter average sentence = clearer
                sentences = max(1, content.count('.') + content.count('!') + content.count('?'))
                avg_len = len(content.split()) / sentences
                raw = 100 if avg_len < 15 else (75 if avg_len < 22 else 45)
            elif name == "persuasiveness":
                persuasive = ["tốt nhất", "uy tín", "chất lượng cao", "tiết kiệm", "giảm giá", "độc quyền", "hot"]
                count = sum(1 for w in persuasive if w.lower() in content.lower())
                raw = min(100, 40 + count * 12)
            elif name == "engagement":
                emojis = sum(1 for c in content if c in "🔥🌟💸🚀🎯✨")
                exclamations = content.count('!')
                raw = min(100, 50 + emojis * 8 + exclamations * 6)
            elif name == "cta_effectiveness":
                ctas = ["mua ngay", "đặt hàng", "sở hữu ngay", "click", "tại đây", "liên hệ ngay"]
                count = sum(1 for c in ctas if c.lower() in content.lower())
                raw = min(100, count * 25)
            else:
                raw = 70

            weighted = raw * weight / 100
            results[name] = {"raw": round(raw, 1), "weighted": round(weighted, 1)}
            total += weighted

        return {"total": round(total, 1), "details": results}


if __name__ == "__main__":
    # Honest test
    comp = BlindComparator()
    v1 = {"id": "v1", "content": "🔥 Siêu sale! Điện thoại giảm 50%. Mua ngay tại https://aff.link/1 #hot #affiliate"}
    v2 = {"id": "v2", "content": "Điện thoại mới. Bán ở đây."}
    result = comp.compare([v1, v2])
    print(json.dumps(result, indent=2, ensure_ascii=False))