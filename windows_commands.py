from __future__ import annotations

import ctypes
import os
import shutil
import socket
import subprocess
import time
import webbrowser
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

import pyautogui
import pyperclip

import webbrowser

from yt_dlp import YoutubeDL
from voice import speak


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


def _run(
    command: list[str] | str,
    *,
    shell: bool = False,
    wait: bool = False,
    admin: bool = False,
) -> bool:
    """Run a Windows command safely and report failure."""
    try:
        if admin:
            if isinstance(command, list):
                executable = command[0]
                parameters = subprocess.list2cmdline(command[1:])
            else:
                parts = command.split(maxsplit=1)
                executable = parts[0]
                parameters = parts[1] if len(parts) > 1 else ""

            result = ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                executable,
                parameters,
                None,
                1,
            )
            return result > 32

        if wait:
            subprocess.run(
                command,
                shell=shell,
                check=True,
                creationflags=CREATE_NO_WINDOW,
            )
        else:
            subprocess.Popen(
                command,
                shell=shell,
                creationflags=CREATE_NO_WINDOW,
            )
        return True

    except Exception as error:
        print(f"Command error: {error}")
        speak("Sorry sir, I could not complete that command.")
        return False


def _open_uri(uri: str, message: str) -> None:
    speak(message)
    try:
        os.startfile(uri)
    except OSError:
        _run(["explorer.exe", uri])


def _open_path(path: Path, message: str) -> None:
    speak(message)
    path.mkdir(parents=True, exist_ok=True)
    os.startfile(str(path))


def _confirm_text(prompt: str) -> bool:
    answer = input(f"{prompt} Type YES to confirm: ").strip()
    return answer == "YES"


# ---------------------------------------------------------------------------
# System power and session
# ---------------------------------------------------------------------------

def lock_computer() -> None:
    speak("Locking your computer, sir.")
    ctypes.windll.user32.LockWorkStation()


def sign_out() -> None:
    if _confirm_text("Sign out of Windows?"):
        speak("Signing you out, sir.")
        _run(["shutdown", "/l"])


def shutdown_computer(delay_seconds: int = 5) -> None:
    if _confirm_text("Shut down the computer?"):
        speak(f"Shutting down in {delay_seconds} seconds, sir.")
        _run(["shutdown", "/s", "/t", str(delay_seconds)])


def restart_computer(delay_seconds: int = 5) -> None:
    if _confirm_text("Restart the computer?"):
        speak(f"Restarting in {delay_seconds} seconds, sir.")
        _run(["shutdown", "/r", "/t", str(delay_seconds)])


def cancel_shutdown() -> None:
    speak("Cancelling the scheduled shutdown, sir.")
    _run(["shutdown", "/a"])


def sleep_computer() -> None:
    speak("Putting the computer to sleep, sir.")
    _run(
        [
            "rundll32.exe",
            "powrprof.dll,SetSuspendState",
            "0,1,0",
        ]
    )


def hibernate_computer() -> None:
    speak("Hibernating the computer, sir.")
    _run(["shutdown", "/h"])


def show_desktop() -> None:
    pyautogui.hotkey("win", "d")
    speak("Desktop displayed, sir.")


def open_start_menu() -> None:
    pyautogui.press("win")


def open_task_view() -> None:
    pyautogui.hotkey("win", "tab")


# ---------------------------------------------------------------------------
# Windows applications and administration tools
# ---------------------------------------------------------------------------

def open_notepad() -> None:
    speak("Opening Notepad, sir.")
    _run(["notepad.exe"])


def open_calculator() -> None:
    speak("Opening Calculator, sir.")
    _run(["calc.exe"])


def open_paint() -> None:
    speak("Opening Paint, sir.")
    _run(["mspaint.exe"])


def open_file_explorer() -> None:
    speak("Opening File Explorer, sir.")
    _run(["explorer.exe"])


def open_command_prompt() -> None:
    speak("Opening Command Prompt, sir.")
    _run(["cmd.exe"])


def open_powershell() -> None:
    speak("Opening PowerShell, sir.")
    _run(["powershell.exe"])


def open_windows_terminal() -> None:
    speak("Opening Windows Terminal, sir.")
    if not _run(["wt.exe"]):
        open_powershell()


def open_task_manager() -> None:
    speak("Opening Task Manager, sir.")
    _run(["taskmgr.exe"])


def open_control_panel() -> None:
    speak("Opening Control Panel, sir.")
    _run(["control.exe"])


def open_device_manager() -> None:
    speak("Opening Device Manager, sir.")
    _run(["devmgmt.msc"])


def open_disk_management() -> None:
    speak("Opening Disk Management, sir.")
    _run(["diskmgmt.msc"])


def open_services() -> None:
    speak("Opening Windows Services, sir.")
    _run(["services.msc"])


def open_system_information() -> None:
    speak("Opening System Information, sir.")
    _run(["msinfo32.exe"])


def open_system_configuration() -> None:
    speak("Opening System Configuration, sir.")
    _run(["msconfig.exe"])


def open_resource_monitor() -> None:
    speak("Opening Resource Monitor, sir.")
    _run(["resmon.exe"])


def open_performance_monitor() -> None:
    speak("Opening Performance Monitor, sir.")
    _run(["perfmon.exe"])


def open_event_viewer() -> None:
    speak("Opening Event Viewer, sir.")
    _run(["eventvwr.msc"])


def open_registry_editor() -> None:
    speak("Opening Registry Editor, sir.")
    _run(["regedit.exe"])


def open_character_map() -> None:
    speak("Opening Character Map, sir.")
    _run(["charmap.exe"])


def open_on_screen_keyboard() -> None:
    speak("Opening the on-screen keyboard, sir.")
    _run(["osk.exe"])


def open_magnifier() -> None:
    speak("Opening Magnifier, sir.")
    _run(["magnify.exe"])


def open_snipping_tool() -> None:
    speak("Opening Snipping Tool, sir.")
    _run(["snippingtool.exe"])


def open_camera() -> None:
    _open_uri("microsoft.windows.camera:", "Opening Camera, sir.")


def open_recycle_bin() -> None:
    _open_uri("shell:RecycleBinFolder", "Opening Recycle Bin, sir.")


def open_run_dialog() -> None:
    pyautogui.hotkey("win", "r")


def open_windows_security() -> None:
    _open_uri("windowsdefender:", "Opening Windows Security, sir.")


def open_firewall() -> None:
    speak("Opening Windows Defender Firewall, sir.")
    _run(["control.exe", "/name", "Microsoft.WindowsFirewall"])


def open_credential_manager() -> None:
    speak("Opening Credential Manager, sir.")
    _run(["control.exe", "/name", "Microsoft.CredentialManager"])


def open_user_accounts() -> None:
    speak("Opening User Accounts, sir.")
    _run(["control.exe", "/name", "Microsoft.UserAccounts"])


def open_disk_cleanup() -> None:
    speak("Opening Disk Cleanup, sir.")
    _run(["cleanmgr.exe"])


def open_optimize_drives() -> None:
    speak("Opening Optimize Drives, sir.")
    _run(["dfrgui.exe"])


# ---------------------------------------------------------------------------
# Windows Settings pages
# ---------------------------------------------------------------------------

def open_settings() -> None:
    _open_uri("ms-settings:", "Opening Settings, sir.")


def open_display_settings() -> None:
    _open_uri("ms-settings:display", "Opening Display Settings, sir.")


def open_personalization_settings() -> None:
    _open_uri("ms-settings:personalization", "Opening Personalization, sir.")


def open_theme_settings() -> None:
    _open_uri("ms-settings:themes", "Opening Theme Settings, sir.")


def open_taskbar_settings() -> None:
    _open_uri("ms-settings:taskbar", "Opening Taskbar Settings, sir.")


def open_notification_settings() -> None:
    _open_uri("ms-settings:notifications", "Opening Notification Settings, sir.")


def open_sound_settings() -> None:
    _open_uri("ms-settings:sound", "Opening Sound Settings, sir.")


def open_wifi_settings() -> None:
    _open_uri("ms-settings:network-wifi", "Opening Wi-Fi Settings, sir.")


def open_bluetooth_settings() -> None:
    _open_uri("ms-settings:bluetooth", "Opening Bluetooth Settings, sir.")


def open_vpn_settings() -> None:
    _open_uri("ms-settings:network-vpn", "Opening VPN Settings, sir.")


def open_mobile_hotspot_settings() -> None:
    _open_uri(
        "ms-settings:network-mobilehotspot",
        "Opening Mobile Hotspot Settings, sir.",
    )


def open_battery_settings() -> None:
    _open_uri("ms-settings:batterysaver", "Opening Battery Settings, sir.")


def open_storage_settings() -> None:
    _open_uri("ms-settings:storagesense", "Opening Storage Settings, sir.")


def open_clipboard_settings() -> None:
    _open_uri("ms-settings:clipboard", "Opening Clipboard Settings, sir.")


def open_mouse_settings() -> None:
    _open_uri("ms-settings:mousetouchpad", "Opening Mouse Settings, sir.")


def open_keyboard_settings() -> None:
    _open_uri("ms-settings:typing", "Opening Typing Settings, sir.")


def open_language_settings() -> None:
    _open_uri("ms-settings:regionlanguage", "Opening Language Settings, sir.")


def open_date_time_settings() -> None:
    _open_uri("ms-settings:dateandtime", "Opening Date and Time Settings, sir.")


def open_privacy_settings() -> None:
    _open_uri("ms-settings:privacy", "Opening Privacy Settings, sir.")


def open_camera_privacy_settings() -> None:
    _open_uri("ms-settings:privacy-webcam", "Opening Camera Privacy Settings, sir.")


def open_microphone_privacy_settings() -> None:
    _open_uri(
        "ms-settings:privacy-microphone",
        "Opening Microphone Privacy Settings, sir.",
    )


def open_windows_update() -> None:
    _open_uri("ms-settings:windowsupdate", "Opening Windows Update, sir.")


def open_recovery_settings() -> None:
    _open_uri("ms-settings:recovery", "Opening Recovery Settings, sir.")


def open_activation_settings() -> None:
    _open_uri("ms-settings:activation", "Opening Activation Settings, sir.")


def open_network_connections() -> None:
    speak("Opening Network Connections, sir.")
    _run(["ncpa.cpl"])


# ---------------------------------------------------------------------------
# Common folders
# ---------------------------------------------------------------------------

def open_desktop_folder() -> None:
    _open_path(Path.home() / "Desktop", "Opening Desktop folder, sir.")


def open_downloads_folder() -> None:
    _open_path(Path.home() / "Downloads", "Opening Downloads, sir.")


def open_documents_folder() -> None:
    _open_path(Path.home() / "Documents", "Opening Documents, sir.")


def open_pictures_folder() -> None:
    _open_path(Path.home() / "Pictures", "Opening Pictures, sir.")


def open_videos_folder() -> None:
    _open_path(Path.home() / "Videos", "Opening Videos, sir.")


def open_music_folder() -> None:
    _open_path(Path.home() / "Music", "Opening Music, sir.")


def open_this_pc() -> None:
    _open_uri("shell:MyComputerFolder", "Opening This PC, sir.")


def open_network_folder() -> None:
    _open_uri("shell:NetworkPlacesFolder", "Opening Network, sir.")


def open_recent_files() -> None:
    _open_uri("shell:Recent", "Opening Recent Files, sir.")


# ---------------------------------------------------------------------------
# File and folder operations
# ---------------------------------------------------------------------------

def make_folder(folder_path: str) -> None:
    path = Path(folder_path).expanduser()
    try:
        path.mkdir(parents=True, exist_ok=False)
        speak(f"The folder {path.name} has been created successfully, sir.")
    except FileExistsError:
        speak(f"The folder {path.name} already exists, sir.")
    except OSError as error:
        print(error)
        speak("I could not create that folder, sir.")


def delete_folder(folder_path: str) -> None:
    path = Path(folder_path).expanduser()

    if not path.exists():
        speak("That folder does not exist, sir.")
        return

    if not path.is_dir():
        speak("The selected path is not a folder, sir.")
        return

    if not _confirm_text(f"Permanently delete folder '{path}'?"):
        speak("Folder deletion cancelled, sir.")
        return

    try:
        shutil.rmtree(path)
        speak(f"The folder {path.name} has been deleted, sir.")
    except OSError as error:
        print(error)
        speak("I could not delete that folder, sir.")


def rename_path(old_path: str, new_name: str) -> None:
    source = Path(old_path).expanduser()

    if not source.exists():
        speak("The selected file or folder does not exist, sir.")
        return

    target = source.with_name(new_name)

    try:
        source.rename(target)
        speak(f"Renamed to {new_name}, sir.")
    except OSError as error:
        print(error)
        speak("I could not rename it, sir.")


def delete_file(file_path: str) -> None:
    path = Path(file_path).expanduser()

    if not path.is_file():
        speak("That file does not exist, sir.")
        return

    if not _confirm_text(f"Permanently delete file '{path}'?"):
        speak("File deletion cancelled, sir.")
        return

    try:
        path.unlink()
        speak(f"The file {path.name} has been deleted, sir.")
    except OSError as error:
        print(error)
        speak("I could not delete that file, sir.")


def copy_path(source_path: str, destination_path: str) -> None:
    source = Path(source_path).expanduser()
    destination = Path(destination_path).expanduser()

    try:
        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        elif source.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        else:
            speak("The source path does not exist, sir.")
            return

        speak("Copy completed successfully, sir.")
    except OSError as error:
        print(error)
        speak("I could not copy that item, sir.")


def move_path(source_path: str, destination_path: str) -> None:
    source = Path(source_path).expanduser()
    destination = Path(destination_path).expanduser()

    if not source.exists():
        speak("The source path does not exist, sir.")
        return

    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        speak("Move completed successfully, sir.")
    except OSError as error:
        print(error)
        speak("I could not move that item, sir.")


def compress_folder(folder_path: str, output_zip: Optional[str] = None) -> None:
    folder = Path(folder_path).expanduser()

    if not folder.is_dir():
        speak("The selected folder does not exist, sir.")
        return

    output_base = (
        str(Path(output_zip).with_suffix(""))
        if output_zip
        else str(folder)
    )

    try:
        archive = shutil.make_archive(output_base, "zip", root_dir=folder)
        speak(f"Archive created at {archive}, sir.")
    except OSError as error:
        print(error)
        speak("I could not compress that folder, sir.")


def extract_zip(zip_path: str, destination: Optional[str] = None) -> None:
    archive = Path(zip_path).expanduser()

    if not archive.is_file():
        speak("The ZIP file does not exist, sir.")
        return

    target = Path(destination).expanduser() if destination else archive.with_suffix("")

    try:
        target.mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(str(archive), str(target))
        speak(f"The archive has been extracted to {target}, sir.")
    except (OSError, shutil.ReadError) as error:
        print(error)
        speak("I could not extract that archive, sir.")


def search_files(file_name: str, root: str = str(Path.home())) -> list[str]:
    speak(f"Searching for {file_name}, sir.")
    matches: list[str] = []
    query = file_name.lower()

    for current_root, _, names in os.walk(root):
        for name in names:
            if query in name.lower():
                matches.append(str(Path(current_root) / name))
                if len(matches) >= 50:
                    return matches

    if matches:
        speak(f"I found {len(matches)} matching files, sir.")
    else:
        speak("No matching files were found, sir.")

    return matches


# ---------------------------------------------------------------------------
# Window, keyboard and mouse controls
# ---------------------------------------------------------------------------

def close_window() -> None:
    pyautogui.hotkey("alt", "f4")


def minimize_window() -> None:
    pyautogui.hotkey("win", "down")


def maximize_window() -> None:
    pyautogui.hotkey("win", "up")


def restore_window() -> None:
    pyautogui.hotkey("win", "down")


def switch_window() -> None:
    pyautogui.hotkey("alt", "tab")


def snap_window_left() -> None:
    pyautogui.hotkey("win", "left")


def snap_window_right() -> None:
    pyautogui.hotkey("win", "right")


def full_screen() -> None:
    pyautogui.press("f11")


def copy_selected() -> None:
    pyautogui.hotkey("ctrl", "c")


def paste_clipboard() -> None:
    pyautogui.hotkey("ctrl", "v")


def cut_selected() -> None:
    pyautogui.hotkey("ctrl", "x")


def undo_action() -> None:
    pyautogui.hotkey("ctrl", "z")


def redo_action() -> None:
    pyautogui.hotkey("ctrl", "y")


def select_all() -> None:
    pyautogui.hotkey("ctrl", "a")


def press_enter() -> None:
    pyautogui.press("enter")


def press_escape() -> None:
    pyautogui.press("esc")


def press_tab() -> None:
    pyautogui.press("tab")


def refresh_window() -> None:
    pyautogui.press("f5")


def left_click() -> None:
    pyautogui.click()


def right_click() -> None:
    pyautogui.rightClick()


def double_click() -> None:
    pyautogui.doubleClick()


def scroll_up(amount: int = 5) -> None:
    pyautogui.scroll(abs(amount))


def scroll_down(amount: int = 5) -> None:
    pyautogui.scroll(-abs(amount))


def move_mouse(x: int, y: int, duration: float = 0.3) -> None:
    pyautogui.moveTo(x, y, duration=duration)


def center_mouse() -> None:
    width, height = pyautogui.size()
    pyautogui.moveTo(width // 2, height // 2, duration=0.3)


# ---------------------------------------------------------------------------
# Volume and media
# ---------------------------------------------------------------------------

def volume_up(steps: int = 5) -> None:
    for _ in range(max(1, steps)):
        pyautogui.press("volumeup")


def volume_down(steps: int = 5) -> None:
    for _ in range(max(1, steps)):
        pyautogui.press("volumedown")


def mute_volume() -> None:
    pyautogui.press("volumemute")


def unmute_volume() -> None:
    # Windows uses the same media key for mute and unmute.
    pyautogui.press("volumemute")


def play_pause_media() -> None:
    pyautogui.press("playpause")


def next_track() -> None:
    pyautogui.press("nexttrack")


def previous_track() -> None:
    pyautogui.press("prevtrack")


def stop_media() -> None:
    pyautogui.press("stop")


def open_spotify() -> None:
    speak("Opening Spotify, sir.")
    try:
        os.startfile("spotify:")
    except OSError:
        _run(["explorer.exe", "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"])


def open_vlc() -> None:
    possible_paths = [
        Path(os.environ.get("ProgramFiles", "")) / "VideoLAN/VLC/vlc.exe",
        Path(os.environ.get("ProgramFiles(x86)", "")) / "VideoLAN/VLC/vlc.exe",
    ]

    for path in possible_paths:
        if path.exists():
            speak("Opening VLC Media Player, sir.")
            _run([str(path)])
            return

    speak("VLC Media Player was not found, sir.")


# ---------------------------------------------------------------------------
# Screenshot, recording and clipboard
# ---------------------------------------------------------------------------

def take_screenshot(output_path: Optional[str] = None) -> str:
    screenshots = Path.home() / "Pictures" / "SARAS Screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)

    path = (
        Path(output_path).expanduser()
        if output_path
        else screenshots / f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
    )

    image = pyautogui.screenshot()
    image.save(path)
    speak(f"Screenshot saved, sir.")
    return str(path)


def start_screen_recording() -> None:
    # Opens Xbox Game Bar recording shortcut.
    speak("Starting screen recording, sir.")
    pyautogui.hotkey("win", "alt", "r")


def stop_screen_recording() -> None:
    speak("Stopping screen recording, sir.")
    pyautogui.hotkey("win", "alt", "r")


def read_clipboard() -> str:
    text = pyperclip.paste()
    if text:
        speak(str(text))
    else:
        speak("The clipboard is empty, sir.")
    return str(text)


def clear_clipboard() -> None:
    pyperclip.copy("")
    speak("Clipboard cleared, sir.")


def set_clipboard(text: str) -> None:
    pyperclip.copy(text)
    speak("Text copied to the clipboard, sir.")


# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------

def show_ip_address() -> str:
    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        speak(f"Your local IP address is {ip_address}, sir.")
        return ip_address
    except OSError:
        speak("I could not determine the IP address, sir.")
        return ""


def ping_google() -> None:
    speak("Testing the internet connection, sir.")
    result = subprocess.run(
        ["ping", "-n", "2", "8.8.8.8"],
        capture_output=True,
        text=True,
        creationflags=CREATE_NO_WINDOW,
    )

    if result.returncode == 0:
        speak("The internet connection is working, sir.")
    else:
        speak("I could not reach the internet, sir.")


def flush_dns() -> None:
    speak("Flushing the DNS cache, sir.")
    if _run(["ipconfig", "/flushdns"], wait=True, admin=True):
        speak("DNS cache flushed successfully, sir.")


def release_ip() -> None:
    speak("Releasing the IP configuration, sir.")
    _run(["ipconfig", "/release"], admin=True)


def renew_ip() -> None:
    speak("Renewing the IP configuration, sir.")
    _run(["ipconfig", "/renew"], admin=True)


def set_wifi(enabled: bool) -> None:
    state = "enabled" if enabled else "disabled"
    action = "enable" if enabled else "disable"
    speak(f"Turning Wi-Fi {state}, sir.")
    _run(
        [
            "netsh",
            "interface",
            "set",
            "interface",
            'name="Wi-Fi"',
            f"admin={action}",
        ],
        shell=True,
        admin=True,
    )


def open_speed_test() -> None:
    speak("Opening an internet speed test, sir.")
    webbrowser.open("https://www.speedtest.net/")


# ---------------------------------------------------------------------------
# Websites and searches
# ---------------------------------------------------------------------------

def open_youtube() -> None:
    speak("Opening YouTube, sir.")
    webbrowser.open("https://www.youtube.com/")


def open_google() -> None:
    speak("Opening Google, sir.")
    webbrowser.open("https://www.google.com/")


def open_chatgpt() -> None:
    speak("Opening ChatGPT, sir.")
    webbrowser.open("https://chatgpt.com/")


def open_gmail() -> None:
    speak("Opening Gmail, sir.")
    webbrowser.open("https://mail.google.com/")


def open_github() -> None:
    speak("Opening GitHub, sir.")
    webbrowser.open("https://github.com/")


def open_instagram() -> None:
    speak("Opening Instagram, sir.")
    webbrowser.open("https://www.instagram.com/")


def open_facebook() -> None:
    speak("Opening Facebook, sir.")
    webbrowser.open("https://www.facebook.com/")


def open_wikipedia() -> None:
    speak("Opening Wikipedia, sir.")
    webbrowser.open("https://www.wikipedia.org/")

def open_discord() -> None:
    speak("Opening discord, sir")
    webbrowser.open("https://www.discord.com/")


def google_search(query: str) -> None:
    speak(f"Searching Google for {query}, sir.")
    webbrowser.open(f"https://www.google.com/search?q={quote_plus(query)}")


def youtube_search(query: str) -> None:
    speak(f"Searching YouTube for {query}, sir.")
    webbrowser.open(
        f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    )


def wikipedia_search(query: str) -> None:
    speak(f"Searching Wikipedia for {query}, sir.")
    webbrowser.open(
        f"https://en.wikipedia.org/wiki/Special:Search?search={quote_plus(query)}"
    )


def play_youtube_song(song_name: str) -> None:
    song_name = song_name.strip()

    if not song_name:
        speak("Please tell me the song name, sir.")
        return

    speak(f"Playing {song_name} on YouTube, sir.")

    search_options = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }

    try:
        with YoutubeDL(search_options) as youtube:
            search_result = youtube.extract_info(
                f"ytsearch1:{song_name}",
                download=False,
            )

        videos = search_result.get("entries", [])

        if not videos:
            speak(
                f"Sorry sir, I could not find {song_name} on YouTube."
            )
            return

        first_video = videos[0]
        video_id = first_video.get("id")

        if not video_id:
            speak(
                "Sorry sir, I could not get the YouTube video link."
            )
            return

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        webbrowser.open(video_url)

    except Exception as error:
        print(f"YouTube playback error: {error}")

        speak(
            "I could not open the first video, sir. "
            "Opening the YouTube search results instead."
        )

        youtube_search(song_name)




def _open_installed_app(name: str, candidates: list[Path]) -> None:
    for candidate in candidates:
        if candidate.exists():
            speak(f"Opening {name}, sir.")
            _run([str(candidate)])
            return

    executable = shutil.which(candidates[0].name)
    if executable:
        speak(f"Opening {name}, sir.")
        _run([executable])
        return

    speak(f"{name} was not found on this computer, sir.")


def open_vscode() -> None:
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Programs/Microsoft VS Code/Code.exe",
        Path(os.environ.get("ProgramFiles", ""))
        / "Microsoft VS Code/Code.exe",
    ]
    _open_installed_app("Visual Studio Code", candidates)


def open_pycharm() -> None:
    jetbrains = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs"
    candidates = list(jetbrains.glob("PyCharm*/bin/pycharm64.exe"))
    if not candidates:
        candidates = [
            Path(os.environ.get("ProgramFiles", ""))
            / "JetBrains/PyCharm/bin/pycharm64.exe"
        ]
    _open_installed_app("PyCharm", candidates)


def open_android_studio() -> None:
    candidates = [
        Path(os.environ.get("ProgramFiles", ""))
        / "Android/Android Studio/bin/studio64.exe",
    ]
    _open_installed_app("Android Studio", candidates)


def run_python_file(file_path: str) -> None:
    path = Path(file_path).expanduser()

    if not path.is_file():
        speak("That Python file does not exist, sir.")
        return

    speak(f"Running {path.name}, sir.")
    _run(["python", str(path)])


def git_pull(repository_path: str) -> None:
    path = Path(repository_path).expanduser()

    if not path.is_dir():
        speak("The repository folder does not exist, sir.")
        return

    speak("Pulling the latest Git changes, sir.")
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "pull"],
            capture_output=True,
            text=True,
            check=False,
        )
        print(result.stdout or result.stderr)
        if result.returncode == 0:
            speak("Git pull completed successfully, sir.")
        else:
            speak("Git pull failed, sir.")
    except FileNotFoundError:
        speak("Git is not installed or is not available in PATH, sir.")



def quick_defender_scan() -> None:
    speak("Starting a Windows Defender quick scan, sir.")
    powershell = (
        "Start-MpScan -ScanType QuickScan"
    )
    _run(["powershell.exe", "-NoProfile", "-Command", powershell], admin=True)


def empty_recycle_bin() -> None:
    if not _confirm_text("Permanently empty the Recycle Bin?"):
        speak("Recycle Bin cleanup cancelled, sir.")
        return

    speak("Emptying the Recycle Bin, sir.")
    powershell = (
        "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
    )
    _run(["powershell.exe", "-NoProfile", "-Command", powershell], wait=True)
    speak("Recycle Bin emptied, sir.")
