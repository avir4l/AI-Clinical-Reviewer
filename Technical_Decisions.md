# Technical Decisions and Trade-offs

## 1. Backend: FastAPI
* **Decision:** Selected FastAPI over Flask or Django.
* **Reasoning:** Native asynchronous support, automatic OpenAPI/Swagger documentation generation, and high-performance serialization for file uploads and JSON responses.

## 2. Frontend: Vanilla HTML5 / JavaScript (Decoupled)
* **Decision:** Decoupled HTML/JS over tightly coupled frameworks like Streamlit.
* **Reasoning:** Satisfies the requirement for clear architectural separation between frontend and backend while maintaining a lightweight footprint without node build step overhead.

## 3. AI Pipeline: Direct Gemini Multimodal Integration
* **Decision:** Direct native document passing over a Tesseract OCR + LLM pipeline.
* **Reasoning:** Traditional OCR pipelines degrade significantly on handwritten or noisy clinical documents. Gemini natively reads PDF and image tokens alongside text instructions, preserving layout context.

## 4. Database: SQLite
* **Decision:** SQLite via standard relational tables.
* **Reasoning:** Zero-configuration, zero-latency local relational persistence that meets report storage and retrieval requirements without external database server overhead.

## 5. Limitations & Future Roadmap
* **Current Limitation:** Single-node local storage without multi-tenant authentication.
* **Future Work:** Migrate to PostgreSQL for distributed persistence and introduce vector embeddings with pgvector for semantic retrieval across historical patient records.