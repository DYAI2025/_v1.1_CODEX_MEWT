import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()

SCHEMA_DIR = Path(__file__).resolve().parents[4] / "schemas"

@router.get("/schemas")
def get_schemas():
    result = {}
    for file in SCHEMA_DIR.glob("*.*"):
        result[file.name] = json.loads(file.read_text()) if file.suffix == ".json" else file.read_text()
    return result
