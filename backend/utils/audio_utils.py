# backend/utils/audio_utils.py

import os
from pydub import AudioSegment
import wave
import contextlib

# ------------------------------
# Convert WEBM audio to WAV
# ------------------------------
def convert_webm_to_wav(input_path: str, output_path: str):
    """
    Converts a .webm audio file to .wav format.
    Requires pydub and ffmpeg installed in the system.
    """
    try:
        audio = AudioSegment.from_file(input_path, format="webm")
        audio.export(output_path, format="wav")
        print(f"Converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {input_path} to WAV: {e}")
        raise e

# ------------------------------
# Get duration of a WAV file (in seconds)
# ------------------------------
def get_wav_duration(file_path: str) -> float:
    """
    Returns the duration of a WAV file in seconds.
    """
    try:
        with contextlib.closing(wave.open(file_path,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        return 0.0

# ------------------------------
# Optional: Normalize WAV audio
# ------------------------------
def normalize_wav(input_path: str, output_path: str):
    """
    Normalizes the audio volume of a WAV file.
    """
    try:
        audio = AudioSegment.from_wav(input_path)
        normalized_audio = audio.apply_gain(-audio.max_dBFS)
        normalized_audio.export(output_path, format="wav")
        print(f"Normalized WAV saved at {output_path}")
    except Exception as e:
        print(f"Error normalizing WAV {input_path}: {e}")
        raise e

# ------------------------------
# Optional: Delete a file safely
# ------------------------------
def safe_delete(file_path: str):
    """
    Deletes a file if it exists.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
