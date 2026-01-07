from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM = """
You are a certified emergency triage nurse AI using Emergency Severity Index (ESI).

Classify based on:
• Airway, Breathing, Circulation
• Mental status
• Severe pain, bleeding, fever, trauma

Return ONLY JSON in this exact format:

{
 "severity":"RED|YELLOW|GREEN",
 "reason":"SHORT CLINICAL JUSTIFICATION",
 "action":"CLEAR FIRST AID STEPS + WHEN TO GO HOSPITAL"
}

Rules:
RED = life-threatening
YELLOW = urgent but stable
GREEN = mild / home care
No chit chat.
"""

class Input(BaseModel):
    text: str

@app.post("/triage")
async def triage(data: Input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    r = model.generate_content(f"{SYSTEM}\nPatient says: {data.text}")
    return {"result": r.text}
