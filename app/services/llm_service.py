import os

from openai import OpenAI


class LLMService:
    """
    Generates grounded answers using retrieved document context.
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(api_key=api_key)

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.6-terra",
        )

    def generate_answer(
        self,
        query: str,
        results: list[dict],
    ) -> str:

        if not results:
            return (
                "I couldn't find enough information in the "
                "indexed documents to answer this question."
            )

        context_parts = []

        for index, result in enumerate(results, start=1):

            source = result.get("source") or "Unknown source"
            page = result.get("page") or "Unknown page"
            chunk = result.get("chunk_index")
            score = result.get("score", 0)
            text = result.get("text") or ""

            context_parts.append(
                f"""
SOURCE {index}
Source: {source}
Page: {page}
Chunk: {chunk}
Retrieval score: {score:.4f}

Content:
{text}
""".strip()
            )

        context = "\n\n---\n\n".join(context_parts)
import os

from google import genai


class LLMService:
    """
    Generates grounded answers using retrieved document context.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(api_key=api_key)

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        )

    def generate_answer(
        self,
        query: str,
        results: list[dict],
    ) -> str:

        if not results:
            return (
                "I couldn't find enough information in the "
                "indexed documents to answer this question."
            )

        context_parts = []

        for index, result in enumerate(results, start=1):

            source = result.get("source") or "Unknown source"
            page = result.get("page") or "Unknown page"
            chunk = result.get("chunk_index")
            score = result.get("score", 0)
            text = result.get("text") or ""

            context_parts.append(
                f"""
SOURCE {index}
Source: {source}
Page: {page}
Chunk: {chunk}
Retrieval score: {score:.4f}

Content:
{text}
""".strip()
            )

        context = "\n\n---\n\n".join(context_parts)

        prompt = f"""
You are the AI answer engine for a document intelligence system.

Answer the user's question using ONLY the retrieved document
content provided below.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent facts that are not supported by the documents.
3. Give a clear, useful and natural answer.
4. If the documents do not contain enough information, explicitly say so.
5. If different sources contradict each other, explain the contradiction.
6. Cite supporting evidence inline using [Source N, Page X].
7. Keep the answer focused on the user's question.
8. You may synthesize information from multiple retrieved sources.

USER QUESTION:
{query}

RETRIEVED DOCUMENT CONTEXT:
{context}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        answer = response.text

        if not answer:
            return (
                "The AI model did not return an answer. "
                "Please try the question again."
            )

        return answer
