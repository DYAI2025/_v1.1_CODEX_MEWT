#!/usr/bin/env python3
"""
Chat Chunker - Hauptmodul
Ein Tool zum Aufteilen großer Chat-Dateien in verarbeitbare Chunks.
"""

import sys
import os
from pathlib import Path

# Füge src zum Python-Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui import ChunkerGUI
from src.logger import setup_logger

logger = setup_logger("main")

def main():
    """Hauptfunktion zum Starten der Anwendung."""
    try:
        logger.info("Chat Chunker wird gestartet...")
        
        # GUI starten
        app = ChunkerGUI()
        app.run()
        
        logger.info("Chat Chunker beendet")
    except Exception as e:
        logger.error(f"Fehler beim Starten der Anwendung: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 