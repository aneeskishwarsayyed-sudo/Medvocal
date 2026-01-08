from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

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
    return {"status":"Med-Vocal backend running"}

@app.post("/api/triage")
async def triage(data: Input):
    model = genai.GenerativeModel("models/gemini-pro")
    r = model.generate_content(f"{SYSTEM}\nPatient says: {data.text}")
    return {"result": r.text}
