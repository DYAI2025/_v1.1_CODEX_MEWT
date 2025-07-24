from src.text_chunker import TextChunker

class ChunkingService:
    def __init__(self, max_size: int = 5000):
        self.chunker = TextChunker(max_chunk_size=max_size)

    def chunk_text(self, text: str):
        return self.chunker.split_text(text)
