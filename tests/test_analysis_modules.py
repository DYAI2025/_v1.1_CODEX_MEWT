from mewt.marker_frequency import MarkerFrequencyCounter
from mewt.drift_axis import DriftAxisAnalyzer
from monorepo.backend.app.api.v1.models import ChunkResult, MarkerMatch


def make_chunk(ids):
    return ChunkResult(text="", matches=[MarkerMatch(marker_id=i, score=1) for i in ids])


def test_marker_frequency_counter():
    chunks = [make_chunk(["a", "b"]), make_chunk(["a"])]
    freq = MarkerFrequencyCounter().count(chunks)
    assert freq == {"a": 2, "b": 1}


def test_drift_axis_analyzer():
    chunks = [make_chunk(["pos"]), make_chunk(["neg", "neg"]), make_chunk(["pos"])]
    analyzer = DriftAxisAnalyzer({"pos"}, {"neg"})
    result = analyzer.analyze(chunks)
    assert result == -2.0
