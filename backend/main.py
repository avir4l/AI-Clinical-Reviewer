import os
import json
import sqlite3
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

app = FastAPI(title="AI Clinical Document Reviewer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "clinical_reports.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            filename TEXT,
            status TEXT NOT NULL,
            report_summary TEXT,
            detailed_report TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- PASTE YOUR AQ KEY HERE ---
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# Auto-detect the correct model name for your specific key
def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"--- SUCCESS: Auto-detected model {m.name} ---")
                return m.name
    except Exception as e:
        print(f"Model detection failed: {e}")
    return "gemini-1.5-flash" # Fallback if detection fails

MODEL_NAME = get_working_model()

SYSTEM_PROMPT = """
You are an AI clinical document reviewer. Analyze the provided text or document.
Extract the data into ONLY a raw JSON object matching this schema exactly:
{
  "report_summary": "Concise overview of concerns, symptoms, diagnoses, and vitals.",
  "patient_information": {"name": null, "age": null, "gender": null, "id": null},
  "symptoms": [],
  "diagnoses": [],
  "medications": [{"name": "", "dosage": "", "frequency": ""}],
  "vitals": {"blood_pressure": null, "heart_rate": null, "respiratory_rate": null, "temperature": null, "oxygen_saturation": null},
  "allergies": [],
  "clinical_observations": [],
  "clinical_concerns": [],
  "missing_information": [],
  "potential_inconsistencies": [],
  "requires_review": []
}
Return ONLY valid JSON. Do not include markdown formatting ticks.
"""

@app.post("/upload")
async def analyze_document(
    text_input: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    if not text_input and not file:
        raise HTTPException(status_code=400, detail="Please provide notes or upload a file.")

    filename = "Text Input"
    contents = [SYSTEM_PROMPT]

    if text_input:
        contents.append(f"Clinical Notes:\n{text_input}")

    if file:
        filename = file.filename
        file_bytes = await file.read()
        contents.append({
            "mime_type": file.content_type,
            "data": file_bytes
        })

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(contents)
        raw_text = response.text.strip()

        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        parsed_report = json.loads(raw_text.strip())

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI API Error: {str(e)}")

    summary = parsed_report.get("report_summary", "Summary unavailable")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO reports (timestamp, filename, status, report_summary, detailed_report) VALUES (?, ?, ?, ?, ?)",
        (timestamp, filename, "Completed", summary, json.dumps(parsed_report))
    )
    report_id = c.lastrowid
    conn.commit()
    conn.close()

    return {
        "id": report_id,
        "timestamp": timestamp,
        "status": "Completed",
        "report": parsed_report
    }

@app.get("/reports")
async def get_previous_reports():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, timestamp, filename, status, report_summary, detailed_report FROM reports ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "timestamp": r[1],
            "filename": r[2],
            "status": r[3],
            "report_summary": r[4],
            "detailed_report": json.loads(r[5])
        })
    return results