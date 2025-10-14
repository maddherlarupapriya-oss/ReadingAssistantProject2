"""
Flask Web UI - Complete Working Version
Connects to all existing modules
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import os
import json
import sys
from werkzeug.utils import secure_filename
import base64
from datetime import datetime
import webbrowser
import threading
import time
import tempfile

# Get project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Import existing modules
from ocr_module.ocr_module import image_path_to_text, pdf_to_text, docx_to_text
from preprocessing_module.preprocessing_module import preprocess_text
from tts_module.tts_module import generate_audio_with_fallback
from user_profiles.user_profiles import load_profile, save_profile

# Initialize Flask
app = Flask(__name__)
app.secret_key = 'reading_assistant_2024'
app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_ROOT, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf', 'docx', 'bmp', 'tiff'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Data files
USERS_FILE = os.path.join(PROJECT_ROOT, 'users_data.json')
DOCUMENTS_FILE = os.path.join(PROJECT_ROOT, 'documents_data.json')


def load_users():
    """Load users from JSON"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_users(users):
    """Save users to JSON"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def load_documents():
    """Load documents from JSON"""
    if os.path.exists(DOCUMENTS_FILE):
        try:
            with open(DOCUMENTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_documents(documents):
    """Save documents to JSON"""
    with open(DOCUMENTS_FILE, 'w') as f:
        json.dump(documents, f, indent=2)


def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ===== ROUTES =====

@app.route('/')
def index():
    """Home page"""
    if 'user_email' in session:
        return redirect(url_for('upload'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login/Register page"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'message': 'Invalid request'}), 400
            
            action = data.get('action')
            
            users = load_users()
            
            if action == 'register':
                username = data.get('username', '').strip()
                email = data.get('email', '').strip().lower()
                password = data.get('password', '').strip()
                
                if not username or not email or not password:
                    return jsonify({'success': False, 'message': 'All fields required'}), 400
                
                if email in users:
                    return jsonify({'success': False, 'message': 'Email already registered'}), 400
                
                users[email] = {
                    'email': email,
                    'username': username,
                    'password': password,
                    'created_at': datetime.now().isoformat(),
                    'preferences': {
                        'font_size': 18,
                        'reading_speed': 1.0,
                        'highlighting_enabled': True,
                        'line_spacing': 1.8
                    }
                }
                save_users(users)
                session['user_email'] = email
                print(f"[UI] New user registered: {username} ({email})")
                return jsonify({'success': True})
            
            elif action == 'login':
                email = data.get('email', '').strip().lower()
                password = data.get('password', '').strip()
                
                if not email or not password:
                    return jsonify({'success': False, 'message': 'Email and password required'}), 400
                
                if email not in users:
                    return jsonify({'success': False, 'message': 'Account not found'}), 404
                
                if users[email].get('password') != password:
                    return jsonify({'success': False, 'message': 'Incorrect password'}), 401
                
                session['user_email'] = email
                print(f"[UI] User logged in: {users[email]['username']} ({email})")
                return jsonify({'success': True})
            
            else:
                return jsonify({'success': False, 'message': 'Invalid action'}), 400
                
        except Exception as e:
            print(f"[ERROR] Login error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'message': 'Server error'}), 500
    
    # GET - show login page
    try:
        users = load_users()
        last_user_email = None
        last_user_name = None
        
        if users:
            sorted_users = sorted(users.items(), key=lambda x: x[1].get('created_at', ''), reverse=True)
            if sorted_users:
                last_user_email = sorted_users[0][0]
                last_user_name = sorted_users[0][1].get('username', last_user_email)
        
        return render_template('login.html', last_user_email=last_user_email, last_user_name=last_user_name)
    except Exception as e:
        print(f"[ERROR] Login page error: {str(e)}")
        return render_template('login.html', last_user_email=None, last_user_name=None)


@app.route('/quick-login/<email>')
def quick_login(email):
    """Quick login"""
    email = email.strip().lower()
    users = load_users()
    if email in users:
        session['user_email'] = email
        username = users[email].get('username', email)
        print(f"[UI] Quick login: {username}")
        return redirect(url_for('upload'))
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """Logout"""
    email = session.get('user_email')
    session.pop('user_email', None)
    print(f"[UI] User logged out: {email}")
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload page - GET shows page, POST handles uploads"""
    
    # GET request - show upload page
    if request.method == 'GET':
        if 'user_email' not in session:
            return redirect(url_for('login'))
        
        documents = load_documents()
        user_email = session['user_email']
        user_docs = documents.get(user_email, [])
        
        return render_template('upload.html', documents=user_docs, user_email=user_email)
    
    # POST request - handle upload
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        # File upload
        if 'file' in request.files:
            file = request.files['file']
            if not file.filename or not allowed_file(file.filename):
                return jsonify({'success': False, 'message': 'Invalid file'}), 400
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            print(f"[UI->OCR] Processing: {filename}")
            
            ext = filename.rsplit('.', 1)[1].lower()
            handwriting = request.form.get('handwriting', 'false').lower() == 'true'
            
            # Extract text
            if ext in ['png', 'jpg', 'jpeg', 'bmp', 'tiff']:
                raw_text = image_path_to_text(filepath, use_easyocr=handwriting)
            elif ext == 'pdf':
                raw_text = pdf_to_text(filepath, use_easyocr=handwriting)
            elif ext == 'docx':
                raw_text = docx_to_text(filepath)
            else:
                return jsonify({'success': False, 'message': 'Unsupported file'}), 400
            
            print(f"[OCR] Extracted {len(raw_text)} characters")
            cleaned_text = preprocess_text(raw_text)
            
            if not cleaned_text.strip():
                return jsonify({'success': False, 'message': 'No text found'}), 400
            
            # Save document
            doc_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            documents = load_documents()
            user_email = session['user_email']
            
            if user_email not in documents:
                documents[user_email] = []
            
            documents[user_email].append({
                'id': doc_id,
                'title': filename,
                'text': cleaned_text,
                'preview': cleaned_text[:200] + ('...' if len(cleaned_text) > 200 else ''),
                'created_at': datetime.now().isoformat()
            })
            
            save_documents(documents)
            print(f"[UI] Document saved: {doc_id}")
            
            # Clean up
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify({'success': True, 'doc_id': doc_id})
        
        # Pasted text or camera image (JSON)
        elif request.is_json:
            data = request.get_json()
            
            # Pasted text
            if 'text' in data:
                text = data.get('text', '').strip()
                if not text:
                    return jsonify({'success': False, 'message': 'No text provided'}), 400
                
                cleaned_text = preprocess_text(text)
                
                doc_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                documents = load_documents()
                user_email = session['user_email']
                
                if user_email not in documents:
                    documents[user_email] = []
                
                documents[user_email].append({
                    'id': doc_id,
                    'title': 'Pasted Text',
                    'text': cleaned_text,
                    'preview': cleaned_text[:200],
                    'created_at': datetime.now().isoformat()
                })
                
                save_documents(documents)
                print(f"[UI] Pasted text saved: {doc_id}")
                return jsonify({'success': True, 'doc_id': doc_id})
            
            # Camera image (base64)
            elif 'image' in data:
                # Decode base64
                image_data = data['image'].split(',')[1]  # Remove "data:image/jpeg;base64,"
                image_bytes = base64.b64decode(image_data)
                
                # Save to temp file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                temp_file.write(image_bytes)
                temp_file.close()
                
                print(f"[UI->OCR] Processing camera image")
                
                # OCR
                raw_text = image_path_to_text(temp_file.name)
                os.unlink(temp_file.name)
                
                cleaned_text = preprocess_text(raw_text)
                
                if not cleaned_text.strip():
                    return jsonify({'success': False, 'message': 'No text found in image'}), 400
                
                # Save
                doc_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                documents = load_documents()
                user_email = session['user_email']
                
                if user_email not in documents:
                    documents[user_email] = []
                
                documents[user_email].append({
                    'id': doc_id,
                    'title': 'Camera Scan',
                    'text': cleaned_text,
                    'preview': cleaned_text[:200],
                    'created_at': datetime.now().isoformat()
                })
                
                save_documents(documents)
                print(f"[UI] Camera scan saved: {doc_id}")
                return jsonify({'success': True, 'doc_id': doc_id})
        
        return jsonify({'success': False, 'message': 'Invalid request'}), 400
        
    except Exception as e:
        print(f"[ERROR] Upload failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/delete/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete document"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        documents = load_documents()
        user_email = session['user_email']
        
        if user_email in documents:
            documents[user_email] = [doc for doc in documents[user_email] if doc['id'] != doc_id]
            save_documents(documents)
            print(f"[UI] Document deleted: {doc_id}")
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/reader/<doc_id>')
def reader(doc_id):
    """Reader page"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    documents = load_documents()
    user_email = session['user_email']
    user_docs = documents.get(user_email, [])
    
    # Find document
    doc = None
    for d in user_docs:
        if d['id'] == doc_id:
            doc = d
            break
    
    if not doc:
        return "Document not found", 404
    
    # Get user preferences
    users = load_users()
    user_prefs = users.get(user_email, {}).get('preferences', load_profile())
    username = users.get(user_email, {}).get('username', user_email)
    
    return render_template('reader.html', 
                         document=doc, 
                         user_email=user_email,
                         username=username,
                         preferences=user_prefs)

@app.route('/api/generate-audio/<doc_id>')
def generate_audio(doc_id):
    """Generate TTS audio for document"""
    if 'user_email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        # Get document
        documents = load_documents()
        user_email = session['user_email']
        user_docs = documents.get(user_email, [])
        
        doc = None
        for d in user_docs:
            if d['id'] == doc_id:
                doc = d
                break
        
        if not doc:
            return jsonify({'error': 'Document not found'}), 404
        
        # Get voice from query params (speed is handled by Edge TTS rate parameter)
        voice = request.args.get('voice', 'en-US-AriaNeural')
        speed_multiplier = float(request.args.get('speed', '1.0'))
        
        # Convert speed to Edge TTS rate format
        # 1.0 = +0%, 0.5 = -50%, 2.0 = +100%
        rate = f"{int((speed_multiplier - 1.0) * 100):+d}%"
        
        print(f"[TTS] Generating audio: voice={voice}, rate={rate}")
        
        # Generate audio using Edge TTS directly
        import asyncio
        import edge_tts
        
        async def generate_tts():
            output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            output_file.close()
            
            communicate = edge_tts.Communicate(doc['text'], voice, rate=rate)
            await communicate.save(output_file.name)
            
            return output_file.name
        
        audio_path = asyncio.run(generate_tts())
        
        print(f"[TTS] Audio generated: {audio_path}")
        
        if not audio_path or not os.path.exists(audio_path):
            return jsonify({'error': 'Audio generation failed'}), 500
        
        # Send the audio file
        return send_file(
            audio_path,
            mimetype='audio/mpeg',
            as_attachment=False
        )
        
    except Exception as e:
        print(f"[ERROR] Audio generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/word-timings/<doc_id>')
def get_word_timings(doc_id):
    """Get word-level timing data for precise highlighting"""
    if 'user_email' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        # Get document
        documents = load_documents()
        user_email = session['user_email']
        user_docs = documents.get(user_email, [])
        
        doc = None
        for d in user_docs:
            if d['id'] == doc_id:
                doc = d
                break
        
        if not doc:
            return jsonify({'error': 'Document not found'}), 404
        
        voice = request.args.get('voice', 'en-US-AriaNeural')
        speed_multiplier = float(request.args.get('speed', '1.0'))
        rate = f"{int((speed_multiplier - 1.0) * 100):+d}%"
        
        print(f"[TTS] Generating word timings: voice={voice}, rate={rate}")
        
        import asyncio
        import edge_tts
        
        async def get_timings():
            timings = []
            communicate = edge_tts.Communicate(doc['text'], voice, rate=rate)
            
            async for chunk in communicate.stream():
                if chunk["type"] == "WordBoundary":
                    timings.append({
                        'word': chunk['text'],
                        'offset': chunk['offset'] / 10000000,  # Convert to seconds
                        'duration': chunk['duration'] / 10000000
                    })
            
            return timings
        
        timings = asyncio.run(get_timings())
        
        print(f"[TTS] Generated {len(timings)} word timings")
        
        return jsonify({'timings': timings})
        
    except Exception as e:
        print(f"[ERROR] Timing generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'timings': []})


@app.route('/api/edge-voices')
def get_edge_voices():
    """Get all available Edge TTS voices"""
    try:
        import asyncio
        import edge_tts
        
        async def list_voices():
            voices = await edge_tts.list_voices()
            return voices
        
        voices = asyncio.run(list_voices())
        
        # Format voices for dropdown
        voice_list = []
        for v in voices:
            voice_list.append({
                'value': v['ShortName'],
                'label': f"{v['ShortName']} - {v.get('LocalName', v['ShortName'])}"
            })
        
        return jsonify({'voices': voice_list})
        
    except Exception as e:
        print(f"[ERROR] Failed to get voices: {str(e)}")
        return jsonify({'voices': []})

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    """User preferences page"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            users = load_users()
            user_email = session['user_email']
            
            if user_email in users:
                users[user_email]['preferences'] = data
                save_users(users)
                print(f"[UI] Preferences saved for {user_email}")
                return jsonify({'success': True})
            
            return jsonify({'success': False, 'message': 'User not found'}), 404
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # GET - show preferences page
    users = load_users()
    user_email = session['user_email']
    user_prefs = users.get(user_email, {}).get('preferences', load_profile())
    
    return render_template('preferences.html', 
                         preferences=user_prefs, 
                         user_email=user_email)


def open_browser():
    """Open browser after delay"""
    time.sleep(1.5)
    url = 'http://127.0.0.1:5000'
    print(f"\n{'='*60}")
    print(f"🚀 Opening browser at {url}")
    print(f"{'='*60}\n")
    webbrowser.open(url)


def run_app():
    """Run the Flask application"""
    print("\n✓ Flask UI Module Loaded")
    print("✓ Connected to: OCR, Preprocessing, TTS, User Profiles")
    print("✓ Starting server on http://127.0.0.1:5000")
    
    # Start browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run Flask
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)


if __name__ == '__main__':
    run_app()
