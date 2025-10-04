# main.py
from input_module.input_module import get_input_choice, capture_images_from_camera, load_file, read_pasted_text
from ocr_module.ocr_module import image_path_to_text, pdf_to_text, docx_to_text
from preprocessing_module.preprocessing_module import preprocess_text
from tts_module.tts_module import generate_audio_with_fallback, play_with_controls, play_karaoke
from ui_module.ui_module import show_preview
from user_profiles.user_profiles import load_profile, save_profile
import sys


def main():
    try:
        opt = get_input_choice()
        if opt is None:
            return
        
        if opt == "1":
            fname = input("Enter file name: ").strip()
            kind, path = load_file(fname)
            if kind == "image":
                handwriting = input("Is this handwritten text? (y/n, default n): ").strip().lower() == 'y'
                raw = image_path_to_text(path, use_easyocr=handwriting)
            elif kind == "pdf":
                handwriting = input("Does PDF contain handwritten text? (y/n, default n): ").strip().lower() == 'y'
                raw = pdf_to_text(path, use_easyocr=handwriting)
            elif kind == "docx":
                raw = docx_to_text(path)
            else:
                print("Unsupported file type")
                return
        elif opt == "2":
            raw = read_pasted_text()
        elif opt == "3":
            imgs = capture_images_from_camera()
            if not imgs:
                print("No captures made")
                return
            handwriting = input("\nAre these handwritten images? (y/n, default n): ").strip().lower() == 'y'
            parts = []
            print("\nProcessing captured images...")
            for i, p in enumerate(imgs, start=1):
                print(f"Processing {i}/{len(imgs)}...")
                parts.append(image_path_to_text(p, use_easyocr=handwriting))
            raw = "\n".join(parts)
        else:
            print("Invalid option")
            return

        if not raw or not raw.strip():
            print("No text found")
            return

        print("\n=== Raw Extracted Text (first 2000 chars) ===\n")
        print(raw[:2000] + ("\n...[truncated]" if len(raw) > 2000 else ""))

        cleaned = preprocess_text(raw)

        print("\n=== Cleaned Text (first 2000 chars) ===\n")
        print(cleaned[:2000] + ("\n...[truncated]" if len(cleaned) > 2000 else ""))

        show_preview(cleaned)

        profile = load_profile()
        
        voices = {
            "1": ("en-US-AriaNeural", "US English - Aria (Female)"),
            "2": ("en-US-GuyNeural", "US English - Guy (Male)"),
            "3": ("en-GB-LibbyNeural", "British English - Libby (Female)"),
            "4": ("en-GB-RyanNeural", "British English - Ryan (Male)"),
            "5": ("en-IN-NeerjaNeural", "Indian English - Neerja (Female)"),
            "6": ("en-IN-PrabhatNeural", "Indian English - Prabhat (Male)"),
            "7": ("en-AU-NatashaNeural", "Australian English - Natasha (Female)"),
            "8": ("en-AU-WilliamNeural", "Australian English - William (Male)"),
            "9": ("en-US-JennyNeural", "US English - Jenny (Female)"),
            "10": ("en-US-EricNeural", "US English - Eric (Male)")
        }
        
        print("\nAvailable Voices:")
        for k, (voice_id, description) in voices.items():
            print(f"{k}. {description}")
        
        vchoice = input("\nChoose voice number (press Enter to keep saved): ").strip()
        if vchoice in voices:
            profile["voice"] = voices[vchoice][0]
        
        speed_options = {
            "1": ("-50%", "0.5x (Half speed)"),
            "2": ("-25%", "0.75x (Slower)"),
            "3": ("+0%", "1.0x (Normal)"),
            "4": ("+25%", "1.25x (Faster)"),
            "5": ("+50%", "1.5x (Fast)"),
            "6": ("+75%", "1.75x (Very fast)"),
            "7": ("+100%", "2.0x (Double speed)")
        }
        
        print("\nSpeech Speed Options:")
        for k, (rate, description) in speed_options.items():
            print(f"{k}. {description}")
        
        speed_choice = input("\nChoose speed (press Enter to keep saved): ").strip()
        if speed_choice in speed_options:
            profile["rate"] = speed_options[speed_choice][0]

        audio_file, engine_used = generate_audio_with_fallback(cleaned, profile["voice"], profile["rate"])
        if not audio_file:
            print("TTS generation failed")
            return

        print("\n" + "="*80)
        print("PLAYBACK MODE SELECTION")
        print("="*80)
        print("\nChoose how you want to listen:")
        print("  1. Standard Playback (with controls: pause, rewind, forward, etc.)")
        print("  2. Text Highlighting (follow along as words are highlighted)")
        print("="*80)
        
        playback_choice = input("\nEnter choice (1 or 2, default 1): ").strip()
        
        if playback_choice == "2":
            play_karaoke(audio_file, cleaned)
        else:
            res = play_with_controls(audio_file)
            if res == "highlight":
                play_karaoke(audio_file, cleaned)

        # Save settings with Ctrl+C handling
        try:
            save = input("\nSave these settings for next time? (y/n): ").strip().lower() == "y"
            if save:
                save_profile(profile)
                print("Preferences saved")
        except KeyboardInterrupt:
            print("\nExiting without saving...")
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by Ctrl+C")
        print("Exiting immediately...\n")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by Ctrl+C")
        print("Goodbye!\n")
        sys.exit(0)
