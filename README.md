# Marker Engine
![CI](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)

A modular platform for chat analysis built with FastAPI and Streamlit. It processes chat exports and audio files, chunks text, and applies YAML-based rules to generate insights.

## Features
- File upload of WhatsApp ZIP or plain text
- Optional audio transcription (Whisper)
- Chunking of conversations into pieces of max 5000 characters
- Rule based analysis using markers defined in YAML
- REST API with OpenAPI docs
- Minimal Streamlit frontend

## Quickstart
```bash
# Install dependencies
pip install -r requirements.txt

# Run API
uvicorn monorepo.backend.app.main:app --reload
```

Run tests:
```bash
pytest -q
```

A docker-compose file is provided to start the API, frontend and MongoDB.
