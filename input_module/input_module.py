import os
from PIL import Image
from pdf2image import convert_from_path
import docx
import cv2
import time
from config.config import POPPLER_PATH


def get_input_choice():
    print("\nChoose Input Option:")
    print("1. Upload File (Image/PDF/DOCX)")
    print("2. Paste Text Manually")
    print("3. Use Camera to Scan Document")
    opt = input("Enter option number (1-3): ").strip()
    return opt


def capture_images_from_camera(output_dir="captures"):
    os.makedirs(output_dir, exist_ok=True)
    cam = cv2.VideoCapture(0)
    
    if not cam.isOpened():
        print("Error: Could not open camera")
        return []
    
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    captured = []
    idx = 1
    
    print("\nCAMERA MODE")
    print("A window will open showing camera feed")
    print("SPACE = Capture | ESC = Finish | CTRL+C = Force quit\n")
    
    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Failed to read from camera")
                break
            
            # Create a COPY for display with overlays
            display_frame = frame.copy()
            
            # Add text ONLY to display frame (NOT to the saved image)
            cv2.putText(display_frame, f"Captured: {len(captured)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, "SPACE=Capture | ESC=Finish", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Show display frame with overlays
            cv2.imshow("Camera - SPACE to capture, ESC to finish", display_frame)
            key = cv2.waitKey(1)
            
            if key == 27:  # ESC
                break
            if key == 32:  # SPACEBAR
                # Save ORIGINAL frame without overlays
                fname = os.path.join(output_dir, f"capture_{idx}.png")
                cv2.imwrite(fname, frame)  # Save frame, NOT display_frame
                captured.append(fname)
                print(f"Captured: {fname}")
                idx += 1
    
    except KeyboardInterrupt:
        print("\nCamera interrupted by Ctrl+C")
    
    finally:
        cam.release()
        cv2.destroyAllWindows()
    
    print(f"\nTotal captured: {len(captured)}")
    return captured


def load_file(file_name):
    if not os.path.exists(file_name):
        print(f"File not found: {file_name}")
        return ("unsupported", None)
    ext = file_name.lower().split('.')[-1]
    if ext in ["png", "jpg", "jpeg", "bmp", "tiff"]:
        return ("image", file_name)
    if ext == "pdf":
        return ("pdf", file_name)
    if ext == "docx":
        return ("docx", file_name)
    return ("unsupported", None)


def read_pasted_text():
    print("\nPaste text. Press ENTER twice when done.")
    lines = []
    empty_count = 0
    
    try:
        while True:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 1:
                    break
            else:
                empty_count = 0
                lines.append(line)
    except KeyboardInterrupt:
        print("\nInput interrupted by Ctrl+C")
    
    return "\n".join(lines)
