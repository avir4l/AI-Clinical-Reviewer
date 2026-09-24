# AI Clinical Document Reviewer

A FastAPI-based web application that leverages the Google Gemini API to analyze, structure, and synthesize raw clinical notes and medical documents into standardized clinical reports. 

**[🎥 Watch the Demo Video Here](#)** *(Link your screen recording here before submitting)*

## Features

* **LLM-Powered Clinical Synthesis:** Extracts patient demographics, reported symptoms, active medications, assessed diagnoses, and critical clinical flags from unstructured text using Gemini.
* **Multimodal Input:** Supports both raw text pasting (doctor's notes, discharge summaries) and direct file uploads (PDFs/Images).
* **Automated Audit History:** Saves all processed encounters locally via SQLite, allowing users to instantly retrieve and review past reports.
* **Integrated Clinical UI:** A responsive, zero-dependency frontend built with Vanilla JS/CSS, served directly from the FastAPI root endpoint.
* **Ngrok Ready:** Configured to easily tunnel local ports to public URLs with bypass headers for seamless remote evaluation.

## Tech Stack

* **Backend:** Python 3.14, FastAPI, Uvicorn
* **AI Integration:** `google-generativeai` (Gemini API)
* **Database:** SQLite (Local)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript

---

## Local Setup & Installation

Follow these steps to run the application on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/avir4l/murphyai.git](https://github.com/avir4l/murphyai.git)
cd murphyai
```

### 2. Install Dependencies
Ensure you have Python installed, then install the required packages:
```bash
pip install -r requirements.txt
```
*(If you are running multiple Python versions, you may need to use `python -m pip install -r requirements.txt`)*

### 3. Configure the Environment
The application requires a valid Google Gemini API key to process documents. Export the key in your terminal before starting the server.

**For Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

**For Mac/Linux:**
```bash
export GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

### 4. Start the Backend Server
Navigate to the root directory and start the Uvicorn server:
```bash
uvicorn api.index:app --port 8000
```
*(Alternatively, use `python -m uvicorn api.index:app --port 8000`)*

### 5. Access the Application
The frontend is served directly from the FastAPI backend. Open your web browser and navigate to:
```text
[http://127.0.0.1:8000](http://127.0.0.1:8000)
```

To access the interactive API documentation (Swagger UI), navigate to:
```text
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
```

---

## Optional: Remote Access via Ngrok

If you need to expose this local server to the internet for remote testing:

1. Keep the Uvicorn server running in your first terminal.
2. Open a second terminal and run:
   ```bash
   ngrok http 8000
   ```
3. Copy the generated `https://...ngrok-free.dev` URL.
4. Visit the URL in your browser. The frontend is pre-configured with the `ngrok-skip-browser-warning` header to ensure seamless API calls through the tunnel.