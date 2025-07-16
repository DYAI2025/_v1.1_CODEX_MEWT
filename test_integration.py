import pytest
import tempfile
import os
import shutil
from pathlib import Path
from src.text_chunker import TextChunker
from src.file_handler import FileHandler

@pytest.mark.integration
class TestIntegration:
    """Integration-Tests für den kompletten Workflow."""
    
    def setup_method(self):
        """Setup für jeden Test."""
        self.temp_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.temp_dir, "input")
        self.output_dir = os.path.join(self.temp_dir, "output")
        os.makedirs(self.input_dir)
        
        self.chunker = TextChunker(max_chunk_size=100)
        self.file_handler = FileHandler(output_dir=self.output_dir)
    
    def teardown_method(self):
        """Cleanup nach jedem Test."""
        shutil.rmtree(self.temp_dir)
    
    def test_complete_workflow(self):
        """Test des kompletten Workflows: Lesen → Chunking → Speichern."""
        # Testdatei erstellen
        test_content = "Dies ist ein Test. " * 50  # ~950 Zeichen
        input_file = os.path.join(self.input_dir, "test_chat.txt")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Workflow ausführen
        content = self.file_handler.read_file(input_file)
        assert content is not None
        
        chunks = self.chunker.split_text(content)
        assert len(chunks) > 1  # Sollte in mehrere Chunks aufgeteilt werden
        
        saved_files = self.file_handler.save_chunks(chunks, "test_chat.txt")
        assert len(saved_files) == len(chunks)
        
        # Prüfe dass alle Chunks existieren und lesbar sind
        for file_path in saved_files:
            assert os.path.exists(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                chunk_content = f.read()
                assert len(chunk_content) > 0
                assert len(chunk_content) <= self.chunker.max_chunk_size
    
    def test_chat_format_workflow(self):
        """Test mit Chat-formatiertem Text."""
        # Chat-Beispiel erstellen
        chat_content = """15.03.24, 10:30 - Alice: Hallo Bob!
15.03.24, 10:31 - Bob: Hi Alice, wie geht's?
15.03.24, 10:32 - Alice: Gut, danke! Und dir?
15.03.24, 10:33 - Bob: Auch gut. Was machst du gerade?
15.03.24, 10:34 - Alice: Ich arbeite an einem neuen Projekt.
15.03.24, 10:35 - Bob: Klingt spannend! Erzähl mal mehr.""" * 5
        
        input_file = os.path.join(self.input_dir, "whatsapp_chat.txt")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(chat_content)
        
        # Workflow mit Sprecher-Formatierung
        content = self.file_handler.read_file(input_file)
        formatted_content = self.chunker.format_with_speakers(content)
        
        # Prüfe Formatierung
        assert "[Alice]" in formatted_content
        assert "[Bob]" in formatted_content
        
        chunks = self.chunker.split_text(formatted_content)
        saved_files = self.file_handler.save_chunks(chunks, "whatsapp_chat.txt")
        
        # Prüfe dass Sprecher in gespeicherten Dateien erhalten bleiben
        for file_path in saved_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                chunk_content = f.read()
                # Mindestens einer der Sprecher sollte in jedem Chunk sein
                assert "[Alice]" in chunk_content or "[Bob]" in chunk_content
    
    def test_large_file_performance(self):
        """Test mit großer Datei für Performance."""
        # Große Testdatei erstellen (1MB)
        large_content = "Dies ist eine Zeile mit etwas Text. " * 30000
        input_file = os.path.join(self.input_dir, "large_file.txt")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(large_content)
        
        # Zeit messen
        import time
        start_time = time.time()
        
        # Workflow
        content = self.file_handler.read_file(input_file)
        chunks = self.chunker.split_text(content)
        saved_files = self.file_handler.save_chunks(chunks, "large_file.txt")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Performance-Checks
        assert duration < 5.0  # Sollte in weniger als 5 Sekunden fertig sein
        assert len(saved_files) > 100  # Sollte viele Chunks erstellen
        
        # Prüfe dass alle Chunks die richtige Größe haben
        for file_path in saved_files:
            file_size = os.path.getsize(file_path)
            assert file_size <= self.chunker.max_chunk_size + 100  # Etwas Spielraum
    
    def test_special_characters(self):
        """Test mit Sonderzeichen und Emojis."""
        special_content = """User1: Hallo! 😊
User2: Wie geht's? 🎉
User1: Super! Schöne Grüße aus München 🏙️
User2: Danke! Grüße zurück aus Berlin 🐻"""
        
        input_file = os.path.join(self.input_dir, "special_chars.txt")
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(special_content)
        
        # Workflow
        content = self.file_handler.read_file(input_file)
        formatted = self.chunker.format_with_speakers(content)
        chunks = self.chunker.split_text(formatted)
        saved_files = self.file_handler.save_chunks(chunks, "special_chars.txt")
        
        # Prüfe dass Sonderzeichen erhalten bleiben
        for file_path in saved_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                chunk_content = f.read()
                # Prüfe ob mindestens ein Emoji erhalten geblieben ist
                emojis = ['😊', '🎉', '🏙️', '🐻']
                assert any(emoji in chunk_content for emoji in emojis)
    
    def test_empty_file(self):
        """Test mit leerer Datei."""
        empty_file = os.path.join(self.input_dir, "empty.txt")
        Path(empty_file).touch()
        
        # Workflow
        content = self.file_handler.read_file(empty_file)
        chunks = self.chunker.split_text(content)
        saved_files = self.file_handler.save_chunks(chunks, "empty.txt")
        
        # Sollte keine Chunks erstellen
        assert len(saved_files) == 0 