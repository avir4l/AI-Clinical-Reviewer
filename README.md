# AI Clinical Document Reviewer

An end-to-end AI application that processes typed, scanned, and handwritten clinical documentation to generate structured clinical reports.

## Features
- Plain text, Image (PNG/JPEG), and PDF document ingestion.
- Structured clinical entity extraction (Diagnoses, Symptoms, Meds, Vitals).
- Automated clinical summary highlighting missing information and inconsistencies.
- Historical report dashboard backed by SQLite persistence.
- Decoupled API architecture.

## Tech Stack
- **Backend:** FastAPI (Python 3.10+)
- **Database:** SQLite
- **AI/ML:** Google Gemini 
- **Frontend:** HTML5, Modern JavaScript, CSS3

## Setup Instructions

### 1. Backend Setup
Navigate to the backend directory, install requirements, and run the server:
`cd backend`
`pip install -r requirements.txt`
`python -m uvicorn main:app --reload`
The API will run at `http://127.0.0.1:8000`.

### 2. Frontend Setup
Open `frontend/index.html` in any web browser.

### 3. Verification
Access the automated API documentation at `http://127.0.0.1:8000/docs`.