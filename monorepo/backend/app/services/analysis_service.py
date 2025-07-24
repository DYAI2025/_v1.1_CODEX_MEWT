import re
import yaml
from pathlib import Path
from ..api.v1.models import MarkerMatch, ChunkResult

DEFAULT_MARKER_DIR = Path(__file__).resolve().parents[3] / "marker_bank"

class AnalysisService:
    def __init__(self, marker_dir: Path | None = None):
        self.marker_dir = marker_dir or DEFAULT_MARKER_DIR

    def load_markers(self):
        markers = []
        for file in self.marker_dir.glob("*.yml"):
            markers.extend(yaml.safe_load(file.read_text()))
        return markers

    def analyze_chunk(self, text: str, markers):
        matches = []
        for m in markers:
            pattern = m.get("pattern") or m.get("patterns")
            if isinstance(pattern, list):
                pattern = "|".join(pattern)
            if pattern and re.search(pattern, text, re.IGNORECASE):
                matches.append(MarkerMatch(marker_id=m.get("id", "unknown"), score=m.get("score", 1)))
        return ChunkResult(text=text, matches=matches)
