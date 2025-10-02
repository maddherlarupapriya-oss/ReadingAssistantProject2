import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import docx
from config.config import TESSERACT_CMD, POPPLER_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def image_path_to_text(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def pil_image_to_text(img):
    return pytesseract.image_to_string(img)

def pdf_to_text(pdf_path):
    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    text = ""
    for i, page in enumerate(pages, start=1):
        text += f"\n--- Page {i} ---\n" + pytesseract.image_to_string(page)
    return text

def docx_to_text(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])
