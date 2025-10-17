# Reading Assistant

A full‑stack web application that turns documents into natural‑sounding speech with optional word‑by‑word highlighting, dual OCR engines, and user preferences designed for dyslexic readers.

## Table of contents

- Overview
- Features
- Tech stack
- Project structure
- Prerequisites
- Installation
- Run locally
- Usage
- Reader modes
- Preferences
- API endpoints
- Configuration
- Troubleshooting
- Roadmap
- Contributing
- License

## Overview

Reading Assistant is a browser‑based app built with Flask that extracts text from PDFs, images, DOCX, and live camera scans, then reads it aloud using either in‑browser voices with perfect highlighting sync or Microsoft Edge’s neural voices. It includes a dyslexia‑friendly UI, OpenDyslexic font, larger spacing, and user‑saved preferences.

## Features

- Inputs
  - Upload PDF, image (PNG, JPG, JPEG, BMP, TIFF), and DOCX
  - Paste text directly in the browser
  - Camera capture with live preview for quick scans

- OCR and text cleanup
  - Tesseract OCR for printed text
  - Optional EasyOCR for handwriting
  - Preprocessing pipeline: denoise, threshold, contrast/sharpness, line/whitespace normalization
  - Multi‑page PDF processing and progress feedback

- Text‑to‑speech
  - Live Highlighting mode (browser SpeechSynthesis) with word‑level sync
  - Edge TTS mode with 10+ high‑quality neural voices and speed control
  - Fast toggle between modes

- Reader experience
  - Play, pause, resume, stop
  - Rewind and forward (time‑seek in Edge TTS, word‑skip in highlight mode)
  - Progress bar and auto‑scroll to current word
  - Dyslexia‑friendly typography via OpenDyslexic

- Preferences and profiles
  - Save font size, reading speed, default highlighting, line spacing, and handwriting preference
  - Applied automatically for each signed‑in user

## Tech stack

- Backend: Python, Flask
- OCR and parsing: pytesseract (Tesseract), PyMuPDF for PDFs, python‑docx for DOCX, Pillow for image ops, optional EasyOCR
- TTS: Web Speech API (browser), edge‑tts (Microsoft neural voices)
- Frontend: HTML, CSS, JavaScript
- Browser APIs: MediaDevices.getUserMedia (camera), Canvas (frame capture)
- Storage: JSON files for demo persistence (users and documents)

## Project structure

```
ReadingAssistantProject2/
├── main.py
├── ui_module/
│   ├── __init__.py
│   └── ui_flask.py                # Flask app (routes, templates, static)
├── templates/
│   ├── login.html
│   ├── upload.html
│   ├── preferences.html
│   └── reader.html
├── static/                        # CSS/JS/assets as needed
├── input_module/
│   ├── __init__.py
│   └── input_module.py
├── ocr_module/
│   ├── __init__.py
│   └── ocr_module.py
│   └── poppler-xx.xx.x/           # Poppler (Windows, optional)
├── preprocessing_module/
│   ├── __init__.py
│   └── preprocessing_module.py
├── tts_module/
│   ├── __init__.py
│   └── tts_module.py
├── user_profiles/
│   ├── __init__.py
│   └── user_profiles.py
├── users_data.json                # demo user store (auto-created)
├── documents_data.json            # demo document store (auto-created)
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10+
- Tesseract OCR installed and on PATH
- Poppler installed for PDF rasterization (if using image‑based PDF path)
- Optional EasyOCR (GPU optional)
- Internet connection for Edge TTS voices
- A webcam for camera capture (optional)

## Installation

```bash
# Clone
git clone https://github.com/maddherlarupapriya-oss/ReadingAssistantProject2.git
cd ReadingAssistantProject2

# Create venv
python -m venv .venv

# Activate
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install Python deps
pip install -r requirements.txt
# If you don’t have a requirements.txt, install the core libs:
# pip install Flask pytesseract PyMuPDF python-docx Pillow edge-tts easyocr
```

Tesseract and Poppler

- Windows
  - Tesseract: install from UB‑Mannheim build and add to PATH
  - Poppler: use included poppler‑xx.xx.x or install and set path
- macOS
  - brew install tesseract
  - brew install poppler
- Linux
  - sudo apt‑get install tesseract‑ocr
  - sudo apt‑get install poppler‑utils

## Run locally

```bash
# From project root
python ui_module/ui_flask.py

# App will open at:
# http://127.0.0.1:5000
```

## Usage

- Register or log in
- Upload a document, paste text, or scan with camera
- Open the Reader to listen and highlight
- Choose a voice and speed
- Save Preferences to persist font size, speed, default highlighting, and spacing

## Reader modes

- Live Highlighting
  - Uses browser SpeechSynthesis for word boundaries
  - Accurate word‑by‑word highlight and auto‑scroll
  - Pause/resume from the current word
  - Word‑skip on rewind/forward

- Edge TTS
  - Uses Microsoft neural voices with speed control
  - Standard audio playback with time‑seek
  - Highlighting disabled by default in this mode
  - Auto‑fallback path can be added if needed

## Preferences

- Saved at /preferences for the logged‑in user
- Applied in reader.html on load via injected template data
- Fields
  - font_size
  - reading_speed
  - highlighting_enabled
  - line_spacing
  - auto_handwriting

## API endpoints

- GET /api/edge‑voices
  - Returns available short names and labels for Edge TTS voices

- GET /api/generate‑audio/<doc_id>?voice=…&speed=…
  - Streams MP3 generated with edge‑tts for the selected document

- GET /reader/<doc_id>
  - Renders the Reader with injected user preferences

- POST /preferences
  - Saves the current user’s preferences JSON

## Configuration

- Tesseract path can be set in code if not on PATH
- Poppler path can be configured for Windows
- Default preferences injected for new users

## Troubleshooting

- No highlighting
  - Ensure Live mode is enabled; Edge TTS mode disables highlighting by design
- Pause/resume restarts from beginning
  - Confirm the updated reader.js logic that tracks currentWordIndex is present
- Voices not listed
  - Wait for onvoiceschanged in browser mode or refresh Edge voices endpoint
- OCR quality poor
  - Use handwriting mode for cursive or noisy images and ensure good lighting
- Camera blocked
  - Allow camera permissions in the browser and use HTTPS in production

## Roadmap

- Word timing alignment for cloud TTS with timestamps
- More languages and voices
- Cloud deployment template (Docker + HTTPS)
- Database persistence (PostgreSQL or SQLite) instead of JSON

## Contributing

- Fork the repo, create a feature branch, commit changes, and open a PR with a description and screenshots or short video
- Please include repro steps and environment details for bugs

## License

MIT License. See LICENSE for details.

