from fastapi import APIRouter

from app.schemas.ask import (
    AskRequest,
    AskResponse,
    AskSource,
)

from app.services.rag_service import RAGService


router = APIRouter(
    prefix="/ask",
    tags=["RAG"],
)


rag_service = RAGService()


@router.post(
    "",
    response_model=AskResponse,
)
async def ask(request: AskRequest):

    result = rag_service.ask(
        query=request.query,
        limit=request.limit,
        min_score=request.min_score,
        source=request.source,
    )

    sources = [
        AskSource(
            score=item["score"],
            text=item["text"],
            chunk_index=item["chunk_index"],
            page=item["page"],
            source=item["source"],
        )
        for item in result["results"]
    ]

    return AskResponse(
        query=result["query"],
        answer=result["answer"],
        sources=sources,
    )
