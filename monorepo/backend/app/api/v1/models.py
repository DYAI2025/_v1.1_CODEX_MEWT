from pydantic import BaseModel
from typing import List

class MarkerMatch(BaseModel):
    marker_id: str
    score: int

class ChunkResult(BaseModel):
    text: str
    matches: List[MarkerMatch]

class AnalysisResult(BaseModel):
    id: str
    chunks: List[ChunkResult]
