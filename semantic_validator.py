"""
SEN V3 — Semantic Validator
=============================
Kiểm định ngữ nghĩa prompt trước khi đưa vào pipeline LLM.
Ngăn "garbage in → garbage out" và tiết kiệm chi phí API.

3 tầng kiểm tra:
  1. Rule-based nhanh (length, keyword blacklist)
  2. Heuristic scoring (entropy, coherence)
  3. LLM-based deep check (chỉ khi 2 tầng trên không chắc)
"""

import logging
import re
import math
from typing import Optional

logger = logging.getLogger(__name__)

# ── Cấu hình ──────────────────────────────────────────────────────────────────

MIN_PROMPT_LENGTH  = 20     # ký tự
MAX_PROMPT_LENGTH  = 4000   # ký tự
MIN_ENTROPY        = 2.5    # bit — quá thấp = nội dung lặp vô nghĩa
SCORE_PASS         = 0.6    # ngưỡng heuristic để tự động pass
SCORE_FAIL         = 0.3    # ngưỡng heuristic để tự động fail
                            # [0.3 - 0.6] → gọi LLM deep check

BLACKLIST_PATTERNS = [
    r"\b(hack|crack|exploit|injection|bypass|jailbreak)\b",
    r"[\x00-\x08\x0b\x0c\x0e-\x1f]",   # control chars
    r"(.)\1{15,}",                        # ký tự lặp ≥ 15 lần liên tiếp
]

AFFILIATE_KEYWORDS = [
    "sản phẩm", "mua ngay", "giảm giá", "ưu đãi", "review",
    "đánh giá", "khuyến mãi", "link", "affiliate", "commission",
    "product", "buy", "discount", "offer", "deal",
]


class SemanticValidator:
    """
    Sử dụng trong MetaAgent trước khi dispatch:
        validator = SemanticValidator()
        ok = await validator.validate(prompt)
    """

    def __init__(self):
        self._compiled_blacklist = [
            re.compile(p, re.IGNORECASE) for p in BLACKLIST_PATTERNS
        ]

    async def validate(self, prompt: str) -> bool:
        """
        Trả về True nếu prompt hợp lệ.
        Trả về False nếu bị reject.
        """
        # Tầng 1: Rule-based (nhanh, không tốn API)
        rule_result = self._rule_check(prompt)
        if rule_result is not None:
            return rule_result

        # Tầng 2: Heuristic scoring
        score = self._heuristic_score(prompt)
        logger.debug(f"[SemanticValidator] Heuristic score: {score:.2f}")

        if score >= SCORE_PASS:
            return True
        if score < SCORE_FAIL:
            logger.warning(
                f"[SemanticValidator] Reject — score thấp ({score:.2f}): "
                f"{prompt[:60]}..."
            )
            return False

        # Tầng 3: LLM deep check (chỉ khi không chắc)
        return await self._llm_check(prompt)

    # ── Tầng 1: Rule-based ────────────────────────────────────────────────────

    def _rule_check(self, prompt: str) -> Optional[bool]:
        """
        Trả về True/False nếu chắc chắn.
        Trả về None nếu cần kiểm tra thêm.
        """
        stripped = prompt.strip()

        if len(stripped) < MIN_PROMPT_LENGTH:
            logger.warning(f"[SemanticValidator] Reject — quá ngắn ({len(stripped)} ký tự)")
            return False

        if len(stripped) > MAX_PROMPT_LENGTH:
            logger.warning(f"[SemanticValidator] Reject — quá dài ({len(stripped)} ký tự)")
            return False

        for pattern in self._compiled_blacklist:
            if pattern.search(stripped):
                logger.warning(
                    f"[SemanticValidator] Reject — blacklist pattern: {pattern.pattern}"
                )
                return False

        return None   # chưa kết luận, tiếp tục tầng 2

    # ── Tầng 2: Heuristic ────────────────────────────────────────────────────

    def _heuristic_score(self, prompt: str) -> float:
        """
        Tính điểm 0.0–1.0 dựa trên:
          - Shannon entropy (độ đa dạng ký tự)
          - Tỷ lệ affiliate keywords
          - Tỷ lệ chữ thường/chữ hoa (all caps = spam)
          - Tỷ lệ ký tự đặc biệt
        """
        scores = []

        # Shannon entropy
        entropy = self._shannon_entropy(prompt)
        scores.append(min(entropy / 5.0, 1.0))   # normalize: 5 bit = 1.0

        # Affiliate keyword density
        words       = prompt.lower().split()
        if words:
            aff_count   = sum(1 for w in words if any(k in w for k in AFFILIATE_KEYWORDS))
            aff_ratio   = aff_count / len(words)
            scores.append(min(aff_ratio * 3, 1.0))   # ít nhất 1 keyword trong 3 từ = tốt

        # Không phải all-caps spam
        alpha = [c for c in prompt if c.isalpha()]
        if alpha:
            upper_ratio = sum(1 for c in alpha if c.isupper()) / len(alpha)
            scores.append(1.0 - min(upper_ratio * 2, 1.0))

        # Tỷ lệ ký tự đặc biệt thấp
        special = sum(1 for c in prompt if not c.isalnum() and c not in " .,!?-\n")
        special_ratio = special / max(len(prompt), 1)
        scores.append(1.0 - min(special_ratio * 5, 1.0))

        return sum(scores) / len(scores) if scores else 0.0

    @staticmethod
    def _shannon_entropy(text: str) -> float:
        if not text:
            return 0.0
        freq = {}
        for c in text:
            freq[c] = freq.get(c, 0) + 1
        n = len(text)
        return -sum((f / n) * math.log2(f / n) for f in freq.values())

    # ── Tầng 3: LLM deep check ───────────────────────────────────────────────

    async def _llm_check(self, prompt: str) -> bool:
        """
        Gọi LLM nhẹ (Gemini Flash) để phán quyết cuối cùng.
        Chỉ dùng khi heuristic score nằm trong vùng không chắc [0.3–0.6].

        TODO: kết nối với SafeLLMWriter khi tích hợp thực tế.
        """
        logger.info(
            f"[SemanticValidator] Gọi LLM deep check cho prompt: {prompt[:60]}..."
        )

        # Placeholder — thay bằng call Gemini Flash thực tế
        # check_prompt = (
        #     "Đánh giá xem đây có phải yêu cầu tạo nội dung affiliate marketing hợp lệ không. "
        #     "Trả lời chỉ 'YES' hoặc 'NO'.\n\nYêu cầu: " + prompt
        # )
        # result = await safe_writer.generate(check_prompt, tier=LLMTier.FILTER)
        # return result and "YES" in result.content.upper()

        return True   # mặc định pass khi chưa tích hợp LLM
