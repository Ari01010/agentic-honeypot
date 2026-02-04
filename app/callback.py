# app/callback.py

import requests

GUVI_ENDPOINT = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_callback(session: dict):
    payload = {
        "sessionId": session["sessionId"],
        "scamDetected": True,
        "totalMessagesExchanged": session["totalMessages"],
        "extractedIntelligence": session["intelligence"],
        "agentNotes": "Scammer used urgency tactics and payment redirection"
    }

    try:
        requests.post(GUVI_ENDPOINT, json=payload, timeout=5)
    except Exception as e:
        print("Callback failed:", e)

