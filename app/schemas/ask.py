from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=8, ge=1, le=20)
    min_score: float | None = None
    source: str | None = None


class AskSource(BaseModel):
    score: float
    text: str
    chunk_index: int | None = None
    page: int | None = None
    source: str | None = None


class AskResponse(BaseModel):
    query: str
    answer: str
    sources: list[AskSource]
