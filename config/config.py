import platform

TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe" if platform.system() == "Windows" else "tesseract"

POPPLER_PATH = r"C:\Users\User\OneDrive\Desktop\ReadingAssistantProject2\ocr_module\poppler-25.07.0\Library\bin" if platform.system() == "Windows" else None

PROFILE_FILE = "user_profile.json"
AUDIO_FILE = "output.mp3"