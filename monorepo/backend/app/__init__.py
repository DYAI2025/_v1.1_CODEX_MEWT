from fastapi import FastAPI
from .api.v1.endpoints.analysis import router as analysis_router
from .api.v1.endpoints.markers import router as markers_router
from .api.v1.endpoints.schemas import router as schemas_router
from .api.v1.endpoints.feedback import router as feedback_router

app = FastAPI(title="Marker Engine API")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(markers_router, prefix="/api/v1")
app.include_router(schemas_router, prefix="/api/v1")
app.include_router(feedback_router, prefix="/api/v1")
