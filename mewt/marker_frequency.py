from collections import Counter
from typing import Iterable, Protocol


class _ChunkLike(Protocol):
    matches: Iterable

class MarkerFrequencyCounter:
    """Count occurrences of markers across chunks."""

    def count(self, chunks: Iterable[_ChunkLike]) -> dict[str, int]:
        freq: Counter[str] = Counter()
        for chunk in chunks:
            for match in chunk.matches:
                freq[match.marker_id] += 1
        return dict(freq)
