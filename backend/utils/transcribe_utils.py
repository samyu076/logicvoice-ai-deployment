import whisper
import os
import torch

# Load 'base' for balance of speed/accuracy. Use device="cuda" if you have an NVIDIA GPU.
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

def transcribe_audio(file_path):
    """
    High-accuracy local transcription.
    The prompt ensures the AI hears domain-specific NGO terms correctly.
    """
    context_prompt = "NGO project, beach clean-up, recycling units, municipality, panchayat, volunteers, LFA."
    
    result = model.transcribe(
        file_path, 
        initial_prompt=context_prompt,
        language="en",
        fp16=False # Required for CPU stability
    )
    return result["text"]