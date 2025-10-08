"""
Flask API for OCR Service
Simple and direct API for the OCR functionality
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
import json
from ocr import process_file, batch_process
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'OCR API',
        'version': '1.0.0'
    })

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    languages = {
        'en': 'English',
        'es': 'Spanish', 
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ar': 'Arabic',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'hi': 'Hindi'
    }
    return jsonify({
        'success': True,
        'languages': languages
    })

@app.route('/api/process', methods=['POST'])
def process_files():
    """Main OCR processing endpoint"""
    try:
        # Check if files are present
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files uploaded'
            }), 400

        files = request.files.getlist('files')
        if not files or files[0].filename == '':
            return jsonify({
                'success': False,
                'error': 'No files selected'
            }), 400

        # Get processing options
        languages = json.loads(request.form.get('languages', '["en"]'))
        use_high_accuracy = request.form.get('useHighAccuracy', 'true').lower() == 'true'
        confidence_threshold = float(request.form.get('confidenceThreshold', '0.7'))
        
        # Process files
        temp_files = []
        try:
            # Save uploaded files temporarily
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}")
                    file.save(temp_file.name)
                    temp_files.append(temp_file.name)

            if not temp_files:
                return jsonify({
                    'success': False,
                    'error': 'No valid files to process'
                }), 400

            # Process with OCR
            if len(temp_files) == 1:
                # Single file processing
                result = process_file(
                    temp_files[0],
                    languages=languages,
                    detail=True,
                    use_fallback=use_high_accuracy
                )
            else:
                # Batch processing
                result = batch_process(
                    temp_files,
                    languages=languages,
                    detail=True,
                    use_fallback=use_high_accuracy
                )

            # Format response
            if isinstance(result, dict):
                if result.get('status') == 'success':
                    extracted_text = result.get('text') or result.get('full_text') or ''
                    return jsonify({
                        'success': True,
                        'data': {
                            'extractedText': extracted_text,
                            'method': result.get('method', 'easyocr'),
                            'confidence': result.get('confidence') or result.get('average_confidence'),
                            'fallback_used': result.get('fallback_used', False),
                            'details': result
                        }
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': result.get('error', 'Processing failed')
                    }), 500
            else:
                # Plain text result
                return jsonify({
                    'success': True,
                    'data': {
                        'extractedText': str(result),
                        'method': 'easyocr',
                        'fallback_used': False
                    }
                })

        finally:
            # Clean up temporary files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except OSError:
                    pass

    except Exception as e:
        logger.error(f"OCR processing error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Processing failed: {str(e)}'
        }), 500

@app.route('/api/quick', methods=['POST'])
def quick_extract():
    """Quick text extraction endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type'
            }), 400

        # Get options
        languages = request.form.get('languages', 'en').split(',')
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}")
        file.save(temp_file.name)

        try:
            # Quick processing
            result = process_file(
                temp_file.name,
                languages=languages,
                detail=False,
                use_fallback=False
            )

            return jsonify({
                'success': True,
                'text': str(result)
            })

        finally:
            # Clean up
            try:
                os.unlink(temp_file.name)
            except OSError:
                pass

    except Exception as e:
        logger.error(f"Quick extract error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Extraction failed: {str(e)}'
        }), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 50MB.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting OCR Flask API...")
    print("📍 API will be available at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("📋 Process files: POST http://localhost:5000/api/process")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )