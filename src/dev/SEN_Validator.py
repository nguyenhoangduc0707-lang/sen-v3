# src/dev/SEN_Validator.py
import re


class SEN_Validator:
    def __init__(self):
        self.patterns = [r"\d+\s*[\+\-\*]\s*\d+", r"calculate|tinh toan|sum|total"]

    def scan(self, text):
        for p in self.patterns:
            if re.search(p, text, re.I):
                return {"is_clean": False, "issues": [p]}
        return {"is_clean": True, "issues": []}
