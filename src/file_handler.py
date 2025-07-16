import os
from pathlib import Path
from typing import List, Optional
from .logger import setup_logger

logger = setup_logger("file_handler")

class FileHandler:
    """
    Klasse für Datei-I/O Operationen.
    """
    
    def __init__(self, output_dir: str = "ready_chunks"):
        """
        Initialisiert den FileHandler.
        
        Args:
            output_dir: Ausgabeverzeichnis für Chunks
        """
        self.output_dir = Path(output_dir)
        self._ensure_output_dir()
        logger.info(f"FileHandler initialisiert mit output_dir={output_dir}")
    
    def _ensure_output_dir(self):
        """Stellt sicher, dass das Ausgabeverzeichnis existiert."""
        self.output_dir.mkdir(exist_ok=True)
        logger.debug(f"Ausgabeverzeichnis erstellt/verifiziert: {self.output_dir}")
    
    def read_file(self, file_path: str, encoding: str = 'utf-8') -> Optional[str]:
        """
        Liest eine Textdatei ein.
        
        Args:
            file_path: Pfad zur Datei
            encoding: Zeichenkodierung (Standard: utf-8)
            
        Returns:
            Dateiinhalt als String oder None bei Fehler
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                logger.info(f"Datei erfolgreich gelesen: {file_path} ({len(content)} Zeichen)")
                return content
        except UnicodeDecodeError:
            logger.warning(f"UTF-8 Dekodierung fehlgeschlagen für {file_path}, versuche latin-1")
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                    logger.info(f"Datei mit latin-1 gelesen: {file_path}")
                    return content
            except Exception as e:
                logger.error(f"Fehler beim Lesen der Datei {file_path}: {e}")
                return None
        except Exception as e:
            logger.error(f"Fehler beim Lesen der Datei {file_path}: {e}")
            return None
    
    def save_chunks(self, chunks: List[str], base_name: str) -> List[str]:
        """
        Speichert Text-Chunks in einzelne Dateien.
        
        Args:
            chunks: Liste der Text-Chunks
            base_name: Basis-Name für die Ausgabedateien
            
        Returns:
            Liste der erstellten Dateipfade
        """
        # Entferne Dateierweiterung vom Basis-Namen
        base_name = Path(base_name).stem
        
        # Bereinige den Dateinamen (entferne ungültige Zeichen)
        base_name = self._sanitize_filename(base_name)
        
        saved_files = []
        
        for i, chunk in enumerate(chunks, 1):
            # Formatiere Chunk-Nummer mit führenden Nullen
            chunk_filename = f"{base_name}_ch{i:03d}.txt"
            chunk_path = self.output_dir / chunk_filename
            
            try:
                with open(chunk_path, 'w', encoding='utf-8') as file:
                    file.write(chunk)
                saved_files.append(str(chunk_path))
                logger.debug(f"Chunk gespeichert: {chunk_path}")
            except Exception as e:
                logger.error(f"Fehler beim Speichern von {chunk_path}: {e}")
        
        logger.info(f"{len(saved_files)} Chunks gespeichert für {base_name}")
        return saved_files
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Bereinigt einen Dateinamen von ungültigen Zeichen.
        
        Args:
            filename: Der zu bereinigende Dateiname
            
        Returns:
            Bereinigter Dateiname
        """
        # Entferne oder ersetze ungültige Zeichen
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Entferne führende/nachfolgende Leerzeichen und Punkte
        filename = filename.strip('. ')
        
        # Begrenze Länge
        if len(filename) > 100:
            filename = filename[:100]
        
        # Fallback, falls Dateiname leer ist
        if not filename:
            filename = "unnamed"
        
        return filename
    
    def clear_output_directory(self):
        """Löscht alle Dateien im Ausgabeverzeichnis."""
        try:
            for file in self.output_dir.glob("*.txt"):
                file.unlink()
            logger.info("Ausgabeverzeichnis geleert")
        except Exception as e:
            logger.error(f"Fehler beim Leeren des Ausgabeverzeichnisses: {e}") 