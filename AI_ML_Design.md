# AI/ML Design Documentation

## 1. Models & Services Used
* **Model:** Google Gemini Base via the official `google-generativeai` SDK.
* **Architecture:** Multimodal Document Pipeline with zero-shot clinical schema enforcement.

## 2. Document Processing & Ingestion Pipeline
* **Text Input:** Ingested directly as structured prompt context.
* **Image & PDF Documents:** Ingested via native multimodal bytes transmission, bypassing brittle traditional OCR pipelines. The model processes typed, scanned, and handwritten synthetic notes directly.

## 3. Structured Output Generation
* A rigorous system prompt enforces deterministic JSON output adhering to the required clinical review schema.
* Extracted components include Report Summary, Patient Details, Symptoms, Diagnoses, Medications, Vitals, Allergies, Missing Data, and Inconsistencies.

## 4. Handling Incomplete & Uncertain Information
* The model is explicitly instructed not to hallucinate missing data.
* If critical parameters (such as dosage, vital ranges, or baseline lab results) are omitted or illegible, they are populated into the `missing_information` and `requires_review` arrays.

## 5. Failure Mitigation & Error Handling
* JSON parsing errors and API limits trigger standardized HTTP status codes (400 for bad input, 502 for external provider issues).
* Frontend displays clear, non-technical explanations of failures.