from typing import Iterable, Set, Protocol


class _ChunkLike(Protocol):
    matches: Iterable

class DriftAxisAnalyzer:
    """Simple drift analyzer comparing positive and negative marker usage."""

    def __init__(self, positive_markers: Set[str] | None = None, negative_markers: Set[str] | None = None):
        self.positive_markers = positive_markers or set()
        self.negative_markers = negative_markers or set()

    def analyze(self, chunks: Iterable[_ChunkLike]) -> float:
        """Return difference between second half and first half marker scores."""
        chunks = list(chunks)
        if not chunks:
            return 0.0
        mid = len(chunks) // 2
        def score(sub):
            total = 0
            for chunk in sub:
                for m in chunk.matches:
                    if m.marker_id in self.positive_markers:
                        total += m.score
                    if m.marker_id in self.negative_markers:
                        total -= m.score
            return total
        first = score(chunks[:mid or 1])
        second = score(chunks[mid:])
        return float(second - first)
