from __future__ import annotations

from groq_brain import ask_groq
from gemini_brain import ask_gemini


def is_error_response(response: str | None) -> bool:
    if not response:
        return True

    response_lower = response.lower()

    error_words = (
        "groq error",
        "gemini error",
        "api error",
        "currently unavailable",
        "rate limit",
        "quota exceeded",
        "could not reach",
        "failed",
    )

    return any(word in response_lower for word in error_words)


def ask_ai(prompt: str) -> str:
    prompt = prompt.strip()

    if not prompt:
        return "Please provide a question, sir."

    # First brain: Groq
    try:
        response = ask_groq(prompt)

        if not is_error_response(response):
            print("AI provider: Groq")
            return response

    except Exception as error:
        print(f"Groq failed: {error}")

    # Backup brain: Gemini
    try:
        response = ask_gemini(prompt)

        if not is_error_response(response):
            print("AI provider: Gemini")
            return response

    except Exception as error:
        print(f"Gemini failed: {error}")

    return "Sorry sir, both of my AI brains are currently unavailable."
