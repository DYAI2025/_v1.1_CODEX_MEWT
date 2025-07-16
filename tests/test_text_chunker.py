import pytest
from src.text_chunker import TextChunker

class TestTextChunker:
    """Test-Suite für die TextChunker-Klasse."""
    
    def setup_method(self):
        """Setup für jeden Test."""
        self.chunker = TextChunker(max_chunk_size=100)
    
    def test_empty_text(self):
        """Test mit leerem Text."""
        result = self.chunker.split_text("")
        assert result == []
    
    def test_short_text(self):
        """Test mit Text kürzer als max_chunk_size."""
        text = "Dies ist ein kurzer Text."
        result = self.chunker.split_text(text)
        assert len(result) == 1
        assert result[0] == text
    
    def test_long_text_word_boundary(self):
        """Test dass Wörter nicht getrennt werden."""
        text = "Dies ist ein sehr langer Text " * 10
        result = self.chunker.split_text(text)
        
        # Prüfe dass kein Chunk die maximale Größe überschreitet
        for chunk in result:
            assert len(chunk) <= self.chunker.max_chunk_size
        
        # Prüfe dass alle Wörter vollständig sind
        for chunk in result:
            words = chunk.split()
            for word in words:
                assert word in text
    
    def test_text_with_newlines(self):
        """Test mit Text der Zeilenumbrüche enthält."""
        text = "Zeile 1\nZeile 2\nZeile 3\n" * 10
        result = self.chunker.split_text(text)
        
        # Stelle sicher dass Zeilen intakt bleiben
        combined = "\n".join(result)
        assert text.strip() == combined.strip()
    
    def test_very_long_line(self):
        """Test mit einer sehr langen Zeile."""
        text = "Wort " * 50  # Eine sehr lange Zeile
        result = self.chunker.split_text(text)
        
        # Sollte in mehrere Chunks aufgeteilt werden
        assert len(result) > 1
        
        # Alle Wörter sollten erhalten bleiben
        all_words = []
        for chunk in result:
            all_words.extend(chunk.split())
        assert all_words.count("Wort") == 50
    
    def test_detect_speaker_whatsapp(self):
        """Test Sprecher-Erkennung für WhatsApp-Format."""
        line = "15.03.24, 10:30 - Max Mustermann: Hallo, wie geht's?"
        speaker, message = self.chunker.detect_speaker(line)
        assert speaker == "Max Mustermann"
        assert message == "Hallo, wie geht's?"
    
    def test_detect_speaker_simple(self):
        """Test Sprecher-Erkennung für einfaches Format."""
        line = "Alice: Das ist eine Nachricht"
        speaker, message = self.chunker.detect_speaker(line)
        assert speaker == "Alice"
        assert message == "Das ist eine Nachricht"
    
    def test_detect_speaker_none(self):
        """Test wenn kein Sprecher erkannt wird."""
        line = "Dies ist nur eine normale Zeile ohne Sprecher"
        result = self.chunker.detect_speaker(line)
        assert result is None
    
    def test_format_with_speakers(self):
        """Test Formatierung mit Sprechern."""
        text = """Max: Hallo!
Max: Wie geht es dir?
Anna: Mir geht es gut, danke!
Anna: Und dir?"""
        
        result = self.chunker.format_with_speakers(text)
        
        # Prüfe dass Sprecher-Markierungen vorhanden sind
        assert "[Max]" in result
        assert "[Anna]" in result
        
        # Prüfe dass Nachrichten erhalten bleiben
        assert "Hallo!" in result
        assert "Mir geht es gut, danke!" in result
    
    def test_chunk_size_parameter(self):
        """Test verschiedene chunk_size Parameter."""
        text = "Ein Test " * 100
        
        # Test mit kleiner Chunk-Größe
        small_chunker = TextChunker(max_chunk_size=50)
        small_chunks = small_chunker.split_text(text)
        
        # Test mit großer Chunk-Größe
        large_chunker = TextChunker(max_chunk_size=500)
        large_chunks = large_chunker.split_text(text)
        
        # Kleinere Chunks sollten mehr Teile haben
        assert len(small_chunks) > len(large_chunks) 