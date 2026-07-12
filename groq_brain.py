from __future__ import annotations

import json
from pathlib import Path

from groq import Groq


with open("config.json","r", encoding="utf-8") as file:
    keys = json.load(file)

client = Groq(api_key=keys["GROQ_API"])


def ask_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are S.A.R.A.S, the Smart Autonomous Responsive "
                    "Assistant System developed by Goutham V. "
                    "Keep answers helpful and concise. Address the user "
                    "as sir naturally."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.7,
        max_tokens=1500,
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("Groq returned an empty response.")

    return answer.strip()
