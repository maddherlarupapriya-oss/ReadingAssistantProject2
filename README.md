# Reading Assistant

A versatile reading assistant application that converts various text sources into speech with interactive playback features.

## Features

- Multiple Input Methods:
  - File Upload (Image/PDF/DOCX)
  - Text Paste
  - Camera Capture
- Text Processing:
  - OCR for images
  - PDF text extraction
  - DOCX parsing
  - Text preprocessing
- Text-to-Speech:
  - Multiple voice options
  - Adjustable speech rate
  - Karaoke-style word highlighting
  - Basic playback controls
- User Profiles:
  - Save voice preferences
  - Save speech rate settings

## Prerequisites

- Python 3.x
- Poppler (for PDF processing)
- A webcam (for camera capture feature)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ReadingAssistantProject
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
source .venv/bin/activate
```

3. Install required packages:
```bash
pip install edge-tts pyttsx3 pygame Pillow pdf2image python-docx opencv-python
```

4. Install Poppler:
- Windows: Included in the repository under `ocr_module/poppler-xx.xx.x/`
- Linux: `sudo apt-get install poppler-utils`
- MacOS: `brew install poppler`

## Usage

1. Run the main script:
```bash
python main.py
```

2. Choose input method:
   - Upload a file (Image/PDF/DOCX)
   - Paste text manually
   - Use camera to scan document

3. Select voice preferences:
   - Choose from available voices
   - Set speech rate

4. Choose playback mode:
   - Standard playback
   - Karaoke mode with word highlighting

## Project Structure

- `main.py` - Main application entry point
- `config/` - Configuration settings
- `input_module/` - Input handling functions
- `ocr_module/` - OCR and text extraction
- `preprocessing_module/` - Text preprocessing
- `tts_module/` - Text-to-speech functionality
- `ui_module/` - User interface functions
- `user_profiles/` - User preferences management

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.