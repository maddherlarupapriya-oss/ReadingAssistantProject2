import os
from PIL import Image
from pdf2image import convert_from_path
import docx
import cv2
from config.config import POPPLER_PATH

def get_input_choice():
    print("Choose Input Option:")
    print("1. Upload File (Image/PDF/DOCX)")
    print("2. Paste Text Manually")
    print("3. Use Camera to Scan Document")
    opt = input("Enter option number: ").strip()
    return opt

def capture_images_from_camera(output_dir="captures"):
    os.makedirs(output_dir, exist_ok=True)
    cam = cv2.VideoCapture(0)
    captured = []
    idx = 1
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        cv2.imshow("Camera - SPACE capture, ESC done", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == 32:
            fname = os.path.join(output_dir, f"capture_{idx}.png")
            cv2.imwrite(fname, frame)
            captured.append(fname)
            idx += 1
    cam.release()
    cv2.destroyAllWindows()
    return captured

def load_file(file_name):
    ext = file_name.lower().split('.')[-1]
    if ext in ["png", "jpg", "jpeg"]:
        return ("image", file_name)
    if ext == "pdf":
        return ("pdf", file_name)
    if ext == "docx":
        return ("docx", file_name)
    return ("unsupported", None)

def read_pasted_text():
    print("Paste or type your text. Finish input with an empty line:")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)