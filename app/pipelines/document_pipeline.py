"""
Document Pipeline

This module is the main entry point for document processing in the
Document Intelligence Engine.

Responsibilities:
- Detect the uploaded file type (PDF or image).
- Route the document to the appropriate processing pipeline.
- Extract text directly from text-based PDFs.
- Classify PDFs to determine whether OCR is required.
- Run OCR for scanned PDFs when necessary.
- Clean extracted text.
- Return a unified processing result for downstream components.

This class acts as the orchestrator of the document processing workflow,
delegating the actual extraction and OCR tasks to specialized services.
"""

from pathlib import Path

from app.services.pdf_service import extract_text_from_pdf
from app.services.document_classifier import DocumentClassifier
from app.services.ocr_service import OCRService
from app.services.text_cleaner import TextCleaner
from app.services.chunking_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.qdrant_service import QdrantService


class DocumentPipeline:
    """
    Main orchestrator responsible for routing documents through the
    appropriate processing pipeline.
    """

    def __init__(self):
        self.cleaner = TextCleaner()
        self.classifier = DocumentClassifier()

        # OCR is initialized lazily.
        # This prevents PaddleOCR/PaddlePaddle from starting for
        # normal text-based PDFs that do not need OCR.
        self.ocr_service = None

        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

        # Ensure the Qdrant collection exists before storing data.
        self.qdrant_service.create_collection()

    def _get_ocr_service(self):
        """
        Initialize OCR only when it is actually required.
        """
        if self.ocr_service is None:
            print("Initializing OCR service...")
            self.ocr_service = OCRService()

        return self.ocr_service

    async def process(self, file_path: Path):

        print(f"Processing file: {file_path}")

        extension = file_path.suffix.lower()

        print(f"Detected file type: {extension}")

        if extension == ".pdf":
            return await self._process_pdf(file_path)

        elif extension in [".png", ".jpg", ".jpeg"]:
            return await self._process_image(file_path)

        else:
            raise ValueError(f"Unsupported file type: {extension}")

    async def _process_pdf(self, file_path: Path):

        print("PDF pipeline selected")

        # ---------------------------------------------------------
        # STEP 1: Extract text directly from PDF
        # ---------------------------------------------------------

        document = extract_text_from_pdf(file_path)

        # ---------------------------------------------------------
        # STEP 2: Clean extracted text
        # ---------------------------------------------------------

        for page in document.page_data:
            page.text = self.cleaner.clean(page.text)

        # Rebuild full document text
        document.text = "\n".join(
            page.text
            for page in document.page_data
        )

        document.characters = len(document.text)
        document.is_empty = len(document.text.strip()) == 0

        print(
            f"Extracted characters: {document.characters}, "
            f"empty={document.is_empty}"
        )

        # ---------------------------------------------------------
        # STEP 3: Decide whether OCR is required
        # ---------------------------------------------------------

        decision = self.classifier.classify(document)

        print(f"Document classification: {decision}")

        # ---------------------------------------------------------
        # STEP 4: OCR only when required
        # ---------------------------------------------------------

        if decision == "ocr":

            print("OCR required. Starting OCR service...")

            ocr_service = self._get_ocr_service()

            document = ocr_service.extract_text(file_path)

            # Clean OCR output
            for page in document.page_data:
                page.text = self.cleaner.clean(page.text)

            # Rebuild full document text
            document.text = "\n".join(
                page.text
                for page in document.page_data
            )

            document.characters = len(document.text)
            document.is_empty = len(document.text.strip()) == 0

            print(
                f"OCR extracted characters: {document.characters}, "
                f"empty={document.is_empty}"
            )

        # ---------------------------------------------------------
        # STEP 5: Split document into chunks
        # ---------------------------------------------------------

        chunks = self.chunk_service.split(
            pages=document.page_data,
            source=document.source,
        )

        print(f"Generated {len(chunks)} chunks")

        # Print a small preview for debugging
        for chunk in chunks[:5]:
            print(
                f"chunk={chunk.id}, "
                f"page={chunk.page}, "
                f"source={chunk.source}, "
                f"text_preview={chunk.text[:50]!r}"
            )

        # ---------------------------------------------------------
        # STEP 6: Generate embeddings
        # ---------------------------------------------------------

        embeddings = self.embedding_service.encode(chunks)

        print(f"Generated {len(embeddings)} embeddings")

        # ---------------------------------------------------------
        # STEP 7: Store embeddings in Qdrant
        # ---------------------------------------------------------

        self.qdrant_service.store_embeddings(embeddings)

        print("Embeddings stored successfully in Qdrant")

        # ---------------------------------------------------------
        # STEP 8: Return processing result
        # ---------------------------------------------------------

        return {
            "pipeline": "pdf",
            "decision": decision,
            "pages": document.pages,
            "characters": document.characters,
            "is_empty": document.is_empty,
            "preview": document.text[:500],
            "chunks": len(chunks),
            "embeddings": len(embeddings),
        }

    async def _process_image(self, file_path: Path):

        print("Image pipeline selected")

        # Images always require OCR.
        ocr_service = self._get_ocr_service()

        # ---------------------------------------------------------
        # STEP 1: OCR extraction
        # ---------------------------------------------------------

        document = ocr_service.extract_text(file_path)

        # ---------------------------------------------------------
        # STEP 2: Clean OCR output
        # ---------------------------------------------------------

        for page in document.page_data:
            page.text = self.cleaner.clean(page.text)

        # Rebuild full document text
        document.text = "\n".join(
            page.text
            for page in document.page_data
        )

        document.characters = len(document.text)
        document.is_empty = len(document.text.strip()) == 0

        # ---------------------------------------------------------
        # STEP 3: Split into chunks
        # ---------------------------------------------------------

        chunks = self.chunk_service.split(
            pages=document.page_data,
            source=document.source,
        )

        print(f"Generated {len(chunks)} chunks")

        # ---------------------------------------------------------
        # STEP 4: Generate embeddings
        # ---------------------------------------------------------

        embeddings = self.embedding_service.encode(chunks)

        print(f"Generated {len(embeddings)} embeddings")

        # ---------------------------------------------------------
        # STEP 5: Store embeddings in Qdrant
        # ---------------------------------------------------------

        self.qdrant_service.store_embeddings(embeddings)

        print("Embeddings stored successfully in Qdrant")

        # ---------------------------------------------------------
        # STEP 6: Return processing result
        # ---------------------------------------------------------

        return {
            "pipeline": "image",
            "characters": document.characters,
            "is_empty": document.is_empty,
            "preview": document.text[:500],
            "chunks": len(chunks),
            "embeddings": len(embeddings),
        }
