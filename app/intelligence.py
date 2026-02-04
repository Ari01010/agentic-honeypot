# app/intelligence.py

import re

def extract_intelligence(text: str, intelligence: dict):
    upi_ids = re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", text)
    phone_numbers = re.findall(r"\+91\d{10}", text)
    links = re.findall(r"https?://\S+", text)

    for upi in upi_ids:
        if upi not in intelligence["upiIds"]:
            intelligence["upiIds"].append(upi)

    for phone in phone_numbers:
        if phone not in intelligence["phoneNumbers"]:
            intelligence["phoneNumbers"].append(phone)

    for link in links:
        if link not in intelligence["phishingLinks"]:
            intelligence["phishingLinks"].append(link)

    for word in ["urgent", "verify", "blocked", "suspended"]:
        if word in text.lower() and word not in intelligence["suspiciousKeywords"]:
            intelligence["suspiciousKeywords"].append(word)

