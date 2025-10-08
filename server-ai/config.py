# config.py
"""
Configuration file for OCR service
"""
import os

# Google Generative AI Configuration
GENAI_API_KEY = os.getenv('GENAI_API_KEY', "AIzaSyDihLWQIt3Dp9Mw5QldrhNj9NMKpoUv-jE")

# OCR Quality Thresholds
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
MIN_TEXT_LENGTH = int(os.getenv('MIN_TEXT_LENGTH', '10'))

# EasyOCR Configuration
USE_GPU = os.getenv('USE_GPU', 'false').lower() == 'true'

# PDF Processing Configuration
DEFAULT_DPI = int(os.getenv('DEFAULT_DPI', '300'))

# Fallback Configuration
ENABLE_FALLBACK = os.getenv('ENABLE_FALLBACK', 'true').lower() == 'true'

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')