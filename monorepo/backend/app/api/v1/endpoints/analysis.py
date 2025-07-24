import uuid
import zipfile
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from mewt.marker_frequency import MarkerFrequencyCounter
from ..models import AnalysisResult
from ....services.transcription_service import TranscriptionService
from ....services.chunking_service import ChunkingService
from ....services.analysis_service import AnalysisService
from ....utils.file_handler import save_temp_file

router = APIRouter()

_results: dict[str, AnalysisResult] = {}

@router.post("/analyze", response_model=AnalysisResult)
async def analyze(file: UploadFile = File(...)):
    analysis_id = str(uuid.uuid4())
    temp_path = await save_temp_file(file)

    if zipfile.is_zipfile(temp_path):
        with zipfile.ZipFile(temp_path) as z:
            texts = []
            audios = []
            for name in z.namelist():
                if name.endswith(".txt"):
                    texts.append(z.read(name).decode("utf-8", errors="ignore"))
                if name.endswith((".opus", ".mp4")):
                    audio_path = z.extract(name)
                    audios.append(audio_path)
    else:
        texts = [open(temp_path, "r", encoding="utf-8").read()]
        audios = []

    transcriber = TranscriptionService()
    transcripts = [await transcriber.transcribe(a) for a in audios]
    full_text = "\n".join(texts + transcripts)

    chunker = ChunkingService()
    chunks = chunker.chunk_text(full_text)

    analyzer = AnalysisService()
    markers = analyzer.load_markers()
    results = [analyzer.analyze_chunk(c, markers) for c in chunks]

    result = AnalysisResult(id=analysis_id, chunks=results)
    _results[analysis_id] = result
    return result

@router.get("/results/{analysis_id}")
async def get_result(analysis_id: str):
    data = _results.get(analysis_id)
    if not data:
        return JSONResponse(status_code=404, content={"detail": "not found"})
    return data


@router.get("/summary/{analysis_id}")
async def get_summary(analysis_id: str):
    data = _results.get(analysis_id)
    if not data:
        return JSONResponse(status_code=404, content={"detail": "not found"})
    freq = MarkerFrequencyCounter().count(data.chunks)
    return {"id": analysis_id, "frequencies": freq}


@router.post("/reload")
async def reload_results():
    _results.clear()
    return {"status": "reloaded"}
