from command_router import run_commands
from voice import speak,listen
from datetime import datetime
import json

with open("config.json", "r") as file:
    keys = json.load(file)


def greet_user() -> None:
    hour = datetime.now().hour

    if 6 <= hour <= 11:
        greeting = "Good morning"
    elif 12 <= hour <= 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    speak(f"{greeting}, sir. How can I help you today?")


def security() -> bool:
    speak("Verification required. Please enter your security code, sir.")
    code = input("code: ")

    if code == keys["SECURITY_KEY"]:
        speak("Security verified.")
        return True
    else:
        speak("Invalid code. Access to SARAS has been denied, sir.")
        return False


def main() -> None:
    if not security():
        return

    greet_user()

    while True:
        command = listen()

        if not command:
            print("No activation command detected.")
            continue

        command = command.lower().strip()

        if "activate" in command:
            speak(
                "Activation complete. SARAS is at your service sir. How may I assist you today, sir")
            break

    while True:
        command = listen()

        if not command:
            print("I did not catch that, sir. Please repeat the command.")
            continue

        command = command.lower().strip()

        if any(word in command for word in [
            "deactivate",
            "stop listening",
            "go offline",
            "exit assistant",
            "terminate assistant"
        ]):
            speak("SARAS signing off. I'll be ready whenever you need me again, sir")
            break

        try:
            run_commands(command)
        except Exception as error:
            print(f"Command error: {error}")
            speak("Sorry sir, an error occurred while executing that command.")


if __name__ == "__main__":
    main()
