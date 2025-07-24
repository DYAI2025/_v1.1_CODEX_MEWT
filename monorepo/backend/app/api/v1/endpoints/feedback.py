from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

_feedback_store: list[dict] = []

class Feedback(BaseModel):
    analysis_id: str
    message: str

@router.post("/feedback")
def send_feedback(data: Feedback):
    _feedback_store.append(data.model_dump())
    return {"status": "received"}
