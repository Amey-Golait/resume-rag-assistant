# AI Resume Screening & Career Assistant

This project is a free, local resume analysis application. It lets a user upload a resume PDF and a job description PDF, then compares them to produce a match score, strengths, missing skills, improvement suggestions, interview questions, and document-based chat answers.

The first version used OpenAI for embeddings and text generation. We changed it to a fully local implementation so the project can run without a paid API key.

## What We Built

- A FastAPI backend for document upload, indexing, analysis, matching, and chat.
- A Streamlit frontend with dashboard, resume analysis, chat assistant, and about pages.
- PDF validation and text extraction using `pypdf`.
- Local text chunking, local embeddings, and ChromaDB vector search.
- Resume-to-job match scoring using local keyword overlap.
- Source citations from the stored document chunks.
- No OpenAI API key required.

## Tech Stack

| Area | Technology |
| --- | --- |
| Backend | FastAPI, Python |
| Frontend | Streamlit |
| PDF Parsing | pypdf |
| Vector Database | ChromaDB |
| Embeddings | Local hashing-based embeddings |
| Analysis | Local Python keyword matching |
| API Client | httpx |

## Project Structure

```text
resume-rag-assistant/
├── app/
│   ├── main.py
│   ├── requirements.txt
│   ├── uploads/
│   ├── vectorstore/
│   └── services/
│       ├── analysis.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── indexing.py
│       ├── match.py
│       ├── pdf_extract.py
│       ├── pdf_upload.py
│       ├── rag.py
│       ├── text_analysis.py
│       └── vectorstore.py
├── frontend/
│   ├── streamlit_app.py
│   ├── requirements.txt
│   ├── config.py
│   ├── state.py
│   ├── api/
│   │   └── client.py
│   └── components/
│       ├── about.py
│       ├── analysis_page.py
│       ├── analysis_results.py
│       ├── chat.py
│       ├── dashboard.py
│       ├── hero.py
│       ├── sidebar.py
│       ├── styles.py
│       └── uploads.py
└── README.md
```

## How The App Works

1. User uploads a resume PDF.
2. Backend validates that the file is a real PDF.
3. Backend saves the PDF with a UUID-based filename.
4. Text is extracted from the PDF using `pypdf`.
5. Text is split into overlapping chunks.
6. Each chunk is converted into a local vector embedding.
7. Chunks and embeddings are stored in ChromaDB.
8. User uploads or pastes a job description.
9. The app compares resume terms against job description terms.
10. The app shows match score, strengths, missing skills, suggestions, interview questions, and citations.
11. The chat assistant searches relevant chunks and returns document-based answers.

## Main Backend Files

### `app/main.py`

This is the FastAPI entry point.

Important endpoints:

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Checks if backend is running |
| `POST /upload/resume` | Uploads and indexes a resume PDF |
| `POST /upload/job` | Uploads and indexes a job description PDF |
| `POST /analyze` | Compares one resume with a job description |
| `POST /match` | Returns match result for resume/job |
| `POST /ask` | Answers questions using uploaded documents |
| `GET /job-text/{filename}` | Extracts text from an uploaded job PDF |

### `app/services/pdf_upload.py`

Validates uploaded files:

- Filename must exist.
- File must end with `.pdf`.
- File bytes must start with PDF magic bytes.
- `pypdf` must be able to read the PDF.
- File is saved with a UUID prefix to avoid name conflicts.

### `app/services/pdf_extract.py`

Extracts text from each PDF page and joins all readable text together.

### `app/services/chunking.py`

Splits long text into smaller chunks.

Current defaults:

- Chunk size: `1000` characters
- Overlap: `200` characters

The overlap helps keep context between nearby chunks.

### `app/services/embeddings.py`

Creates free local embeddings.

Instead of OpenAI embeddings, this file:

- Tokenizes text.
- Hashes each token into one of `384` vector positions.
- Counts token frequency.
- Normalizes the vector.

This gives us a simple vector representation that ChromaDB can search using cosine similarity.

### `app/services/vectorstore.py`

Handles ChromaDB storage and search.

It creates or loads collections and stores:

- Chunk text
- Embeddings
- Source filename
- Chunk index

We use `upsert` instead of `add`, so re-indexing the same source does not crash because of duplicate IDs.

### `app/services/indexing.py`

Connects the document pipeline:

```text
PDF -> extracted text -> chunks -> embeddings -> ChromaDB
```

It stores resumes in the `resumes` collection and job descriptions in the `jobs` collection.

### `app/services/text_analysis.py`

This is the local analysis engine.

It:

- Tokenizes resume and job description text.
- Removes common stopwords.
- Detects common technical skills.
- Finds matched job terms.
- Finds missing job terms.
- Calculates match percentage.
- Builds strengths.
- Builds weaknesses.
- Builds improvement suggestions.
- Builds interview questions.

### `app/services/analysis.py`

Loads the selected resume PDF, compares it with the job description, and returns the full analysis result.

### `app/services/rag.py`

Implements the local chat assistant.

It:

- Embeds the user question locally.
- Searches resume and job chunks from ChromaDB.
- Selects relevant sentences from matching chunks.
- Returns an answer with sources.

This is a simple extractive RAG approach. It does not invent new text like an LLM; it tries to answer from the uploaded documents.

## Main Frontend Files

### `frontend/streamlit_app.py`

Main Streamlit app entry point.

It:

- Sets page config.
- Applies custom CSS.
- Initializes session state.
- Checks backend health.
- Renders selected page from sidebar navigation.

### `frontend/api/client.py`

Frontend API client using `httpx`.

It calls:

- Backend health check
- Resume upload
- Job upload
- Analyze
- Ask/chat

### `frontend/components/uploads.py`

Shows two upload cards:

- Resume PDF
- Job description PDF

It also lets the user paste a job description manually.

### `frontend/components/analysis_page.py`

Main analysis workflow:

1. Show hero section.
2. Show upload section.
3. Enable `Analyze Resume` button only when resume and job description are ready.
4. Call backend analysis endpoint.
5. Show analysis results.
6. Show embedded chat assistant.

### `frontend/components/analysis_results.py`

Displays:

- Match percentage
- Summary
- Strengths
- Weaknesses
- Missing skills
- Improvement suggestions
- Interview questions
- Source citations

### `frontend/components/chat.py`

Shows chat history, sends questions to backend, and displays answers with citations.

## What We Changed To Make It Free

Originally, the app depended on OpenAI:

- OpenAI embeddings
- GPT-based resume analysis
- GPT-based chat answers
- `OPENAI_API_KEY`

We removed that dependency.

Current free/local approach:

- `embeddings.py` creates local hash-based embeddings.
- `text_analysis.py` creates match score and feedback locally.
- `rag.py` answers by extracting relevant sentences from stored chunks.
- Frontend text now says local RAG instead of OpenAI.
- The app no longer needs `OPENAI_API_KEY`.

This makes the project easier to run in interviews, demos, and college/resume submissions because it has no paid service dependency.

## Commands To Run The Project

Run these commands from the project root:

```bash
cd /Users/amee/resume-rag-assistant
```

### 1. Create Backend Virtual Environment

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Backend

```bash
cd /Users/amee/resume-rag-assistant/app
source .venv/bin/activate
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

### 3. Create Frontend Virtual Environment

Open a second terminal:

```bash
cd /Users/amee/resume-rag-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r frontend/requirements.txt
```

### 4. Start Frontend

```bash
cd /Users/amee/resume-rag-assistant
source .venv/bin/activate
streamlit run frontend/streamlit_app.py
```

Frontend URL is usually:

```text
http://localhost:8501
```

## Clean Vector Store If Needed

If ChromaDB gives an error after changing embedding logic, clear the vector store and upload documents again:

```bash
rm -rf /Users/amee/resume-rag-assistant/app/vectorstore/*
touch /Users/amee/resume-rag-assistant/app/vectorstore/.gitkeep
```

## API Test Commands

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Upload Resume

```bash
curl -X POST http://127.0.0.1:8000/upload/resume \
  -F "file=@/path/to/resume.pdf"
```

### Upload Job Description

```bash
curl -X POST http://127.0.0.1:8000/upload/job \
  -F "file=@/path/to/job-description.pdf"
```

### Analyze Resume

Replace `resume_filename_from_upload.pdf` with the filename returned from upload.

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume_filename": "resume_filename_from_upload.pdf",
    "job_description": "Python FastAPI Streamlit SQL developer role"
  }'
```

### Ask A Question

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What skills does this resume show?"
  }'
```

## Interview Explanation

You can explain the project like this:

> I built a resume screening and career assistant using FastAPI and Streamlit. The app accepts resume and job description PDFs, extracts text using pypdf, chunks the text, creates local vector embeddings, and stores them in ChromaDB. Then it compares the resume against the job description using local keyword and skill matching. It returns a match percentage, strengths, missing skills, resume improvement suggestions, interview questions, and source citations. I originally had OpenAI-based embeddings and analysis, but I converted the project to a free local RAG approach so it can run without any paid API key.

## Important Design Decisions

### Why FastAPI?

FastAPI is lightweight, fast, and easy to expose as an API. It also gives automatic validation through Pydantic models.

### Why Streamlit?

Streamlit is good for quickly building data and AI-style applications with Python. It let us build upload screens, analysis views, and chat UI quickly.

### Why ChromaDB?

ChromaDB stores document chunks as vectors and lets us retrieve the most relevant chunks for a question or job description.

### Why Local Embeddings?

Because this is a free resume project. Local embeddings remove the need for OpenAI or any paid service.

### Why Chunking?

Large PDFs are difficult to search as one block of text. Chunking creates smaller searchable parts, which improves retrieval and source citations.

### Why Source Citations?

Citations show which chunk of the resume or job description was used. This makes the answer more trustworthy and easier to explain.

## Limitations

- The local analysis is keyword-based, so it is not as intelligent as a large language model.
- It may miss synonyms. For example, it may not always know that "JS" and "JavaScript" are related.
- Chat answers are extractive, meaning they come from matching document sentences.
- PDF extraction quality depends on how readable the PDF text is.
- Scanned image-only PDFs may not work unless OCR is added.

## Future Improvements

- Add OCR support for scanned resumes.
- Add better synonym handling for technical skills.
- Add downloadable PDF reports.
- Add user authentication.
- Add resume history and delete buttons.
- Add charts for skill match and gap analysis.
- Add unit tests for upload, chunking, embeddings, and analysis.
- Add Docker setup for easier deployment.

## Troubleshooting

### Backend is offline in Streamlit

Start the backend:

```bash
cd /Users/amee/resume-rag-assistant/app
source .venv/bin/activate
uvicorn main:app --reload
```

### Upload fails

Check:

- File is a PDF.
- PDF is not corrupted.
- Backend is running.
- Dependencies are installed.

### ChromaDB embedding error

Clear the vector store:

```bash
rm -rf /Users/amee/resume-rag-assistant/app/vectorstore/*
touch /Users/amee/resume-rag-assistant/app/vectorstore/.gitkeep
```

Then upload resume and job description again.

### Frontend cannot connect to backend

Make sure backend is running at:

```text
http://127.0.0.1:8000
```

If backend is running on a different URL, set:

```bash
export API_BASE_URL="http://127.0.0.1:8000"
streamlit run frontend/streamlit_app.py
```

## Short Resume Bullet Points

- Built a local RAG-based resume screening assistant using FastAPI, Streamlit, ChromaDB, and pypdf.
- Implemented PDF upload, validation, text extraction, chunking, local embeddings, vector search, and source citations.
- Developed local resume-job matching that returns match score, strengths, missing skills, suggestions, and interview questions.
- Removed paid OpenAI dependency and converted the system to a free local analysis pipeline.
# resume-rag-assistant
