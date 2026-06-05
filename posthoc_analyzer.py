import json
from typing import Dict

class PostHocAnalyzer:
    def analyze(self, winner_article: str, loser_article: str, winner_skill_instruction: str, loser_skill_instruction: str) -> Dict:
        """
        Phân tích điểm mạnh/yếu dựa trên nội dung bài viết và instruction của skill.
        Ở đây dùng heuristic đơn giản; bạn có thể thay bằng LLM.
        """
        strengths = []
        weaknesses = []

        # So sánh về chiều dài
        if len(winner_article) > len(loser_article):
            strengths.append(f"Bài viết thắng dài hơn ({len(winner_article)} vs {len(loser_article)} ký tự)")
        else:
            weaknesses.append(f"Bài viết thua ngắn hơn ({len(loser_article)} vs {len(winner_article)} ký tự)")

        # So sánh về emoji / ký tự đặc biệt
        winner_emojis = sum(1 for c in winner_article if c in "🌟🔥🎯💥")
        loser_emojis = sum(1 for c in loser_article if c in "🌟🔥🎯💥")
        if winner_emojis > loser_emojis:
            strengths.append("Bài viết thắng có nhiều emoji hơn (tăng tính hấp dẫn)")
        else:
            weaknesses.append("Bài viết thua thiếu emoji, kém hấp dẫn")

        # So sánh về link affiliate
        if "https://" in winner_article and "https://" not in loser_article:
            strengths.append("Bài viết thắng có link affiliate, bài thua không có")
        elif "https://" in loser_article and "https://" not in winner_article:
            weaknesses.append("Bài viết thua có link affiliate nhưng bài thắng lại không? (kiểm tra lại)")

        # Gợi ý cải tiến dựa trên instruction (mô phỏng)
        suggestions = []
        if "call_to_action" not in loser_skill_instruction.lower():
            suggestions.append({
                "priority": "high",
                "category": "instructions",
                "suggestion": "Thêm dòng 'kêu gọi hành động' (ví dụ: 'Mua ngay kẻo lỡ!') vào instruction",
                "expected_impact": "Tăng tỷ lệ nhấp link"
            })
        if "emoji" not in loser_skill_instruction.lower():
            suggestions.append({
                "priority": "medium",
                "category": "examples",
                "suggestion": "Thêm ví dụ sử dụng emoji (🌟, 🔥) để bài viết sinh động hơn",
                "expected_impact": "Tăng tính hấp dẫn, cải thiện điểm engagement"
            })
        return {
            "winner_strengths": strengths,
            "loser_weaknesses": weaknesses,
            "improvement_suggestions": suggestions
        }

if __name__ == "__main__":
    analyzer = PostHocAnalyzer()
    winner = "🌟 Siêu sale! Điện thoại giảm giá 50%. Mua ngay tại link: https://aff.com/1"
    loser = "Điện thoại mới. Có bán ở shop."
    winner_inst = "Viết bài hấp dẫn, có emoji, kêu gọi hành động."
    loser_inst = "Viết bài giới thiệu sản phẩm."
    result = analyzer.analyze(winner, loser, winner_inst, loser_inst)
    print(json.dumps(result, indent=2, ensure_ascii=False))