# app/main.py

from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
import os

from state import sessions
from detector import detect_scam_signal
from intelligence import extract_intelligence
from ai_agent import run_ai_agent
from callback import send_final_callback

load_dotenv()

API_KEY = os.getenv("API_KEY")

app = FastAPI()

@app.post("/honeypot/message")
def honeypot(payload: dict, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session_id = payload["sessionId"]
    message_text = payload["message"]["text"]
    history = payload.get("conversationHistory", [])

    if session_id not in sessions:
        sessions[session_id] = {
            "sessionId": session_id,
            "scamDetected": False,
            "stage": "early",
            "totalMessages": 0,
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            }
        }

    session = sessions[session_id]
    session["totalMessages"] += 1

    # Lightweight signal detection
    if detect_scam_signal(message_text):
        session["scamDetected"] = True

    # Run AI agent
    ai_result = run_ai_agent(message_text, history)

    session["stage"] = ai_result["conversationStage"]
    session["scamDetected"] = ai_result["scamDetected"] or session["scamDetected"]

    # Extract intelligence silently
    extract_intelligence(message_text, session["intelligence"])
    session["intelligence"]["suspiciousKeywords"].extend(
        ai_result["extractedHints"].get("keywords", [])
    )

    # End condition → mandatory callback
    if session["totalMessages"] >= 15 and session["scamDetected"]:
        send_final_callback(session)

    return {
        "status": "success",
        "reply": ai_result["reply"]
    }

