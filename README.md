# Chat Chunker

Ein Tool zum Aufteilen großer Chat-Dateien in verarbeitbare Chunks von maximal 5000 Zeichen.

## Features

- 📁 Drag & Drop GUI für einfache Dateiverarbeitung
- ✂️ Intelligente Text-Aufteilung an Wortgrenzen
- 💬 Sprecher-Erkennung und formatierte Darstellung
- 📝 Automatische Benennung: NAME_ch001.txt, NAME_ch002.txt, etc.
- 📂 Organisierte Ausgabe im `ready_chunks/` Verzeichnis

## Installation

1. Repository klonen:
```bash
git clone https://github.com/Narion2025/chat_chunker.git
cd chat_chunker
```

2. Virtuelle Umgebung erstellen und aktivieren:
```bash
python -m venv venv
source venv/bin/activate  # Auf Windows: venv\Scripts\activate
```

3. Dependencies installieren:
```bash
pip install -r requirements.txt
```

## Verwendung

1. Programm starten:
```bash
python -m src.main
```

2. Text-Dateien per Drag & Drop in das Fenster ziehen
3. "Process" Button klicken
4. Verarbeitete Chunks finden Sie im `ready_chunks/` Verzeichnis

## Unterstützte Formate

- Standard .txt Dateien
- WhatsApp Chat-Exporte
- Andere Chat-Formate mit klarer Sprecher-Kennzeichnung

## Entwicklung

Tests ausführen:
```bash
pytest tests/ -v --cov=src
```

## Lizenz

MIT License 