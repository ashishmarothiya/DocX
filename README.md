#  Document Intelligence Engine

A production-oriented AI Document Intelligence Engine built with **FastAPI**, **Computer Vision**, **Vector Databases**, and modern **AI/NLP techniques**.

<p align="center">
  <a href="https://github.com/ashishmarothiya/DocX/actions/workflows/ci-cd.yml"><img src="https://github.com/ashishmarothiya/DocX/actions/workflows/ci-cd.yml/badge.svg" alt="CI/CD Pipeline"></a>
  <a href="Dockerfile"><img src="https://img.shields.io/badge/Docker-Multi--Container-2496ED?logo=docker&logoColor=white" alt="Docker"></a>
  <a href="https://github.com/ashishmarothiya/DocX/pkgs/container/docx%2Fbackend"><img src="https://img.shields.io/badge/GitHub_Packages-GHCR-blue?logo=github" alt="GitHub Packages"></a>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.138.1-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18.3-61DAFB?logo=react&logoColor=react" alt="React">
  <img src="https://img.shields.io/badge/Qdrant-Vector_DB-DC244C?logo=qdrant&logoColor=white" alt="Qdrant">
  <img src="https://img.shields.io/badge/PaddleOCR-OCR-00A5E0?logo=paddlepaddle&logoColor=white" alt="PaddleOCR">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/CI%2FCD-Automated-success?logo=githubactions&logoColor=white" alt="CI/CD Status">
  <img src="https://img.shields.io/badge/Status-Production_Ready-green" alt="Project Status">
  <img src="https://img.shields.io/badge/Architecture-Modular_Microservices-blue" alt="Architecture">
  <img src="https://img.shields.io/badge/Focus-AI_Engineering_%26_MLOps-purple" alt="AI Engineering & MLOps">
</p>

The system is designed to ingest, process, understand, and retrieve information from PDF and image documents using OCR, document classification, semantic chunking, vector embeddings, and Qdrant.

The project is being developed as a backend-focused **AI Engineering portfolio project**, with a strong emphasis on modular architecture, separation of concerns, containerization, and production-oriented design.

---


#  Project Goal

Build a scalable AI backend capable of:

* Uploading PDF and image documents
* Validating uploaded files
* Detecting document types automatically
* Extracting text from digital PDFs
* Performing OCR on scanned documents and images
* Classifying documents before processing
* Cleaning and preprocessing extracted text
* Splitting documents into semantic chunks
* Generating vector embeddings
* Storing embeddings in a Vector Database
* Semantic Search
* Retrieval-Augmented Generation (RAG)
* Question Answering over documents
* Document Summarization
* Structured JSON extraction

---

#  Tech Stack

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

## AI & Document Processing

* PyMuPDF
* PaddleOCR
* Sentence Transformers
* BAAI/bge-small-en-v1.5
* OpenAI API *(Planned)*

## Vector Database

* Qdrant
* qdrant-client

## Infrastructure

* Docker
* Docker Compose
* PostgreSQL *(Planned)*
* Redis *(Planned)*

---

#  Project Structure

```text
document-intelligence-engine/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml                # Automated CI/CD Pipeline (Lint, Test, Docker Build & GHCR)
│
├── app/                             # FastAPI Backend Application
│   ├── api/                         # API Routers (/health, /upload, /search, /ask)
│   ├── core/                        # Core Application Settings & Config
│   ├── models/                      # Domain & Data Models
│   ├── pipelines/                   # Ingestion & Document Processing Pipelines
│   ├── schemas/                     # Pydantic Request & Response Schemas
│   ├── services/                    # Business Logic (OCR, Chunking, Embeddings, Qdrant, RAG)
│   ├── utils/                       # Utility Helpers
│   └── main.py                      # FastAPI App Entrypoint & CORS Config
│
├── docx-frontend/                   # Modern React (Vite) User Interface
│   ├── src/                         # React UI Components & Styles
│   ├── Dockerfile                   # Multi-Stage Frontend Dockerfile (Vite + Nginx)
│   ├── nginx.conf                   # Nginx Reverse Proxy & Routing
│   ├── package.json                 # Frontend Dependencies
│   └── vite.config.js               # Vite Configuration
│
├── tests/                           # Automated Test Suite (Pytest)
│   ├── conftest.py                  # Test Fixtures & Mocks
│   ├── test_health.py               # Health Check & Root Route Tests
│   ├── test_api_upload.py           # Upload Validation Tests
│   ├── test_services.py             # TextCleaner, Chunking, Classifier Tests
│   ├── test_schemas.py              # Pydantic Schema Validation Tests
│   └── test_ocr.py                  # OCR Extraction Tests
│
├── data/
│   └── uploads/                     # Document Upload Directory
│
├── Dockerfile                       # Production Backend Dockerfile (Python 3.11)
├── docker-compose.yml               # Multi-Container Compose (Frontend, API, Qdrant)
├── .dockerignore                    # Optimized Docker Build Context
├── pytest.ini                       # Pytest Configuration
├── requirements.txt                 # Production Dependencies
├── requirements-dev.txt             # Development & Testing Dependencies
├── .env.example                     # Environment Variable Template
└── README.md                        # Project Documentation
```

---

#  Document Processing Workflow

The current ingestion pipeline follows this flow:

```text
Upload Document
        │
        ▼
Validate File Type
        │
        ▼
Save File
        │
        ▼
Detect File Type
        │
        ▼
Document Pipeline
        │
        ├──────────────────────┐
        ▼                      ▼
   PDF Pipeline          Image Pipeline
        │                      │
        ▼                      ▼
PDF Text Extraction      PaddleOCR
        │                      │
        ▼                      │
Document Classification        │
        │                      │
   ┌────┴────┐                 │
   ▼         ▼                 │
  Text       OCR               │
   │         │                 │
   └────┬────┘─────────────────┘
        ▼
   Text Cleaning
        │
        ▼
      Chunking
        │
        ▼
BGE Embedding Generation
        │
        ▼
      Qdrant
        │
        ▼
  Vector Storage
```

---

# ✅ Features Implemented

## Backend Foundation

* FastAPI application
* Modular project architecture
* API routing
* Swagger / OpenAPI documentation
* Pydantic schemas
* Service-based architecture
* Pipeline-based document processing

---

##  File Upload

* PDF upload
* PNG upload
* JPG upload
* JPEG upload
* File type validation
* UUID-based file naming
* Automatic file storage

---

##  Document Processing

* Document Processing Pipeline
* File Type Detection
* Pipeline Routing
* Processing Orchestrator
* Unified Document Data Model

---

##  PDF Processing

* PDF text extraction using PyMuPDF
* Multi-page traversal
* Character counting
* Empty document detection
* Text preview generation

---

##  OCR Processing

* PaddleOCR integration
* OCR Service
* Image text extraction
* Scanned PDF processing
* OCR decision engine

The system determines whether a PDF already contains extractable text or requires OCR.

```text
PDF
 │
 ▼
Extract Text
 │
 ▼
Classify Document
 │
 ├── Text Available ──► Continue
 │
 └── OCR Required ────► PaddleOCR
```

---

##  Text Processing

* Text cleaning
* Smart text chunking
* Overlapping chunks
* Chunk metadata

---

##  Embedding Generation

* Sentence Transformers
* BAAI/bge-small-en-v1.5
* 384-dimensional embeddings
* Normalized embeddings
* Embedding data model

Current embedding flow:

```text
Document
    │
    ▼
Text Chunks
    │
    ▼
BGE-small-en-v1.5
    │
    ▼
384-dimensional Vectors
```

---

#  Qdrant Vector Storage

Qdrant has now been integrated into the document processing pipeline.

The system creates a Qdrant collection named:

```text
documents
```

with:

```text
Vector Size: 384
Distance: Cosine
```

Each document chunk is stored as a Qdrant Point containing:

```text
Point
│
├── ID
│
├── Vector
│   └── 384 dimensions
│
└── Payload
    ├── text
    ├── chunk_index
    ├── page
    └── source
```

### Qdrant Service

The project includes:

```text
app/services/qdrant_service.py
```

The service currently provides:

* Collection creation
* Embedding storage
* Vector configuration
* Payload management
* Qdrant client initialization

---

# 🐳 Docker & Containerization

The application is fully containerized across all layers for rapid, deterministic deployment.

### 1. Backend Docker Container (`Dockerfile`)
* **Base Image**: `python:3.11-slim`
* **System Libraries**: `libgl1`, `libglib2.0-0`, `libgomp1`, and `curl` for computer vision and OCR workloads
* **Optimization**: Multi-layer dependency caching (`requirements.txt` installed prior to application code copying)
* **Health Check**: Automated periodic health checks querying `http://localhost:8000/health`
* **Execution**: Production ASGI server via `uvicorn`

### 2. Frontend Docker Container (`docx-frontend/Dockerfile`)
* **Architecture**: Production-optimized **multi-stage build**
  * *Stage 1 (Builder)*: `node:20-alpine` builds optimized static distribution assets via Vite
  * *Stage 2 (Server)*: Ultra-lightweight `nginx:alpine` serves static files and reverse-proxies `/api/` traffic to the backend
* **Health Check**: Automated `wget` probe verifying HTTP 200

---

# 🐳 Full-Stack Docker Compose

Run the entire ecosystem (Frontend, API, and Vector Database) with a single command:

```bash
docker compose up --build
```

### Services & Port Mappings

| Service | Port | Description |
|---|---|---|
| **`frontend`** | `3000` | DocX React Web Interface (Nginx) |
| **`api`** | `8000` | FastAPI Document Intelligence Backend (`/docs` for Swagger) |
| **`qdrant`** | `6333` / `6334` | Qdrant Vector Database REST & gRPC endpoints |

```text
Full-Stack Architecture (docker-compose)
│
├── Frontend (React + Vite + Nginx)       ─── Port 3000
│     │ (proxies /api/ requests)
│     ▼
├── API (FastAPI + OCR + RAG + Embeddings)─── Port 8000
│     │ (communicates over docx-network)
│     ▼
└── Qdrant (Vector Database + Storage)    ─── Port 6333
      └── Persistent Volume: qdrant_data
```

---

# 🚀 CI/CD Pipeline (GitHub Actions)

DocX includes an automated, production-grade **CI/CD Pipeline** defined in [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml).

### Pipeline Workflow & Stages

```text
GitHub Push / Pull Request
         │
         ├───▶ Job 1: Backend CI
         │       • Python 3.11 Setup & Pip Cache
         │       • Flake8 Syntax & Code Quality Checks
         │       • Pytest Test Suite Execution (100% Pass)
         │
         ├───▶ Job 2: Frontend CI
         │       • Node.js 20 Setup & NPM Cache
         │       • Clean Dependency Installation
         │       • Vite Production Bundle Compilation
         │
         └───▶ Job 3: Docker CD & GitHub Container Registry
                 • Docker Compose Configuration Validation
                 • Docker Buildx Multi-Container Build
                 • Automatic Publish to GitHub Packages (GHCR) on `main`:
                     - ghcr.io/ashishmarothiya/docx/backend:latest
                     - ghcr.io/ashishmarothiya/docx/frontend:latest
```

### GitHub Packages & Container Visibility
When code is pushed to `main`, GitHub Actions automatically builds and publishes the container images to **GitHub Container Registry (GHCR)**. The Docker containers are automatically shown and linked on GitHub under the **"Packages"** section on your repository homepage.

---

#  Current Architecture

```text
                         Client
                           │
                           ▼
                     FastAPI API
                           │
                           ▼
                    Upload Endpoint
                           │
                           ▼
                     File Service
                           │
                           ▼
                  Document Pipeline
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
        PDF Pipeline              Image Pipeline
              │                         │
              ▼                         ▼
       PDF Extraction               OCR Service
              │                         │
              ▼                         │
      Document Classifier              │
              │                         │
         ┌────┴────┐                    │
         ▼         ▼                    │
        Text       OCR                  │
         │         │                    │
         └────┬────┘────────────────────┘
              ▼
        Text Cleaner
              │
              ▼
        Chunk Service
              │
              ▼
      Embedding Service
              │
              ▼
        Qdrant Service
              │
              ▼
           Qdrant
              │
              ▼
      Vector Storage
```

---

#  Software Architecture

The project follows a modular service-oriented architecture.

### API Layer

Responsible for:

* HTTP requests
* File uploads
* API routing
* Request/response handling

### Pipeline Layer

Responsible for:

* Orchestrating document processing
* Routing documents
* Coordinating multiple services

### Service Layer

Responsible for specialized operations:

```text
FileService
PDFService
OCRService
DocumentClassifier
TextCleaner
ChunkService
EmbeddingService
QdrantService
```

### Schema Layer

Responsible for structured data models using Pydantic.

Examples:

```text
DocumentData
ChunkData
EmbeddingData
PipelineData
```

This architecture follows:

* Separation of Concerns
* Single Responsibility
* Modular Design
* Service-Oriented Design
* Pipeline-Based Processing
* Clean Code Principles

---

#  Current Progress

## Current Phase

> **Vector Database Integration — Completed**

The project has successfully reached the end of the document ingestion and vector storage phase.

Current pipeline:

```text
Upload
  ↓
Document Processing
  ↓
OCR / PDF Extraction
  ↓
Text Cleaning
  ↓
Chunking
  ↓
Embeddings
  ↓
Qdrant Vector Storage
```

---

#  Completed Milestones

## Milestone 1 — Project Foundation

* Project Initialization
* FastAPI Setup
* API Routing
* Swagger Documentation
* Modular Architecture

---

## Milestone 2 — Document Processing Core

* Upload Endpoint
* File Validation
* File Storage Service
* Document Processing Pipeline
* Document Type Detection
* PDF Text Extraction
* Document Classification
* Unified Document Model

---

## Milestone 3 — OCR Integration

* PaddleOCR Integration
* OCR Service
* Image Processing
* Scanned PDF Processing
* OCR Decision Engine

---

## Milestone 4 — Text Processing & Embeddings

* Text Cleaning
* Chunking Service
* Overlapping Chunks
* Embedding Service
* Sentence Transformers Integration
* BAAI/bge-small-en-v1.5 Integration
* 384-dimensional normalized embeddings

---

## Milestone 5 — Docker & Containerization

* Dockerfile
* Docker Image
* Docker Build Optimization
* `.dockerignore`
* Docker Container Execution
* Docker Compose
* API Container
* Qdrant Container
* Docker Networking
* Persistent Qdrant Volume

---

## Milestone 6 — Qdrant Integration

* qdrant-client integration
* Qdrant Service
* Qdrant Collection Creation
* Vector Configuration
* Cosine Similarity
* Point Creation
* Vector Storage
* Payload Storage
* API → Qdrant communication
* Persistent Vector Database

The current system has successfully stored document embeddings in Qdrant.

Example:

```text
Document
   ↓
14 Chunks
   ↓
14 Embeddings
   ↓
14 Qdrant Points
```

---

#  Current Status

The document ingestion pipeline is complete.

The system can currently:

```text
Upload
   ↓
Extract / OCR
   ↓
Clean
   ↓
Chunk
   ↓
Embed
   ↓
Store in Qdrant
```

The next major step is **Semantic Search**.

---

#  Roadmap

##  Completed

* FastAPI Backend
* File Upload
* File Validation
* File Storage
* PDF Extraction
* OCR Integration
* Document Classification
* Text Cleaning
* Document Chunking
* Embedding Generation
* Docker
* Docker Compose
* Qdrant Integration
* Vector Storage
* Persistent Qdrant Storage

---

##  Next Step

### Semantic Search

Implement:

* Query embedding
* Qdrant similarity search
* Cosine similarity
* Top-K retrieval
* Relevant chunk retrieval
* Search service

Target workflow:

```text
User Question
      │
      ▼
Question Embedding
      │
      ▼
Qdrant Similarity Search
      │
      ▼
Top-K Relevant Chunks
```

---

##  Upcoming

### Retrieval

* Retriever component
* Search abstraction
* Metadata filtering
* Context selection

### RAG

* Retrieval-Augmented Generation pipeline
* Context construction
* Prompt construction
* LLM integration

### LLM

* OpenAI API
* Question Answering
* Context-aware responses

### Document Intelligence

* Document Summarization
* Structured JSON Extraction
* Advanced document understanding

### Infrastructure

* PostgreSQL
* Redis
* Docker Compose improvements
* Production deployment

---

# 🎯 Project Vision

This project is being developed as a **production-oriented AI Engineering portfolio project**.

The goal is not only to build an AI application, but also to apply modern software engineering and AI system design principles.

The project focuses on:

* Clean Architecture
* SOLID Principles
* Separation of Concerns
* Service-Oriented Design
* Pipeline-Based Processing
* Vector Search
* Retrieval-Augmented Generation
* Containerization
* Production-oriented backend engineering

The final goal is to build an end-to-end document intelligence system capable of understanding documents and answering questions using retrieved document context.

---

#  Author

**Hesham Elwakeel**

**AI Engineer | Computer Vision Engineer | Data Scientist**

Building production-oriented AI systems using Python, FastAPI, Computer Vision, Vector Databases, Retrieval-Augmented Generation (RAG), and Large Language Models.

* LinkedIn: https://linkedin.com/in/hesham-elwakeel
* Email: [heshamelwakeel17@gmail.com](mailto:heshamelwakeel17@gmail.com)

---

#  Current Status

> **Document ingestion and vector storage pipeline completed.**

The system currently implements:

**Upload → PDF/OCR Processing → Cleaning → Chunking → Embeddings → Qdrant Vector Storage**

The project is now entering the **Semantic Search and Retrieval phase**, which will serve as the foundation for the upcoming RAG pipeline.





