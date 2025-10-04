# Reading Assistant

A comprehensive reading assistant application that converts various text sources into natural-sounding speech with interactive playback features and advanced OCR capabilities.

## Features

### Input Methods
- **File Upload**: Support for multiple formats
  - Images (PNG, JPG, JPEG, BMP, TIFF)
  - PDF documents
  - DOCX files
- **Text Paste**: Direct text input with multi-line support
- **Camera Capture**: Real-time document scanning with live preview

### Advanced OCR & Text Processing
- **Dual OCR Engines**:
  - Tesseract OCR for printed text (fast, accurate for standard documents)
  - EasyOCR for handwritten text (optional, better for handwriting recognition)
- **Intelligent Image Preprocessing**:
  - Adaptive thresholding for optimal text extraction
  - Noise reduction and denoising
  - Sharpness and contrast enhancement
  - Customized processing for handwritten vs printed text
- **Multi-page PDF Support**: 
  - High-resolution (300 DPI) page conversion
  - Page-by-page processing with progress tracking
- **Text Cleanup & Correction**:
  - Common OCR error correction (e.g., "wilh" → "with", "lhe" → "the")
  - Whitespace normalization
  - Line break standardization

### Text-to-Speech
- **10 High-Quality Voices** (Microsoft Edge TTS):
  - **US English**: Aria (Female), Guy (Male), Jenny (Female), Eric (Male)
  - **British English**: Libby (Female), Ryan (Male)
  - **Indian English**: Neerja (Female), Prabhat (Male)
  - **Australian English**: Natasha (Female), William (Male)
  
- **7 Speed Options**:
  - 0.5x (Half speed)
  - 0.75x (Slower)
  - 1.0x (Normal)
  - 1.25x (Faster)
  - 1.5x (Fast)
  - 1.75x (Very fast)
  - 2.0x (Double speed)

- **Fallback Support**: Automatic fallback to pyttsx3 if Edge TTS is unavailable

### Interactive Playback Modes

#### Standard Playback Mode
Complete control over audio playback:
- **[P]** Pause - Pause playback
- **[R]** Resume - Continue playback
- **[S]** Stop - Stop audio completely
- **[Y]** Replay - Restart from beginning
- **[W]** Rewind - Go back 5 seconds
- **[F]** Forward - Skip ahead 5 seconds
- **[H]** Text Highlight - Switch to karaoke mode
- **[Q]** Quit - Exit application

#### Text Highlighting Mode (Karaoke)
Real-time word-by-word highlighting synchronized with audio:
- Visual progress bar showing completion percentage
- Current word highlighted in blue
- Previously spoken words shown in gray
- Intelligent word timing based on syllable estimation
- Smooth, dynamic text scrolling
- 10-word sliding window display

### User Profiles
- Save preferred voice selection
- Save speech rate settings
- Persistent preferences across sessions
- Profile stored in JSON format

## Prerequisites

### Required Software
- **Python 3.7+**
- **Tesseract OCR**: For printed text recognition
- **Poppler**: For PDF processing
- **Webcam**: For camera capture feature (optional)
- **Internet Connection**: Required for Edge TTS voices

### Optional Software
- **EasyOCR**: For enhanced handwriting recognition (GPU support optional)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/maddherlarupapriya-oss/ReadingAssistantProject2.git
cd ReadingAssistantProject2
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Unix/MacOS:
source .venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install edge-tts pyttsx3 pygame Pillow pdf2image python-docx opencv-python pytesseract

# Optional: For handwriting recognition
pip install easyocr
```

### 4. Install System Dependencies

#### Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location (`C:\Program Files\Tesseract-OCR`)
3. Add to PATH or update `config/config.py` with installation path

**Linux:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**MacOS:**
```bash
brew install tesseract
```

#### Poppler

**Windows:**
- Poppler binaries are included in `ocr_module/poppler-xx.xx.x/`
- Update path in `config/config.py` if needed

**Linux:**
```bash
sudo apt-get install poppler-utils
```

**MacOS:**
```bash
brew install poppler
```

## Usage

### Quick Start
```bash
python main.py
```

### Step-by-Step Workflow

#### 1. Choose Input Method
```
Choose Input Option:
1. Upload File (Image/PDF/DOCX)
2. Paste Text Manually
3. Use Camera to Scan Document
```

#### 2. Process Text
- For **images/PDFs**: Indicate if text is handwritten for better OCR
- For **camera**: Capture multiple pages (SPACE to capture, ESC when done)
- For **pasted text**: Press ENTER twice to finish input

#### 3. Review Extracted Text
- View raw extracted text (first 2000 characters)
- Review cleaned and corrected text
- See preview before audio generation

#### 4. Configure Voice Settings
- Select from 10 available voices
- Choose speech rate (0.5x to 2.0x)
- Option to save preferences for future sessions

#### 5. Select Playback Mode
- **Standard**: Full playback controls with interactive commands
- **Text Highlighting**: Follow along with word-by-word highlighting

#### 6. Enjoy Your Audio!
- Use playback controls as needed
- Switch between modes on the fly
- Save settings for next time

## Camera Capture Instructions

When using camera capture mode:
1. Position document clearly in frame
2. Ensure good lighting (avoid shadows and glare)
3. Press **SPACEBAR** to capture current frame
4. Captured images appear without overlay text
5. Press **ESC** when finished capturing
6. Use **CTRL+C** to force quit if needed

## Project Structure

```
ReadingAssistantProject2/
├── main.py                      # Main application entry point
├── config/
│   ├── __init__.py
│   └── config.py               # Configuration settings
├── input_module/
│   ├── __init__.py
│   └── input_module.py         # Input handling (file, text, camera)
├── ocr_module/
│   ├── __init__.py
│   ├── ocr_module.py           # OCR processing and text extraction
│   └── poppler-xx.xx.x/        # Poppler binaries (Windows)
├── preprocessing_module/
│   ├── __init__.py
│   └── preprocessing_module.py # Text cleanup and error correction
├── tts_module/
│   ├── __init__.py
│   └── tts_module.py           # TTS generation and audio playback
├── ui_module/
│   ├── __init__.py
│   └── ui_module.py            # User interface functions
├── user_profiles/
│   ├── __init__.py
│   └── user_profiles.py        # User preference management
├── user_profile.json           # Saved user preferences (auto-generated)
├── output.mp3                  # Generated audio file (temporary)
└── README.md                   # This file
```

## Configuration

Edit `config/config.py` to customize:
- Tesseract executable path
- Poppler binary path
- Profile file location
- Audio output file name

## Advanced Features

### OCR Engine Selection
- **Tesseract**: Best for clean, printed text (default)
- **EasyOCR**: Better for handwriting and complex fonts (when installed)
- Automatic preprocessing optimization based on text type

### Image Preprocessing Pipeline
1. Grayscale conversion
2. Noise reduction (fastNlMeansDenoising)
3. Adaptive thresholding
4. Sharpness enhancement (2x)
5. Contrast enhancement (1.5x)

### Word Timing Algorithm
The karaoke mode uses an intelligent algorithm to estimate word duration:
- Base duration from word character count
- Syllable estimation for natural pacing
- Proportional time allocation based on word complexity

## Troubleshooting

### Common Issues

**OCR produces poor results:**
- Ensure good image quality and lighting
- Try handwriting mode for non-standard text
- Check that Tesseract is properly installed
- Consider preprocessing images separately

**Audio generation fails:**
- Verify internet connection (required for Edge TTS)
- Application will automatically fallback to pyttsx3
- Check firewall settings for Edge TTS

**Camera not working:**
- Verify webcam is connected and not in use
- Check camera permissions
- Try different camera index if multiple cameras present

**PDF processing errors:**
- Ensure Poppler is correctly installed
- Verify POPPLER_PATH in config.py
- Check PDF isn't password-protected or corrupted

**EasyOCR not available:**
- EasyOCR is optional; Tesseract will be used instead
- Install with: `pip install easyocr`
- Note: First run downloads language models (may take time)

## Keyboard Interrupt Handling

The application gracefully handles **CTRL+C** interrupts:
- Camera capture: Safely releases camera and exits
- Text input: Saves entered text before exit
- Audio playback: Immediate stop and clean exit
- Settings save: Option to skip saving preferences

## Error Handling

Comprehensive error handling for:
- File access and I/O operations
- OCR conversion failures
- Network connectivity issues
- Audio playback problems
- Invalid user inputs
- Missing dependencies

## Performance Tips

- Use Tesseract for faster processing of printed text
- Enable EasyOCR only when needed (slower but better for handwriting)
- Use lower DPI for large PDFs if speed is a priority
- Close other applications using audio devices
- Ensure stable internet connection for Edge TTS

## Privacy & Data

- All processing is done locally except TTS generation
- No user data is transmitted except to Microsoft Edge TTS service
- User profiles stored locally in JSON format
- Captured images saved locally in `captures/` directory
- Audio files are temporary and can be deleted

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Areas for improvement:
- Additional OCR engines
- More TTS voice options
- Enhanced preprocessing algorithms
- Language support beyond English
- GUI interface
- Mobile app version

Please feel free to submit a Pull Request.

## Acknowledgments

- **Microsoft Edge TTS**: High-quality neural voice synthesis
- **Tesseract OCR**: Open-source text recognition engine
- **EasyOCR**: Deep learning-based OCR for handwriting
- **Poppler**: PDF rendering and processing
- **OpenCV**: Computer vision and image processing
- **Pygame**: Audio playback and control
- **Pillow**: Image manipulation and enhancement

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide detailed error messages and system information

## Version History

**Current Version**: Features as documented above
- Multi-engine OCR support
- 10 voice options with 7 speed settings
- Dual playback modes
- Advanced text preprocessing
- Camera capture with live preview
- User preference persistence

---

**Made with ❤️ for accessible reading**
