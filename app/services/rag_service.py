from app.services.search_service import SearchService
from app.services.llm_service import LLMService


class RAGService:
    """
    Retrieval-Augmented Generation service.

    Retrieves relevant document chunks from Qdrant
    and uses an LLM to generate a grounded answer.
    """

    def __init__(self):
        self.search_service = SearchService()
        self.llm_service = LLMService()

    def ask(
        self,
        query: str,
        limit: int = 8,
        min_score: float | None = None,
        source: str | None = None,
    ):

        # Step 1: Retrieve relevant evidence
        results = self.search_service.search(
            query=query,
            limit=limit,
            min_score=min_score,
            source=source,
        )

        # Step 2: Generate grounded answer
        answer = self.llm_service.generate_answer(
            query=query,
            results=results,
        )

        return {
            "query": query,
            "answer": answer,
            "results": results,
        }
