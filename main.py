"""
Reading Assistant - Main Entry Point
Launches the web-based UI with all integrated modules
"""

import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

def main():
    """Main entry point - launches web UI"""
    print("\n" + "="*70)
    print("📖 READING ASSISTANT - STARTING WEB APPLICATION")
    print("="*70)
    
    try:
        # Import and run the Flask UI module
        from ui_module.ui_flask import run_app
        
        print("\n✓ Modules loaded successfully")
        print("✓ Launching web interface...")
        print("\nThe application will open in your default browser.")
        print("If it doesn't open automatically, visit: http://127.0.0.1:5000")
        print("\nPress Ctrl+C to stop the server.")
        print("="*70 + "\n")
        
        # Run the web application
        run_app()
        
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("👋 Shutting down Reading Assistant")
        print("="*70 + "\n")
        sys.exit(0)
    except ImportError as e:
        print(f"\n❌ ERROR: Could not import required modules")
        print(f"   Details: {str(e)}")
        print("\n   Make sure you have installed all dependencies:")
        print("   pip install flask edge-tts pyttsx3 pygame Pillow pdf2image python-docx opencv-python pytesseract")
        print("\n   Optional: pip install easyocr")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()