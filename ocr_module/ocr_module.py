import pytesseract
from PIL import Image, ImageEnhance
from pdf2image import convert_from_path
import docx
import cv2
import numpy as np
from config.config import TESSERACT_CMD, POPPLER_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

# Try to import EasyOCR (optional, for handwriting)
try:
    import easyocr
    EASYOCR_AVAILABLE = True
    # Initialize reader once (it's slow to initialize)
    easyocr_reader = easyocr.Reader(['en'], gpu=False)
except ImportError:
    EASYOCR_AVAILABLE = False
    easyocr_reader = None

def preprocess_image_for_ocr(image, for_handwriting=False):
    """Preprocess image for better OCR results"""
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image
    
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    if for_handwriting:
        # Less aggressive preprocessing for handwriting
        denoised = cv2.fastNlMeansDenoising(gray, None, 5, 7, 21)
        binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 15, 5)
    else:
        # Standard preprocessing for printed text
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
    
    pil_image = Image.fromarray(binary)
    enhancer = ImageEnhance.Sharpness(pil_image)
    sharpened = enhancer.enhance(2.0)
    enhancer = ImageEnhance.Contrast(sharpened)
    contrasted = enhancer.enhance(1.5)
    return contrasted

def image_path_to_text(path, use_easyocr=False):
    """
    Extract text from image.
    Set use_easyocr=True for better handwriting recognition.
    """
    if use_easyocr and EASYOCR_AVAILABLE:
        # Use EasyOCR for handwriting
        result = easyocr_reader.readtext(path, detail=0, paragraph=True)
        return ' '.join(result)
    else:
        # Use Tesseract for printed text
        img = Image.open(path)
        processed_img = preprocess_image_for_ocr(img, for_handwriting=use_easyocr)
        # PSM 6: Assume uniform block of text
        # PSM 7: Treat image as single text line (good for handwriting)
        custom_config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(processed_img, config=custom_config)

def pdf_to_text(pdf_path, use_easyocr=False):
    """Extract text from PDF"""
    try:
        pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH, dpi=300)
        text = ""
        for i, page in enumerate(pages, start=1):
            print(f"Processing page {i}/{len(pages)}...")
            
            if use_easyocr and EASYOCR_AVAILABLE:
                # Convert PIL to numpy array for EasyOCR
                page_array = np.array(page)
                result = easyocr_reader.readtext(page_array, detail=0, paragraph=True)
                page_text = ' '.join(result)
            else:
                processed = preprocess_image_for_ocr(page, for_handwriting=False)
                page_text = pytesseract.image_to_string(processed, config=r'--oem 3 --psm 6')
            
            text += f"\n--- Page {i} ---\n" + page_text
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""

def docx_to_text(path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""