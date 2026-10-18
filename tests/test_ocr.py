from pathlib import Path
from unittest.mock import MagicMock
import pytest

from app.services.ocr_service import OCRService


def test_ocr_extract_text_mocked():
    """Test OCR text extraction pipeline with mocked PaddleOCR engine."""
    ocr = OCRService()
    # Mock predict return value on the instance
    ocr.ocr.predict = MagicMock(return_value=[
        {"rec_texts": ["DocX Test Invoice", "Amount: $1,200.00"]}
    ])

    result = ocr.extract_text(Path("data/uploads/mock_sample.png"))

    assert result.source == "mock_sample.png"
    assert not result.is_empty
    assert "DocX Test Invoice" in result.text
    assert len(result.page_data) == 1
    assert result.page_data[0].page == 1


def test_ocr_extract_text_live_file_if_exists():
    """Live OCR test only runs if local sample image data/uploads/t.png exists."""
    sample_file = Path("data/uploads/t.png")
    if not sample_file.exists():
        pytest.skip("data/uploads/t.png not found; skipping live OCR test.")

    ocr = OCRService()
    result = ocr.extract_text(sample_file)
    assert result is not None