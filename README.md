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
  - Text preprocessing and cleanup
- Text-to-Speech:
  - Multiple voice options (10 different voices):
    - US English - Aria (Female)
    - US English - Guy (Male)
    - British English - Libby (Female)
    - British English - Ryan (Male)
    - Indian English - Neerja (Female)
    - Indian English - Prabhat (Male)
    - Australian English - Natasha (Female)
    - Australian English - William (Male)
    - US English - Jenny (Female)
    - US English - Eric (Male)
  - Adjustable speech rates:
    - 0.5x (Half speed)
    - 0.75x (Slower)
    - 1.0x (Normal)
    - 1.25x (Faster)
    - 1.5x (Fast)
    - 1.75x (Very fast)
    - 2.0x (Double speed)
  - Playback Controls:
    - Play/Pause
    - Forward/Rewind
    - Stop
    - Volume adjustment
  - Interactive Text Display:
    - Standard playback mode
    - Karaoke mode with word highlighting
- User Profiles:
  - Save voice preferences
  - Save speech rate settings
  - Persistent settings between sessions

## Prerequisites

- Python 3.x
- Poppler (for PDF processing)
- A webcam (for camera capture feature)
- Internet connection (for Edge TTS voices)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/maddherlarupapriya-oss/ReadingAssistantProject2.git
cd ReadingAssistantProject2
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
   - Choose from 10 available voices
   - Set preferred speech rate
   - Settings can be saved for future use

4. Choose playback mode:
   - Standard playback with controls (pause, rewind, forward)
   - Karaoke mode with synchronized word highlighting

## Playback Controls

- Space: Play/Pause
- Left Arrow: Rewind
- Right Arrow: Fast Forward
- Up Arrow: Increase Volume
- Down Arrow: Decrease Volume
- Q: Quit playback
- H: Switch to highlighting mode during playback

## Project Structure

- `main.py` - Main application entry point and program flow control
- `config/` - Configuration settings and parameters
- `input_module/` - Input handling for files, text, and camera
- `ocr_module/` - OCR processing and text extraction utilities
- `preprocessing_module/` - Text cleanup and preprocessing
- `tts_module/` - Text-to-speech conversion and audio playback
- `ui_module/` - User interface and display functions
- `user_profiles/` - User preferences and settings management

## Error Handling

The application includes robust error handling for:
- File access and processing
- OCR conversion
- Network connectivity (for TTS)
- Audio playback issues
- Invalid user inputs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Microsoft Edge TTS for high-quality voice synthesis
- Tesseract OCR for text recognition
- Poppler for PDF processing
- OpenCV for camera capture