from fastapi import Query
from pydantic import BaseModel


class AiPromptDto(BaseModel):
    prompt: str = Query(..., description="User search query")
    limit: int = Query(5, ge=1, le=50),