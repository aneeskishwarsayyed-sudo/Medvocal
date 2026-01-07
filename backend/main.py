from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# 🚨 THIS IS THE CRITICAL FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://medvocal-1.web.app"],   # Allow Firebase site ONLY
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

@app.post("/triage")
async def triage(data: Input):
    model = genai.GenerativeModel("gemini-1.5-flash")
    r = model.generate_content(f"{SYSTEM}\nPatient says: {data.text}")
    return {"result": r.text}
