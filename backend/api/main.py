from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
import wave

# Importing your logic engine
from utils.transcribe_utils import transcribe_audio
from utils.lfa_generator import generate_lfa_json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    await websocket.accept()
    
    # --- CRITICAL: SESSION MEMORY ---
    # We initialize this inside the connection but outside the loop 
    # to keep track of everything spoken during this session.
    session_transcript = "" 
    audio_buffer = b""

    try:
        while True:
            data = await websocket.receive_bytes()
            audio_buffer += data

            # Process every 3 seconds of audio
            if len(audio_buffer) >= 16000 * 2 * 3:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    with wave.open(f, 'wb') as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(16000)
                        wf.writeframes(audio_buffer)
                    temp_path = f.name
                
                audio_buffer = b""

                try:
                    # 1. Transcribe the new chunk
                    new_text = transcribe_audio(temp_path)
                    
                    if new_text.strip():
                        # 2. Add new text to the 'Memory' variable
                        session_transcript += " " + new_text
                        
                        # 3. Send raw text to UI for the live scrolling feed
                        await websocket.send_text(new_text)
                        
                        # 4. Generate the FULL package using the whole history
                        # This populates the Narrative, Indicators, and Audit
                        full_intelligence = generate_lfa_json(session_transcript)
                        
                        await websocket.send_json(full_intelligence)
                        
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
    except WebSocketDisconnect:
        print("Session ended.")
    except Exception as e:
        print(f"Error: {e}")