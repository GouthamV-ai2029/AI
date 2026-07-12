from __future__ import annotations

import json

from google import genai

with open("config.json", "r") as f:
    keys = json.load(f)


client = genai.Client(api_key=keys["GEMINI_API"])


def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "system_instruction": (
                "You are S.A.R.A.S, the Smart Autonomous Responsive "
                "Assistant System developed by Goutham V. "
                "Keep answers helpful and concise. Address the user "
                "as sir naturally."
            ),
            "temperature": 0.7,
            "max_output_tokens": 1500,
        },
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text.strip()
