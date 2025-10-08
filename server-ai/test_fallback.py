"""
Example script demonstrating the OCR fallback functionality
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from ocr import process_file, extract_text_from_image
import json

def create_low_quality_image(output_path='low_quality_test.png'):
    """Create a low quality image that might trigger fallback"""
    # Create a small, blurry image with low contrast text
    img = Image.new('RGB', (200, 100), color=(240, 240, 240))  # Light gray background
    draw = ImageDraw.Draw(img)
    
    # Use small, light gray text (low contrast)
    try:
        font = ImageFont.truetype("arial.ttf", 8)  # Very small font
    except:
        font = ImageFont.load_default()
    
    # Draw light gray text on light gray background (poor contrast)
    draw.text((10, 10), "Low quality text", fill=(200, 200, 200), font=font)
    draw.text((10, 30), "Blurry content", fill=(180, 180, 180), font=font)
    draw.text((10, 50), "Hard to read", fill=(190, 190, 190), font=font)
    
    # Make it blurry
    img = img.resize((100, 50))  # Downsize
    img = img.resize((200, 100))  # Upsize to make it blurry
    
    img.save(output_path)
    print(f"✓ Created low quality test image: {output_path}")
    return output_path

def create_high_quality_image(output_path='high_quality_test.png'):
    """Create a high quality image that should work well with EasyOCR"""
    img = Image.new('RGB', (800, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Draw clear black text on white background
    draw.text((50, 50), "High Quality Text", fill='black', font=font)
    draw.text((50, 100), "Clear and Readable", fill='black', font=font)
    
    img.save(output_path)
    print(f"✓ Created high quality test image: {output_path}")
    return output_path

def test_fallback():
    """Test the fallback functionality"""
    print("=" * 60)
    print("OCR Fallback Functionality Test")
    print("=" * 60)
    
    # Create test images
    low_quality_img = create_low_quality_image()
    high_quality_img = create_high_quality_image()
    
    print("\n1. Testing HIGH QUALITY image (should use EasyOCR):")
    print("-" * 50)
    result_hq = process_file(high_quality_img, detail=True, use_fallback=True)
    if isinstance(result_hq, dict):
        print(f"Method used: {result_hq.get('method', 'unknown')}")
        print(f"Fallback used: {result_hq.get('fallback_used', False)}")
        if 'average_confidence' in result_hq:
            print(f"Average confidence: {result_hq['average_confidence']:.3f}")
        print(f"Extracted text: {result_hq.get('text', result_hq.get('full_text', 'No text'))}")
    
    print("\n2. Testing LOW QUALITY image (might trigger fallback):")
    print("-" * 50)
    result_lq = process_file(low_quality_img, detail=True, use_fallback=True)
    if isinstance(result_lq, dict):
        print(f"Method used: {result_lq.get('method', 'unknown')}")
        print(f"Fallback used: {result_lq.get('fallback_used', False)}")
        if 'average_confidence' in result_lq:
            print(f"Average confidence: {result_lq.get('average_confidence', 'N/A')}")
        if 'original_confidence' in result_lq:
            print(f"Original EasyOCR confidence: {result_lq['original_confidence']:.3f}")
        print(f"Extracted text: {result_lq.get('text', result_lq.get('full_text', 'No text'))}")
    
    print("\n3. Testing with fallback DISABLED:")
    print("-" * 50)
    result_no_fallback = process_file(low_quality_img, detail=True, use_fallback=False)
    if isinstance(result_no_fallback, dict):
        print(f"Method used: {result_no_fallback.get('method', 'unknown')}")
        print(f"Fallback used: {result_no_fallback.get('fallback_used', False)}")
        if 'average_confidence' in result_no_fallback:
            print(f"Average confidence: {result_no_fallback['average_confidence']:.3f}")
        print(f"Extracted text: {result_no_fallback.get('text', result_no_fallback.get('full_text', 'No text'))}")
    
    # Clean up
    import time
    time.sleep(1)  # Give some time for file handles to be released
    
    for img_path in [low_quality_img, high_quality_img]:
        if os.path.exists(img_path):
            try:
                os.remove(img_path)
            except PermissionError:
                print(f"Warning: Could not delete {img_path} - file in use")
    
    print("\n✓ Test completed. Check if fallback was triggered for low quality image.")

if __name__ == "__main__":
    test_fallback()