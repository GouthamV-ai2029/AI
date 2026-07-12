from __future__ import annotations

import asyncio
import os
import queue
import tempfile
import threading
import time
import wave
from pathlib import Path

import edge_tts
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from playsound import playsound


# ============================================================
# VOICE CONFIGURATION
# ============================================================

VOICE = "en-US-AvaMultilingualNeural"

SAMPLE_RATE = 16000
CHANNELS = 1

# Stop recording after this many seconds of silence.
SILENCE_DURATION = 1.5

# Maximum time one command can record.
MAX_RECORDING_DURATION = 15

# Ignore audio quieter than this value.
# Increase if background noise triggers recording.
# Decrease if your voice is not detected.
SILENCE_THRESHOLD = 500

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"

TEMP_DIR.mkdir(exist_ok=True)

SPEECH_FILE = TEMP_DIR / "saras_voice.mp3"
MIC_FILE = TEMP_DIR / "microphone_input.wav"


# ============================================================
# WHISPER MODEL
# ============================================================

print("Loading speech recognition model...")

whisper_model = WhisperModel(
    "base.en",
    device="cpu",
    compute_type="int8",
)

print("Speech recognition model loaded.")


# ============================================================
# SPEAK FUNCTION
# ============================================================

async def _generate_speech(text: str) -> None:
    """
    Generate speech using Microsoft Edge TTS.
    """
    communicator = edge_tts.Communicate(
        text=text,
        voice=VOICE,
    )

    await communicator.save(str(SPEECH_FILE))


def _run_async_function(coroutine) -> None:
    """
    Run an asynchronous function safely, even if an event loop
    is already active.
    """
    try:
        asyncio.run(coroutine)

    except RuntimeError:
        new_loop = asyncio.new_event_loop()

        try:
            new_loop.run_until_complete(coroutine)

        finally:
            new_loop.close()


def speak(text: object) -> None:
    """
    Convert text into speech and print it in the terminal.
    """
    if text is None:
        return

    message = str(text).strip()

    if not message:
        return

    print(f"S.A.R.A.S: {message}")

    try:
        if SPEECH_FILE.exists():
            SPEECH_FILE.unlink()

        _run_async_function(_generate_speech(message))

        if SPEECH_FILE.exists():
            playsound(str(SPEECH_FILE))

    except Exception as error:
        print(f"Speak error: {error}")

    finally:
        try:
            if SPEECH_FILE.exists():
                SPEECH_FILE.unlink()

        except PermissionError:
            pass


# ============================================================
# MICROPHONE RECORDING
# ============================================================

def _calculate_volume(audio_data: np.ndarray) -> float:
    """
    Calculate the average volume level of an audio block.
    """
    if audio_data.size == 0:
        return 0.0

    audio_float = audio_data.astype(np.float32)

    return float(
        np.sqrt(
            np.mean(
                np.square(audio_float)
            )
        )
    )


def _save_audio(
    filename: Path,
    audio_data: np.ndarray,
) -> None:
    """
    Save recorded microphone audio as a WAV file.
    """
    with wave.open(str(filename), "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data.astype(np.int16).tobytes())


def record_microphone() -> Path | None:
    """
    Record one voice command.

    Recording starts when speech is detected and stops after
    a short period of silence.
    """
    audio_queue: queue.Queue[np.ndarray] = queue.Queue()
    recorded_chunks: list[np.ndarray] = []

    speech_started = False
    silence_started_at: float | None = None

    recording_started_at = time.time()

    def microphone_callback(
        input_data: np.ndarray,
        frames: int,
        time_info,
        status,
    ) -> None:
        if status:
            print(f"Microphone status: {status}")

        audio_queue.put(input_data.copy())

    print("Listening...")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            callback=microphone_callback,
            blocksize=1024,
        ):
            while True:
                current_time = time.time()

                if (
                    current_time - recording_started_at
                    >= MAX_RECORDING_DURATION
                ):
                    break

                try:
                    audio_chunk = audio_queue.get(timeout=0.5)

                except queue.Empty:
                    continue

                volume = _calculate_volume(audio_chunk)

                if not speech_started:
                    if volume >= SILENCE_THRESHOLD:
                        speech_started = True
                        silence_started_at = None
                        recorded_chunks.append(audio_chunk)

                        print("Speech detected...")

                else:
                    recorded_chunks.append(audio_chunk)

                    if volume < SILENCE_THRESHOLD:
                        if silence_started_at is None:
                            silence_started_at = current_time

                        elif (
                            current_time - silence_started_at
                            >= SILENCE_DURATION
                        ):
                            break

                    else:
                        silence_started_at = None

    except Exception as error:
        print(f"Microphone error: {error}")
        return None

    if not speech_started or not recorded_chunks:
        print("No speech detected.")
        return None

    complete_audio = np.concatenate(
        recorded_chunks,
        axis=0,
    )

    try:
        _save_audio(
            MIC_FILE,
            complete_audio,
        )

    except Exception as error:
        print(f"Audio save error: {error}")
        return None

    return MIC_FILE


# ============================================================
# TRANSCRIPTION
# ============================================================

def transcribe_audio(audio_file: Path) -> str | None:
    """
    Convert the recorded WAV file into text using Faster Whisper.
    """
    try:
        segments, information = whisper_model.transcribe(
            str(audio_file),
            language="en",
            beam_size=5,
            vad_filter=True,
            vad_parameters={
                "min_silence_duration_ms": 500,
            },
        )

        transcript_parts: list[str] = []

        for segment in segments:
            segment_text = segment.text.strip()

            if segment_text:
                transcript_parts.append(segment_text)

        command = " ".join(transcript_parts).strip()

        if not command:
            print("No understandable speech detected.")
            return None

        return command

    except Exception as error:
        print(f"Transcription error: {error}")
        return None


# ============================================================
# LISTEN FUNCTION
# ============================================================

def listen() -> str | None:
    """
    Listen through the microphone and return recognized text.
    """
    audio_file = record_microphone()

    if audio_file is None:
        return None

    try:
        command = transcribe_audio(audio_file)

        if not command:
            return None

        command = command.lower().strip()

        print(f"You said: {command}")

        return command

    finally:
        try:
            if MIC_FILE.exists():
                MIC_FILE.unlink()

        except PermissionError:
            pass
