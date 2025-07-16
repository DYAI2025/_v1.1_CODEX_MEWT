import pytest
import tempfile
import os
from pathlib import Path
from src.file_handler import FileHandler

class TestFileHandler:
    """Test-Suite für die FileHandler-Klasse."""
    
    def setup_method(self):
        """Setup für jeden Test."""
        # Temporäres Verzeichnis für Tests
        self.temp_dir = tempfile.mkdtemp()
        self.handler = FileHandler(output_dir=os.path.join(self.temp_dir, "test_output"))
    
    def teardown_method(self):
        """Cleanup nach jedem Test."""
        # Temporäres Verzeichnis löschen
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_output_dir_creation(self):
        """Test dass Ausgabeverzeichnis erstellt wird."""
        assert self.handler.output_dir.exists()
        assert self.handler.output_dir.is_dir()
    
    def test_read_file_success(self):
        """Test erfolgreiches Lesen einer Datei."""
        # Testdatei erstellen
        test_file = os.path.join(self.temp_dir, "test.txt")
        test_content = "Dies ist ein Test."
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Datei lesen
        result = self.handler.read_file(test_file)
        assert result == test_content
    
    def test_read_file_not_exists(self):
        """Test Lesen einer nicht existierenden Datei."""
        result = self.handler.read_file("/nicht/existierende/datei.txt")
        assert result is None
    
    def test_read_file_encoding_fallback(self):
        """Test Encoding-Fallback auf latin-1."""
        # Testdatei mit latin-1 Encoding erstellen
        test_file = os.path.join(self.temp_dir, "test_latin1.txt")
        test_content = "Ümläute: äöü"
        with open(test_file, 'w', encoding='latin-1') as f:
            f.write(test_content)
        
        # Datei lesen (sollte auf latin-1 zurückfallen)
        result = self.handler.read_file(test_file)
        assert result is not None
        assert "äöü" in result or "Ã¤Ã¶Ã¼" in result  # Je nach Encoding
    
    def test_save_chunks(self):
        """Test Speichern von Chunks."""
        chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
        base_name = "testfile.txt"
        
        saved_files = self.handler.save_chunks(chunks, base_name)
        
        # Prüfe Anzahl gespeicherter Dateien
        assert len(saved_files) == 3
        
        # Prüfe Dateinamen
        expected_names = ["testfile_ch001.txt", "testfile_ch002.txt", "testfile_ch003.txt"]
        for i, file_path in enumerate(saved_files):
            assert expected_names[i] in file_path
            
            # Prüfe Inhalt
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert content == chunks[i]
    
    def test_save_chunks_empty_list(self):
        """Test Speichern einer leeren Chunk-Liste."""
        saved_files = self.handler.save_chunks([], "test.txt")
        assert saved_files == []
    
    def test_sanitize_filename(self):
        """Test Dateinamen-Bereinigung."""
        # Test mit ungültigen Zeichen
        assert self.handler._sanitize_filename('test<>file.txt') == 'test__file.txt'
        assert self.handler._sanitize_filename('test:file|name') == 'test_file_name'
        
        # Test mit führenden/nachfolgenden Leerzeichen
        assert self.handler._sanitize_filename('  test  ') == 'test'
        
        # Test mit zu langem Namen
        long_name = 'a' * 150
        sanitized = self.handler._sanitize_filename(long_name)
        assert len(sanitized) == 100
        
        # Test mit leerem Namen
        assert self.handler._sanitize_filename('') == 'unnamed'
    
    def test_clear_output_directory(self):
        """Test Leeren des Ausgabeverzeichnisses."""
        # Erstelle einige Testdateien
        for i in range(3):
            test_file = self.handler.output_dir / f"test_{i}.txt"
            test_file.write_text("Test")
        
        # Verzeichnis sollte Dateien enthalten
        assert len(list(self.handler.output_dir.glob("*.txt"))) == 3
        
        # Verzeichnis leeren
        self.handler.clear_output_directory()
        
        # Verzeichnis sollte leer sein
        assert len(list(self.handler.output_dir.glob("*.txt"))) == 0
    
    def test_chunk_numbering(self):
        """Test korrekte Nummerierung mit führenden Nullen."""
        # Erstelle mehr als 10 Chunks um Nummerierung zu testen
        chunks = [f"Chunk {i}" for i in range(15)]
        saved_files = self.handler.save_chunks(chunks, "test.txt")
        
        # Prüfe Nummerierung
        for i, file_path in enumerate(saved_files):
            expected_num = f"ch{i+1:03d}"
            assert expected_num in file_path 