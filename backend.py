from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import uuid
from TTS.api import TTS
import os

app = FastAPI()

# Load Hindi model
tts = TTS(model_name="tts_models/hi/in/vits")

class TextRequest(BaseModel):
    text: str

@app.post("/generate_audio")
async def generate_audio(req: TextRequest):
    filename = f"{uuid.uuid4()}.wav"
    tts.tts_to_file(text=req.text, file_path=filename)
    response = FileResponse(filename, media_type="audio/wav", filename="voice.wav")

    @response.call_on_close
    def cleanup():
        if os.path.exists(filename):
            os.remove(filename)

    return response
