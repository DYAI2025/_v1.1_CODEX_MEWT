"""
Eigene Exception-Klassen für das Chat Chunker Projekt.
"""

class ChunkerError(Exception):
    """Basis-Exception für alle Chat Chunker Fehler."""
    pass

class FileReadError(ChunkerError):
    """Fehler beim Lesen einer Datei."""
    pass

class FileWriteError(ChunkerError):
    """Fehler beim Schreiben einer Datei."""
    pass

class ChunkingError(ChunkerError):
    """Fehler beim Chunking-Prozess."""
    pass

class EncodingError(ChunkerError):
    """Fehler bei der Zeichenkodierung."""
    pass 