import pytest
from app.schemas.chunk import ChunkData
from app.schemas.document import DocumentData, PageData
from app.schemas.embedding import EmbeddingData
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.schemas.ask import AskRequest, AskResponse, AskSource


def test_chunk_data():
    chunk = ChunkData(
        id=42,
        text="Extracted section",
        page=3,
        source="doc1.pdf"
    )
    assert chunk.id == 42
    assert chunk.text == "Extracted section"
    assert chunk.page == 3
    assert chunk.source == "doc1.pdf"


def test_document_data():
    page = PageData(page=1, text="Page 1 text")
    doc = DocumentData(
        text="Page 1 text",
        characters=11,
        is_empty=False,
        pages=1,
        source="test.pdf",
        page_data=[page]
    )
    assert doc.pages == 1
    assert not doc.is_empty
    assert len(doc.page_data) == 1


def test_embedding_data():
    emb = EmbeddingData(
        text="Sample text",
        embedding=[0.1, 0.2, 0.3],
        chunk_index=1,
        page=1,
        source="doc.pdf"
    )
    assert emb.chunk_index == 1
    assert len(emb.embedding) == 3
    assert emb.source == "doc.pdf"


def test_search_request_and_response():
    req = SearchRequest(query="invoice total", limit=5, min_score=0.8)
    assert req.query == "invoice total"
    assert req.limit == 5
    assert req.min_score == 0.8

    res_item = SearchResult(
        score=0.92,
        text="Total amount: $120.00",
        chunk_index=1,
        page=1,
        source="bill.pdf"
    )
    res = SearchResponse(
        query=req.query,
        results=[res_item],
        min_score=req.min_score
    )
    assert len(res.results) == 1
    assert res.results[0].score == 0.92
    assert res.min_score == 0.8


def test_ask_request_and_response():
    req = AskRequest(query="What is the due date?", limit=3)
    assert req.query == "What is the due date?"
    assert req.limit == 3

    source_item = AskSource(
        score=0.88,
        text="Payment due on Nov 1",
        chunk_index=2,
        page=2,
        source="due.pdf"
    )
    res = AskResponse(
        query=req.query,
        answer="The payment is due on November 1st.",
        sources=[source_item]
    )
    assert res.answer.startswith("The payment")
    assert len(res.sources) == 1
