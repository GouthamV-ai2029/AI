from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Callable

from voice import speak
import windows_commands as wc
from ai_brain import ask_ai


# ============================================================
# COMMAND ALIASES
# ============================================================

COMMAND_ALIASES = {
    # Assistant
    "your intro": "introduce yourself",
    "who are you": "introduce yourself",
    "introduce saras": "introduce yourself",

    # Websites
    "yt": "open youtube",
    "youtube": "open youtube",
    "google": "open google",
    "chat gpt": "open chatgpt",
    "github": "open github",
    "gmail": "open gmail",
    "insta": "open instagram",
    "instagram": "open instagram",
    "fb": "open facebook",
    "facebook": "open facebook",
    "wiki": "open wikipedia",
    "wikipedia": "open wikipedia",
    "discord": "open discord",

    # Apps
    "note pad": "open notepad",
    "notepad": "open notepad",
    "calc": "open calculator",
    "calculator": "open calculator",
    "paint": "open paint",
    "files": "open file explorer",
    "explorer": "open file explorer",
    "cmd": "open command prompt",
    "power shell": "open powershell",
    "terminal": "open windows terminal",
    "task manager": "open task manager",
    "control panel": "open control panel",
    "device manager": "open device manager",
    "disk management": "open disk management",
    "services": "open services",
    "system info": "open system information",
    "system configuration": "open system configuration",
    "resource monitor": "open resource monitor",
    "performance monitor": "open performance monitor",
    "event viewer": "open event viewer",
    "registry editor": "open registry editor",
    "character map": "open character map",
    "keyboard": "open on screen keyboard",
    "magnifier": "open magnifier",
    "snipping": "open snipping tool",
    "camera": "open camera",
    "spotify": "open spotify",
    "vlc": "open vlc",
    "code": "open vscode",
    "vs code": "open vscode",
    "visual studio code": "open vscode",
    "pycharm": "open pycharm",
    "android studio": "open android studio",

    # Security apps
    "windows security": "open windows security",
    "firewall": "open firewall",
    "credential manager": "open credential manager",
    "user accounts": "open user accounts",
    "disk cleanup": "open disk cleanup",
    "optimize drives": "open optimize drives",

    # Settings
    "settings": "open settings",
    "display settings": "open display settings",
    "personalization settings": "open personalization settings",
    "theme settings": "open theme settings",
    "taskbar settings": "open taskbar settings",
    "notification settings": "open notification settings",
    "wifi settings": "open wifi settings",
    "wi fi settings": "open wifi settings",
    "bluetooth settings": "open bluetooth settings",
    "sound settings": "open sound settings",
    "vpn settings": "open vpn settings",
    "hotspot settings": "open mobile hotspot settings",
    "mobile hotspot": "open mobile hotspot settings",
    "windows update": "open windows update",
    "storage settings": "open storage settings",
    "battery settings": "open battery settings",
    "clipboard settings": "open clipboard settings",
    "mouse settings": "open mouse settings",
    "keyboard settings": "open keyboard settings",
    "language settings": "open language settings",
    "date time settings": "open date time settings",
    "privacy settings": "open privacy settings",
    "camera privacy": "open camera privacy settings",
    "microphone privacy": "open microphone privacy settings",
    "recovery settings": "open recovery settings",
    "activation settings": "open activation settings",

    # Folders
    "downloads": "open downloads",
    "documents": "open documents",
    "pictures": "open pictures",
    "videos": "open videos",
    "music folder": "open music folder",
    "desktop folder": "open desktop folder",
    "this pc": "open this pc",
    "network folder": "open network folder",
    "recent files": "open recent files",
    "recycle bin": "open recycle bin",

    # Window controls
    "close current window": "close window",
    "close app": "close window",
    "minimise window": "minimize window",
    "minimise app": "minimize window",
    "maximize app": "maximize window",
    "restore app": "restore window",
    "full screen": "full screen",
    "switch app": "switch window",
    "switch application": "switch window",
    "snap left": "snap window left",
    "snap right": "snap window right",
    "desktop": "show desktop",
    "task view": "open task view",
    "start menu": "open start menu",

    # Keyboard controls
    "copy": "copy selected",
    "paste": "paste clipboard",
    "cut": "cut selected",
    "undo": "undo action",
    "redo": "redo action",
    "select everything": "select all",
    "enter": "press enter",
    "escape": "press escape",
    "tab": "press tab",
    "refresh": "refresh window",

    # Mouse controls
    "click": "left click",
    "left mouse click": "left click",
    "right mouse click": "right click",
    "double mouse click": "double click",
    "mouse up": "scroll up",
    "mouse down": "scroll down",
    "move mouse center": "center mouse",

    # Volume and media
    "increase volume": "volume up",
    "raise volume": "volume up",
    "decrease volume": "volume down",
    "lower volume": "volume down",
    "mute": "mute volume",
    "unmute": "unmute volume",
    "pause music": "play pause media",
    "resume music": "play pause media",
    "pause video": "play pause media",
    "resume video": "play pause media",
    "next song": "next track",
    "previous song": "previous track",
    "stop music": "stop media",

    # Security and power
    "lock pc": "lock computer",
    "lock system": "lock computer",
    "power off": "shutdown computer",
    "turn off computer": "shutdown computer",
    "shut down computer": "shutdown computer",
    "reboot computer": "restart computer",
    "restart pc": "restart computer",
    "cancel shutdown": "cancel shutdown",
    "sleep": "sleep computer",
    "hibernate": "hibernate computer",
    "sign out": "sign out",
    "empty bin": "empty recycle bin",
    "quick scan": "defender quick scan",

    # Network
    "my ip": "show ip address",
    "ip address": "show ip address",
    "check internet": "ping google",
    "test internet": "ping google",
    "flush dns": "flush dns",
    "release ip": "release ip",
    "renew ip": "renew ip",
    "network connections": "open network connections",
    "speed test": "open speed test",

    # Screen and clipboard
    "screenshot": "take screenshot",
    "capture screen": "take screenshot",
    "start recording": "start screen recording",
    "stop recording": "stop screen recording",
    "read clipboard": "read clipboard",
    "clear clipboard": "clear clipboard",

    # Time and date
    "what time is it": "current time",
    "show time": "current time",
    "tell me the time": "current time",
    "what is the date": "current date",
    "show date": "current date",
    "tell me the date": "current date",
}


# ============================================================
# EXACT COMMANDS
# ============================================================

EXACT_COMMANDS: dict[str, Callable[[], None]] = {
    # Websites
    "open youtube": wc.open_youtube,
    "open google": wc.open_google,
    "open chatgpt": wc.open_chatgpt,
    "open gmail": wc.open_gmail,
    "open github": wc.open_github,
    "open instagram": wc.open_instagram,
    "open facebook": wc.open_facebook,
    "open wikipedia": wc.open_wikipedia,
    "open discord": wc.open_discord,

    # Windows apps
    "open notepad": wc.open_notepad,
    "open calculator": wc.open_calculator,
    "open paint": wc.open_paint,
    "open file explorer": wc.open_file_explorer,
    "open command prompt": wc.open_command_prompt,
    "open powershell": wc.open_powershell,
    "open windows terminal": wc.open_windows_terminal,
    "open task manager": wc.open_task_manager,
    "open control panel": wc.open_control_panel,
    "open device manager": wc.open_device_manager,
    "open disk management": wc.open_disk_management,
    "open services": wc.open_services,
    "open system information": wc.open_system_information,
    "open system configuration": wc.open_system_configuration,
    "open resource monitor": wc.open_resource_monitor,
    "open performance monitor": wc.open_performance_monitor,
    "open event viewer": wc.open_event_viewer,
    "open registry editor": wc.open_registry_editor,
    "open character map": wc.open_character_map,
    "open on screen keyboard": wc.open_on_screen_keyboard,
    "open magnifier": wc.open_magnifier,
    "open snipping tool": wc.open_snipping_tool,
    "open camera": wc.open_camera,
    "open recycle bin": wc.open_recycle_bin,
    "open run dialog": wc.open_run_dialog,
    "open windows security": wc.open_windows_security,
    "open firewall": wc.open_firewall,
    "open credential manager": wc.open_credential_manager,
    "open user accounts": wc.open_user_accounts,
    "open disk cleanup": wc.open_disk_cleanup,
    "open optimize drives": wc.open_optimize_drives,

    # Windows settings
    "open settings": wc.open_settings,
    "open display settings": wc.open_display_settings,
    "open personalization settings": wc.open_personalization_settings,
    "open theme settings": wc.open_theme_settings,
    "open taskbar settings": wc.open_taskbar_settings,
    "open notification settings": wc.open_notification_settings,
    "open sound settings": wc.open_sound_settings,
    "open wifi settings": wc.open_wifi_settings,
    "open bluetooth settings": wc.open_bluetooth_settings,
    "open vpn settings": wc.open_vpn_settings,
    "open mobile hotspot settings": wc.open_mobile_hotspot_settings,
    "open battery settings": wc.open_battery_settings,
    "open storage settings": wc.open_storage_settings,
    "open clipboard settings": wc.open_clipboard_settings,
    "open mouse settings": wc.open_mouse_settings,
    "open keyboard settings": wc.open_keyboard_settings,
    "open language settings": wc.open_language_settings,
    "open date time settings": wc.open_date_time_settings,
    "open privacy settings": wc.open_privacy_settings,
    "open camera privacy settings": wc.open_camera_privacy_settings,
    "open microphone privacy settings": wc.open_microphone_privacy_settings,
    "open windows update": wc.open_windows_update,
    "open recovery settings": wc.open_recovery_settings,
    "open activation settings": wc.open_activation_settings,
    "open network connections": wc.open_network_connections,

    # Folders
    "open desktop folder": wc.open_desktop_folder,
    "open downloads": wc.open_downloads_folder,
    "open documents": wc.open_documents_folder,
    "open pictures": wc.open_pictures_folder,
    "open videos": wc.open_videos_folder,
    "open music folder": wc.open_music_folder,
    "open this pc": wc.open_this_pc,
    "open network folder": wc.open_network_folder,
    "open recent files": wc.open_recent_files,

    # Window management
    "close window": wc.close_window,
    "minimize window": wc.minimize_window,
    "maximize window": wc.maximize_window,
    "restore window": wc.restore_window,
    "switch window": wc.switch_window,
    "snap window left": wc.snap_window_left,
    "snap window right": wc.snap_window_right,
    "full screen": wc.full_screen,
    "show desktop": wc.show_desktop,
    "open task view": wc.open_task_view,
    "open start menu": wc.open_start_menu,

    # Keyboard commands
    "copy selected": wc.copy_selected,
    "paste clipboard": wc.paste_clipboard,
    "cut selected": wc.cut_selected,
    "undo action": wc.undo_action,
    "redo action": wc.redo_action,
    "select all": wc.select_all,
    "press enter": wc.press_enter,
    "press escape": wc.press_escape,
    "press tab": wc.press_tab,
    "refresh window": wc.refresh_window,

    # Mouse commands
    "left click": wc.left_click,
    "right click": wc.right_click,
    "double click": wc.double_click,
    "scroll up": wc.scroll_up,
    "scroll down": wc.scroll_down,
    "center mouse": wc.center_mouse,

    # Media commands
    "volume up": wc.volume_up,
    "volume down": wc.volume_down,
    "mute volume": wc.mute_volume,
    "unmute volume": wc.unmute_volume,
    "play pause media": wc.play_pause_media,
    "next track": wc.next_track,
    "previous track": wc.previous_track,
    "stop media": wc.stop_media,
    "open spotify": wc.open_spotify,
    "open vlc": wc.open_vlc,

    # Screen and clipboard commands
    "take screenshot": wc.take_screenshot,
    "start screen recording": wc.start_screen_recording,
    "stop screen recording": wc.stop_screen_recording,
    "read clipboard": wc.read_clipboard,
    "clear clipboard": wc.clear_clipboard,

    # Security and power commands
    "lock computer": wc.lock_computer,
    "sign out": wc.sign_out,
    "shutdown computer": wc.shutdown_computer,
    "restart computer": wc.restart_computer,
    "cancel shutdown": wc.cancel_shutdown,
    "sleep computer": wc.sleep_computer,
    "hibernate computer": wc.hibernate_computer,
    "empty recycle bin": wc.empty_recycle_bin,

    # Network commands
    "show ip address": wc.show_ip_address,
    "ping google": wc.ping_google,
    "flush dns": wc.flush_dns,
    "release ip": wc.release_ip,
    "renew ip": wc.renew_ip,
    "open speed test": wc.open_speed_test,

    # Developer apps
    "open vscode": wc.open_vscode,
    "open pycharm": wc.open_pycharm,
    "open android studio": wc.open_android_studio,

    # Defender
    "defender quick scan": wc.quick_defender_scan,
}


DANGEROUS_COMMANDS = {
    "shutdown computer",
    "restart computer",
    "sign out",
    "sleep computer",
    "hibernate computer",
    "empty recycle bin",
}



pending_confirmation: str | None = None



CODE_PATTERNS = (
    r"```",
    r"^\s*(from|import)\s+\w+",
    r"^\s*(def|class|async\s+def)\s+\w+",
    r"^\s*#include\s*[<\"]",
    r"^\s*(const|let|var|function)\s+\w+",
    r"^\s*<(!doctype|html|head|body|div|script|style)",
    r"^\s*(select|insert|update|delete|create)\s+",
    r"^\s*(public|private|protected)\s+(class|static|void)",
)




def normalize_command(command: str) -> str:

    normalized = " ".join(command.lower().strip().split())

    polite_prefixes = (
        "hey saras ",
        "okay saras ",
        "ok saras ",
        "saras ",
        "please ",
        "can you ",
        "could you ",
        "would you ",
        "will you ",
    )

    changed = True

    while changed:
        changed = False

        for prefix in polite_prefixes:
            if normalized.startswith(prefix):
                normalized = normalized[len(prefix):].strip()
                changed = True
                break

    polite_suffixes = (
        " please",
        " for me",
        " sir",
    )

    changed = True

    while changed:
        changed = False

        for suffix in polite_suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)].strip()
                changed = True
                break

    return COMMAND_ALIASES.get(normalized, normalized)




def looks_like_code(response: str) -> bool:

    if not response:
        return False

    for pattern in CODE_PATTERNS:
        if re.search(
            pattern,
            response,
            flags=re.IGNORECASE | re.MULTILINE,
        ):
            return True

    code_symbols = (
        "{",
        "}",
        "();",
        "=>",
        "__init__",
        "print(",
        "return ",
        "self.",
        "elif ",
        "except ",
    )

    symbol_count = sum(
        response.count(symbol)
        for symbol in code_symbols
    )

    return symbol_count >= 3




def open_custom_folder(value: str) -> None:

    folder_path = Path(value).expanduser()

    wc._open_path(
        folder_path,
        f"Opening {folder_path.name or value}, sir.",
    )



def execute_exact_command(command: str) -> bool:
    """
    Execute a command stored inside EXACT_COMMANDS.
    """
    function = EXACT_COMMANDS.get(command)

    if function is None:
        return False

    try:
        function()

    except Exception as error:
        print(f"Exact command error: {error}")
        speak(
            "Sorry sir, I could not execute that Windows command."
        )

    return True


# ============================================================
# VALUE COMMAND EXECUTOR
# ============================================================

def execute_value_command(command: str) -> bool:
    """
    Execute commands containing search text, file names, folder names,
    paths, songs, clipboard text, or Git repository paths.
    """
    prefixes: dict[str, Callable[[str], None]] = {
        "search google for ": wc.google_search,
        "google search ": wc.google_search,

        "search youtube for ": wc.youtube_search,
        "youtube search ": wc.youtube_search,

        "search wikipedia for ": wc.wikipedia_search,
        "wikipedia search ": wc.wikipedia_search,

        "play song ": wc.play_youtube_song,
        "play music ": wc.play_youtube_song,
        "play ": wc.play_youtube_song,

        "create folder ": wc.make_folder,
        "make folder ": wc.make_folder,

        "delete folder ": wc.delete_folder,
        "remove folder ": wc.delete_folder,

        "delete file ": wc.delete_file,
        "remove file ": wc.delete_file,

        "open folder ": open_custom_folder,

        "set clipboard ": wc.set_clipboard,
        "copy text ": wc.set_clipboard,

        "run python file ": wc.run_python_file,

        "git pull ": wc.git_pull,

        "search files for ": wc.search_files,
        "find files for ": wc.search_files,
    }

    # Check longer prefixes first.
    sorted_prefixes = sorted(
        prefixes.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for prefix, handler in sorted_prefixes:
        if not command.startswith(prefix):
            continue

        value = command[len(prefix):].strip()

        if not value:
            speak("Please provide the required value, sir.")
            return True

        try:
            handler(value)

        except Exception as error:
            print(f"Value command error: {error}")
            speak(
                "Sorry sir, I could not complete that command."
            )

        return True

    return False



def execute_mouse_command(command: str) -> bool:
    """
    Handle a command such as:
    move mouse to 500 300
    move mouse to 500, 300
    """
    if not command.startswith("move mouse to "):
        return False

    value = command.removeprefix("move mouse to ").strip()

    try:
        coordinate_parts = value.replace(",", " ").split()

        if len(coordinate_parts) < 2:
            raise ValueError("Two coordinates are required.")

        x_position = int(coordinate_parts[0])
        y_position = int(coordinate_parts[1])

        wc.move_mouse(x_position, y_position)

    except (ValueError, IndexError):
        speak(
            "Please provide valid X and Y coordinates, sir. "
            "For example, move mouse to 500 300."
        )

    except Exception as error:
        print(f"Mouse command error: {error}")
        speak("Sorry sir, I could not move the mouse.")

    return True



def request_confirmation(command: str) -> bool:
    """
    Store a dangerous command and ask the user to confirm it.
    """
    global pending_confirmation

    pending_confirmation = command

    readable_command = command.replace(" computer", "")

    speak(
        f"You requested to {readable_command}. "
        "Please say confirm to continue, or cancel to stop, sir."
    )

    return True


def handle_confirmation(command: str) -> bool:
    """
    Confirm or cancel a dangerous command.
    """
    global pending_confirmation

    confirm_commands = {
        "confirm",
        "yes confirm",
        "confirm command",
        "do it",
        "proceed",
        "yes proceed",
    }

    cancel_commands = {
        "cancel",
        "cancel command",
        "do not",
        "don't do it",
        "stop command",
        "no",
    }

    if pending_confirmation is None:
        return False

    if command in confirm_commands:
        confirmed_command = pending_confirmation
        pending_confirmation = None

        function = EXACT_COMMANDS.get(confirmed_command)

        if function is None:
            speak(
                "Sorry sir, that command is no longer available."
            )
            return True

        try:
            speak("Confirmation accepted, sir.")
            function()

        except Exception as error:
            print(f"Confirmed command error: {error}")
            speak(
                "Sorry sir, I could not execute the confirmed command."
            )

        return True

    if command in cancel_commands:
        pending_confirmation = None
        speak("Command cancelled, sir.")
        return True

    speak(
        "A command is waiting for confirmation. "
        "Please say confirm or cancel, sir."
    )
    return True


def handle_ai_response(command: str) -> bool:
    try:

        response = ask_ai(command)

        if response is None:
            speak(
                "Sorry sir, my AI brain returned no response."
            )
            return True

        response = str(response).strip()

        if not response:
            speak(
                "Sorry sir, my AI brain returned an empty response."
            )
            return True

        print(f"\nS.A.R.A.S:\n{response}\n")

        if looks_like_code(response):
            speak(
                "I have displayed the code on your screen, sir."
            )
        else:
            speak(response)

    except Exception as error:
        print(f"AI error: {error}")
        speak(
            "Sorry sir, my AI brain is currently unavailable."
        )

    return True



def run_commands(raw_command: str) -> bool:

    if not raw_command:
        speak("I did not receive a command, sir.")
        return False

    if not raw_command.strip():
        speak("I did not receive a command, sir.")
        return False

    command = normalize_command(raw_command)

    print(f"Raw command: {raw_command}")
    print(f"Normalized command: {command}")

    if pending_confirmation is not None:
        return handle_confirmation(command)

    if command == "current time":
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}, sir.")
        return True

    if command == "current date":
        current_date = datetime.now().strftime(
            "%A, %d %B %Y"
        )
        speak(f"Today is {current_date}, sir.")
        return True


    if command == "introduce yourself":
        speak(
            "I am S.A.R.A.S, the Smart Autonomous Responsive "
            "Assistant System, developed by Goutham V, a third-year "
            "BTech student specializing in Artificial Intelligence "
            "and Machine Learning. I am designed to control Windows, "
            "answer questions, automate tasks, and assist you through "
            "voice, dashboard, and mobile commands."
        )
        return True

    if command in DANGEROUS_COMMANDS:
        return request_confirmation(command)


    if execute_exact_command(command):
        return True

    if execute_value_command(command):
        return True

    if execute_mouse_command(command):
        return True

    return handle_ai_response(command)
