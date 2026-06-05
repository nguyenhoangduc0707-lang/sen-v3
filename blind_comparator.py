import json
from typing import Dict, Tuple

class BlindComparator:
    def __init__(self):
        # Rubric đánh giá: mỗi tiêu chí điểm 1-5
        self.rubric = {
            "content_relevance": "Nội dung liên quan đến campaign?",
            "call_to_action": "Có kêu gọi hành động rõ ràng?",
            "engagement": "Mức độ hấp dẫn, sáng tạo?",
            "formatting": "Định dạng, dấu câu, chữ hoa/thường?",
            "affiliate_link_presence": "Có link affiliate hợp lệ?"
        }

    def _score_article(self, article: str) -> Dict:
        # Hàm chấm điểm đơn giản dựa trên heuristic
        # Bạn có thể thay bằng LLM hoặc rule phức tạp hơn
        scores = {}
        # relevance: có chứa tên campaign? (giả sử campaign name in article)
        # Ở đây ta demo: cứ cho điểm cao nếu có từ "sale" hoặc "giảm giá"
        scores["content_relevance"] = 5 if "sale" in article.lower() else 3
        scores["call_to_action"] = 5 if "mua ngay" in article.lower() else 3
        scores["engagement"] = 5 if any(w in article for w in ["🌟", "🔥", "🎯"]) else 3
        scores["formatting"] = 5 if article.count("!") >= 1 else 3
        scores["affiliate_link_presence"] = 5 if "https://" in article else 1
        return scores

    def compare(self, article_a: str, article_b: str) -> Tuple[str, Dict]:
        scores_a = self._score_article(article_a)
        scores_b = self._score_article(article_b)
        total_a = sum(scores_a.values())
        total_b = sum(scores_b.values())

        if total_a > total_b:
            winner = "A"
            reasoning = f"Điểm A ({total_a}) cao hơn B ({total_b})"
        elif total_b > total_a:
            winner = "B"
            reasoning = f"Điểm B ({total_b}) cao hơn A ({total_a})"
        else:
            winner = "TIE"
            reasoning = "Hai bài viết bằng điểm nhau"

        return winner, {
            "winner": winner,
            "reasoning": reasoning,
            "scores": {"A": scores_a, "B": scores_b}
        }

if __name__ == "__main__":
    comp = BlindComparator()
    art_a = "🌟 Siêu sale! Điện thoại giảm giá 50%. Mua ngay tại link: https://aff.com/1"
    art_b = "Điện thoại mới. Có bán ở shop."
    winner, result = comp.compare(art_a, art_b)
    print(json.dumps(result, indent=2, ensure_ascii=False))