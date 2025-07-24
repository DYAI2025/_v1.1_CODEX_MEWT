import argparse
import json
from pathlib import Path
from .schema_loader import SchemaLoader
from .marker_frequency import MarkerFrequencyCounter
from .drift_axis import DriftAxisAnalyzer
from monorepo.backend.app.services.chunking_service import ChunkingService
from monorepo.backend.app.services.analysis_service import AnalysisService


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run chat analysis")
    parser.add_argument("text_file", help="Path to chat text file")
    parser.add_argument("--schema", help="Schema file", required=False)
    args = parser.parse_args(argv)

    text_path = Path(args.text_file)
    text = text_path.read_text(encoding="utf-8")

    schema = {}
    if args.schema:
        schema = SchemaLoader().load(args.schema)

    marker_dir = Path(schema.get("marker_dir", "monorepo/marker_bank"))
    service = AnalysisService(marker_dir=marker_dir)
    chunker = ChunkingService()

    chunks = chunker.chunk_text(text)
    markers = service.load_markers()
    results = [service.analyze_chunk(c, markers) for c in chunks]

    counter = MarkerFrequencyCounter()
    freq = counter.count(results)

    drift = DriftAxisAnalyzer(
        set(schema.get("positive_markers", [])),
        set(schema.get("negative_markers", [])),
    ).analyze(results)

    output = {"frequencies": freq, "drift": drift, "chunks": [r.model_dump() for r in results]}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
