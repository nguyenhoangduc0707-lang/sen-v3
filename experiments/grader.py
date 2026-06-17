import json
import re
import os
from typing import Dict, List, Any

class Grader:
    """
    Grader Agent - Đánh giá chất lượng nội dung tuyệt đối (Pass/Fail)
    Dựa trên expectations.json theo tài liệu kiến trúc SEN V3.
    """

    def __init__(self, expectations_path: str = "config/expectations.json"):
        self.rubric = self._load_rubric(expectations_path)

    def _load_rubric(self, path: str) -> Dict[str, Any]:
        """Load expectations from JSON file, with sensible defaults."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[Grader] Warning: {path} not found, using built-in defaults.")
            return {
                "min_length": 150,
                "max_length": 800,
                "require_affiliate_link": True,
                "require_cta": True,
                "require_hashtags": True,
                "cta_keywords": ["mua ngay", "đặt hàng", "sở hữu ngay", "click", "tại đây"],
                "hashtag_min_count": 2,
                "forbidden_words": ["lừa đảo", "giả", "kém chất lượng"]
            }

    def grade(self, content: str, affiliate_link: str = None) -> Dict[str, Any]:
        """
        Grade content against the rubric.

        Returns:
            {
                "passed": bool,
                "score": int (0-100),
                "issues": list[str],
                "details": dict
            }
        """
        issues = []
        score = 100
        rubric = self.rubric

        # 1. Length checks
        length = len(content)
        if length < rubric.get("min_length", 150):
            issues.append(f"Content too short: {length} < {rubric.get('min_length')}")
            score -= 20
        elif length > rubric.get("max_length", 800):
            issues.append(f"Content too long: {length} > {rubric.get('max_length')}")
            score -= 10

        # 2. Affiliate link
        if rubric.get("require_affiliate_link", True):
            if not affiliate_link or (affiliate_link and affiliate_link not in content):
                issues.append("Affiliate link missing or not embedded in content")
                score -= 30

        # 3. CTA
        if rubric.get("require_cta", True):
            cta_keywords = rubric.get("cta_keywords", ["mua ngay", "đặt hàng"])
            if not any(kw.lower() in content.lower() for kw in cta_keywords):
                issues.append("No strong Call-To-Action found")
                score -= 20

        # 4. Hashtags
        if rubric.get("require_hashtags", True):
            hashtags = [w for w in content.split() if w.startswith('#')]
            min_count = rubric.get("hashtag_min_count", 2)
            if len(hashtags) < min_count:
                issues.append(f"Not enough hashtags: found {len(hashtags)}, need ≥{min_count}")
                score -= 15

        # 5. Forbidden words
        forbidden = rubric.get("forbidden_words", [])
        found_forbidden = [w for w in forbidden if w.lower() in content.lower()]
        if found_forbidden:
            issues.append(f"Contains forbidden words: {found_forbidden}")
            score -= 25

        # Final decision
        passed = len(issues) == 0 and score >= 60

        return {
            "passed": passed,
            "score": max(0, score),
            "issues": issues,
            "details": {
                "length": length,
                "hashtag_count": len([w for w in content.split() if w.startswith('#')]),
                "has_affiliate_link": bool(affiliate_link and affiliate_link in content) if affiliate_link else False
            }
        }


if __name__ == "__main__":
    # Honest self-test
    sample = "🔥 Siêu sale! Điện thoại thông minh giảm giá sốc 50%. Mua ngay tại https://affiliate.link/123 để nhận hoa hồng cực khủng! #affiliate #kinhtien"
    g = Grader()
    result = g.grade(sample, affiliate_link="https://affiliate.link/123")
    print(json.dumps(result, indent=2, ensure_ascii=False))