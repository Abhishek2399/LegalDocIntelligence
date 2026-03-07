# Legal Document Intelligence System

A backend system that processes legal and financial documents (such as Bank Guarantees) 
using OCR and AI-powered extraction. Built with FastAPI and Python.

## Tech Stack

- **Python 3.11+**
- **FastAPI** — REST API framework
- **PyMuPDF (fitz)** — Digital PDF text extraction
- **Tesseract + pytesseract** — OCR for scanned PDFs
- **Google Gemini API** — LLM for entity extraction and clause classification
- **ChromaDB** — Local vector store for RAG pipeline
- **Uvicorn** — ASGI server

## Folder Structure
```
legal-doc-intelligence/
├── app/
│   ├── api/
│   │   └── routes/          # API route handlers
│   ├── core/                # Core logic (OCR, chunking, embedding, retrieval)
│   ├── services/            # Business logic services
│   └── main.py              # FastAPI app entry point
├── vector_store/            # ChromaDB persistent storage
├── uploads/                 # Uploaded documents
├── .env                     # Environment variables (not committed)
├── requirements.txt         # Python dependencies
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.11+
- Tesseract binary installed on your system

Install Tesseract on Linux:
```bash
sudo apt install tesseract-ocr
```

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/legal-doc-intelligence.git
cd legal-doc-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## How to Run
```bash
uvicorn app.main:app --reload
```

API will be available at:
- Base URL: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

## Features (In Progress)

- [x] PDF upload and text extraction
- [ ] RAG pipeline for document Q&A
- [ ] Entity extraction from legal documents
- [ ] Clause classification
- [ ] Onerous clause detection
- [ ] BG to CRL matching

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Health check |
| POST | /document/upload | Upload and extract text from PDF |