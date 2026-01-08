from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Configure CORS for your Firebase frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://medvocal-1.web.app",
        "https://medvocal-1.firebaseapp.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini with your Environment Variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM = """
You are a certified emergency triage nurse AI using Emergency Severity Index (ESI).

Return ONLY JSON:
{
 "severity":"RED|YELLOW|GREEN",
 "reason":"SHORT CLINICAL JUSTIFICATION",
 "action":"CLEAR FIRST AID STEPS + WHEN TO GO HOSPITAL"
}
"""

class Input(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "Med-Vocal backend running"}

async def get_triage_response(user_text: str):
    try:
        # Changed 'models/gemini-pro' to 'gemini-1.5-flash' to fix the 404 error
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"{SYSTEM}\nPatient says: {user_text}"
        r = model.generate_content(prompt)
        return {"result": r.text}
    except Exception as e:
        # This catches errors (like API issues) and returns a 500 status with the message
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/triage")
async def triage(data: Input):
    return await get_triage_response(data.text)

@app.post("/triage")
async def triage_alias(data: Input):
    return await get_triage_response(data.text)