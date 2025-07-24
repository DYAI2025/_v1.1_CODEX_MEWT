import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from monorepo.backend.app.services.transcription_service import TranscriptionService
from monorepo.backend.app.services.chunking_service import ChunkingService
from monorepo.backend.app.services.analysis_service import AnalysisService

import asyncio


def test_transcription_stub(tmp_path):
    audio = tmp_path / "a.opus"
    audio.write_text("dummy")
    svc = TranscriptionService()
    result = asyncio.run(svc.transcribe(str(audio)))
    assert "Transcribed" in result


def test_chunking_service():
    svc = ChunkingService(max_size=10)
    chunks = svc.chunk_text("hello world hello world")
    assert len(chunks) > 1


def test_analysis_service(tmp_path):
    # create marker file
    mdir = tmp_path / "marker_bank"
    mdir.mkdir()
    (mdir / "markers.yml").write_text("- id: test\n  pattern: hello\n  score: 2")
    service = AnalysisService(marker_dir=mdir)
    markers = service.load_markers()
    result = service.analyze_chunk("hello there", markers)
    assert result.matches[0].score == 2
