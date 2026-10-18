import pytest
from app.services.text_cleaner import TextCleaner
from app.services.chunking_service import ChunkService
from app.services.document_classifier import DocumentClassifier
from app.schemas.document import DocumentData, PageData


def test_text_cleaner_whitespace():
    cleaner = TextCleaner()
    # Normalize spaces and tabs
    raw = "  This   is    a   sample\tdocument.  "
    expected = "This is a sample document."
    assert cleaner.clean(raw) == expected


def test_text_cleaner_newlines():
    cleaner = TextCleaner()
    raw = "Paragraph 1\n\n\n\nParagraph 2\n\nParagraph 3"
    expected = "Paragraph 1\nParagraph 2\nParagraph 3"
    assert cleaner.clean(raw) == expected


def test_text_cleaner_empty_input():
    cleaner = TextCleaner()
    assert cleaner.clean("") == ""
    assert cleaner.clean(None) == ""


def test_document_classifier_empty_doc():
    classifier = DocumentClassifier()
    doc = DocumentData(
        text="",
        characters=0,
        is_empty=True,
        pages=0,
        source="invoice.pdf",
        page_data=[]
    )
    assert classifier.classify(doc) == "ocr"


def test_document_classifier_text_doc():
    classifier = DocumentClassifier()
    page = PageData(page=1, text="Direct text content")
    doc = DocumentData(
        text="Direct text content",
        characters=19,
        is_empty=False,
        pages=1,
        source="contract.pdf",
        page_data=[page]
    )
    assert classifier.classify(doc) == "text"


def test_chunk_service_splitting():
    chunk_service = ChunkService()
    # Generate 600 characters of text
    content = "Hello World! " * 50
    pages = [PageData(page=1, text=content)]

    chunks = chunk_service.split(
        pages=pages,
        source="sample.pdf",
        chunk_size=200,
        overlap=50
    )

    assert len(chunks) > 1
    assert chunks[0].page == 1
    assert chunks[0].source == "sample.pdf"
    assert len(chunks[0].text) == 200
    assert chunks[0].id == 0
    assert chunks[1].id == 1
