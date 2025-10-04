"""
Text preprocessing module with OCR error correction
"""

def preprocess_text(text):
    """
    Main preprocessing function with common OCR error corrections
    """
    # Common OCR errors dictionary (case-sensitive)
    ocr_corrections = {
        'Absiract': 'Abstract',
        'absiract': 'abstract',
        'wilh': 'with',
        'lhe': 'the',
        'Lhe': 'The',
        'compuler': 'computer',
        'Compuler': 'Computer',
        'syslem': 'system',
        'Syslem': 'System',
        'dala': 'data',
        'Dala': 'Data',
        'informalion': 'information',
        'Informalion': 'Information',
        'wilhin': 'within',
        'communicalion': 'communication',
        'Communicalion': 'Communication',
        'compulational': 'computational',
        'Compulational': 'Computational',
    }
    
    # Apply corrections
    for wrong, correct in ocr_corrections.items():
        text = text.replace(wrong, correct)
    
    # Basic cleanup - normalize line breaks
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    
    # Remove excessive spaces (more than 2 spaces become 1)
    while "   " in text:
        text = text.replace("   ", " ")
    
    # Remove excessive blank lines (more than 3 newlines become 2)
    while "\n\n\n\n" in text:
        text = text.replace("\n\n\n\n", "\n\n")
    
    # Trim start and end
    text = text.strip()
    
    return text
