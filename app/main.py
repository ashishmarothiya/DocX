from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.search import router as search_router
from app.api.ask import router as ask_router


app = FastAPI(
    title="Document Intelligence Engine",
    description=(
        "Document Intelligence Engine is a powerful tool for "
        "extracting insights from documents using advanced AI models. "
        "It provides endpoints for health checks, document processing, "
        "semantic search, and AI-powered RAG answers."
    ),
    version="1.0.0",
)

# Enable CORS for local dev and frontend container access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(ask_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Document Intelligence Engine"
    }
