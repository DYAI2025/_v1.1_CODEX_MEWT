import yaml
from fastapi import APIRouter
from ....services.analysis_service import AnalysisService

router = APIRouter()

@router.get("/markers")
def get_markers():
    service = AnalysisService()
    markers = service.load_markers()
    return markers
