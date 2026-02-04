# app/detector.py

SCAM_KEYWORDS = [
    "blocked", "suspended", "verify", "urgent",
    "upi", "otp", "account", "immediately",
  "urgent response required","verify your account",
  "suspended account","wire transfer","unclaimed funds",
  "click this link","final notice"
]

def detect_scam_signal(text: str) -> bool:
    text = text.lower()
    score = sum(1 for kw in SCAM_KEYWORDS if kw in text)
    return score >= 2

