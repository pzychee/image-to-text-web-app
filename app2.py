from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pytesseract
import base64
import os
from gtts import gTTS
from deep_translator import GoogleTranslator
from googletrans import LANGUAGES
import io
import warnings
import tempfile

# Suppress matplotlib warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure pytesseract path - update this based on your installation
#pytesseract.pytesseract.tesseract_cmd = r'F:\project\CODE\Tesseract-OCR\tesseract.exe'
# You can add this to check the environment if needed:
import platform
if platform.system() == 'Windows':
    # For local Windows development only
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Get language options for dropdowns
    language_names = list(LANGUAGES.values())
    language_codes = list(LANGUAGES.keys())
    
    # Convert to list of tuples for easier handling in the template
    languages = list(zip(language_codes, language_names))
    
    return render_template('index.html', languages=languages)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Save uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        try:
            # Use PIL (Pillow) directly instead of matplotlib
            from PIL import Image
            img = Image.open(filename)
            
            # Extract text from image using the PIL image
            extracted_text = pytesseract.image_to_string(img, lang='eng')
            
            # Store text in session or temp file
            temp_text_file = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_text.txt')
            with open(temp_text_file, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            
            return jsonify({
                'success': True,
                'image_path': filename,
                'extracted_text': extracted_text
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': False, 'error': 'Invalid file'})

@app.route('/translate', methods=['POST'])
def translate_text():
    text = request.form.get('text')
    source_lang = request.form.get('source_lang')
    target_lang = request.form.get('target_lang')
    
    if not text or not source_lang or not target_lang:
        return jsonify({'success': False, 'error': 'Missing parameters'})
    
    try:
        translated_text = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return jsonify({
            'success': True,
            'translated_text': translated_text
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.form.get('text')
    lang = request.form.get('lang')
    
    if not text or not lang:
        return jsonify({'success': False, 'error': 'Missing parameters'})
    
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to a temporary file
        speech_file = os.path.join(app.config['UPLOAD_FOLDER'], 'speech.mp3')
        tts.save(speech_file)
        
        return jsonify({
            'success': True,
            'audio_path': speech_file
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download-audio')
def download_audio():
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'speech.mp3')
    return send_file(audio_path, as_attachment=True, download_name='translated_speech.mp3')
@app.route('/debug-tesseract')
def debug_tesseract():
    import shutil
    tesseract_path = shutil.which('tesseract')
    return jsonify({'tesseract_path': tesseract_path})

if __name__ == '__main__':
    app.run(debug=True)