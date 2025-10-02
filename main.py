# main.py
from input_module.input_module import get_input_choice, capture_images_from_camera, load_file, read_pasted_text
from ocr_module.ocr_module import image_path_to_text, pdf_to_text, docx_to_text
from preprocessing_module.preprocessing_module import preprocess_text
from tts_module.tts_module import generate_audio_with_fallback, play_with_controls, play_karaoke
from ui_module.ui_module import show_preview
from user_profiles.user_profiles import load_profile, save_profile


def main():
    opt = get_input_choice()
    if opt is None:
        return
    if opt == "1":
        fname = input("Enter file name: ").strip()
        kind, path = load_file(fname)
        if kind == "image":
            raw = image_path_to_text(path)
        elif kind == "pdf":
            raw = pdf_to_text(path)
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
        parts = []
        for p in imgs:
            parts.append(image_path_to_text(p))
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
        "1": "en-US-AriaNeural",
        "2": "en-US-GuyNeural",
        "3": "en-GB-LibbyNeural",
        "4": "en-IN-NeerjaNeural",
        "5": "en-IN-PrabhatNeural"
    }
    print("\nAvailable Voices:")
    for k, v in voices.items():
        print(k, v)
    vchoice = input("Choose voice number (enter to keep saved): ").strip()
    if vchoice in voices:
        profile["voice"] = voices[vchoice]
    rchoice = input("Enter speech speed (+20% / -20% / 0 for normal, enter to keep saved): ").strip()
    if rchoice:
        if rchoice == "0":
            profile["rate"] = "+0%"
        elif not rchoice.endswith("%"):
            profile["rate"] = f"{rchoice}%"
        else:
            profile["rate"] = rchoice

    audio_file, engine_used = generate_audio_with_fallback(cleaned, profile["voice"], profile["rate"])
    if not audio_file:
        print("TTS generation failed")
        return

    use_k = input("Play with karaoke highlighting? (y/n, default n): ").strip().lower() == "y"
    if use_k:
        play_karaoke(audio_file, cleaned)
    else:
        res = play_with_controls(audio_file)
        if res == "karaoke":
            play_karaoke(audio_file, cleaned)

    save = input("Save these settings for next time? (y/n): ").strip().lower() == "y"
    if save:
        save_profile(profile)
        print("Preferences saved")

if __name__ == "__main__":
    main()