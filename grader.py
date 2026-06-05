import json
import re
from typing import Dict, List

class Grader:
    def __init__(self, expectations: List[Dict]):
        """
        expectations = [
            {"text": "Bài viết có chứa link affiliate", "regex": r"https?://.*affiliate.*"},
            {"text": "Độ dài > 50 ký tự", "min_length": 50},
            {"text": "Có từ khóa 'hoa hồng'", "regex": r"hoa hồng"},
            {"text": "Có cảm xúc tích cực", "positive_words": ["siêu", "hot", "xu hướng", "kiếm tiền"]}
        ]
        """
        self.expectations = expectations

    def grade(self, article: str) -> Dict:
        results = []
        for exp in self.expectations:
            passed = False
            evidence = ""
            if "regex" in exp:
                if re.search(exp["regex"], article, re.IGNORECASE):
                    passed = True
                    evidence = f"Tìm thấy pattern: {exp['regex']}"
                else:
                    evidence = "Không tìm thấy pattern"
            elif "min_length" in exp:
                if len(article) >= exp["min_length"]:
                    passed = True
                    evidence = f"Độ dài {len(article)} >= {exp['min_length']}"
                else:
                    evidence = f"Độ dài {len(article)} < {exp['min_length']}"
            elif "positive_words" in exp:
                words = exp["positive_words"]
                found = [w for w in words if w in article.lower()]
                if found:
                    passed = True
                    evidence = f"Các từ tích cực: {', '.join(found)}"
                else:
                    evidence = "Không có từ tích cực nào"
            else:
                # fallback
                passed = False
                evidence = "Không rõ expectation"
            results.append({
                "text": exp["text"],
                "passed": passed,
                "evidence": evidence
            })
        total = len(results)
        passed_count = sum(1 for r in results if r["passed"])
        return {
            "expectations": results,
            "summary": {
                "passed": passed_count,
                "failed": total - passed_count,
                "total": total,
                "pass_rate": passed_count / total if total > 0 else 0
            }
        }

if __name__ == "__main__":
    # Test
    sample_article = "🌟 Siêu sale! Chiến dịch thời trang mùa hè hoa hồng lên tới 12.5%. Mua ngay tại https://shopee.com/affiliate/123"
    expectations = [
        {"text": "Có link affiliate", "regex": r"https?://.*affiliate"},
        {"text": "Độ dài > 30", "min_length": 30},
        {"text": "Có từ 'hoa hồng'", "regex": r"hoa hồng"},
        {"text": "Có từ tích cực", "positive_words": ["siêu", "hot"]}
    ]
    g = Grader(expectations)
    result = g.grade(sample_article)
    print(json.dumps(result, indent=2, ensure_ascii=False))