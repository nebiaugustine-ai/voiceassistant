import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from gtts import gTTS  

load_dotenv()

router = APIRouter()

@router.get("/voice_assistant")
def voice_assistant(chat_input: str):
    # Initializes the Gemini Client
    client = genai.Client()
    
    system_prompt = """
    You are a helpful voice assistant.
    Reply naturally and very briefly (1-2 sentences maximum) because your response will be read out loud.
    """
    
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=chat_input,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7
        )
    )
    
    ai_text_response = response.text
    
    
    tts = gTTS(text=ai_text_response, lang='en', tld='com')
    
   
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    
    return StreamingResponse(audio_buffer, media_type="audio/mp3")