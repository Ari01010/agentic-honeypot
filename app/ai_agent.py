# app/ai_agent.py
import json
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run_ai_agent(message: str, history: list):
    for _ in range(2):  # self-correction retry loop
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *history,
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )

        output = json.loads(response.choices[0].message.content)

        if not output.get("selfCorrectionNeeded"):
            return output

    return output

