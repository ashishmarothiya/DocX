import os
import sys
from unittest.mock import MagicMock

# Set dummy environment variables for testing
os.environ.setdefault("OPENAI_API_KEY", "mock-test-key")
os.environ.setdefault("GEMINI_API_KEY", "mock-test-key")
os.environ.setdefault("QDRANT_URL", "http://localhost:6333")

# Mock external heavy / network dependencies if not installed in current environment
HEAVY_MODULES = [
    "paddleocr",
    "paddlepaddle",
    "paddlex",
    "sentence_transformers",
    "qdrant_client",
    "qdrant_client.models",
    "fitz",
    "pymupdf",
    "cv2",
    "google",
    "google.genai",
    "openai",
]

for mod in HEAVY_MODULES:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()
