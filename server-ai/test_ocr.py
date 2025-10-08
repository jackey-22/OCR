"""
OCR Service Test Suite
Run tests to verify OCR functionality
"""

import os
import sys
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_test_image(output_path='test_image.png'):
    """Create a simple test image with text"""
    # Create a white image
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add text
    try:
        # Try to use a decent font
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        # Fall back to default font
        font = ImageFont.load_default()
    
    # Draw text
    text_lines = [
        "Hello World!",
        "This is a test image",
        "for OCR processing.",
        "Testing 123456"
    ]
    
    y_position = 50
    for line in text_lines:
        draw.text((50, y_position), line, fill='black', font=font)
        y_position += 80
    
    # Save image
    img.save(output_path)
    print(f"✓ Created test image: {output_path}")
    return output_path

def run_test(description, command):
    """Run a test command and display results"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    print(f"Command: {command}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✓ SUCCESS")
            print("\nOutput:")
            print(result.stdout)
            return True
        else:
            print("✗ FAILED")
            print("\nError:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ TIMEOUT - Test took too long")
        return False
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("OCR Service Test Suite")
    print("=" * 60)
    
    # Create test image
    test_image = create_test_image()
    
    tests = [
        {
            'name': 'Basic Text Extraction',
            'command': f'python ocr.py {test_image}'
        },
        {
            'name': 'JSON Output',
            'command': f'python ocr.py {test_image} --json'
        },
        {
            'name': 'Detailed Output with Confidence Scores',
            'command': f'python ocr.py {test_image} --json --detail'
        },
        {
            'name': 'Multi-language Detection',
            'command': f'python ocr.py {test_image} --languages en es'
        },
        {
            'name': 'Verbose Logging',
            'command': f'python ocr.py {test_image} --verbose'
        },
        {
            'name': 'Help Command',
            'command': 'python ocr.py --help'
        }
    ]
    
    results = []
    for test in tests:
        success = run_test(test['name'], test['command'])
        results.append({'test': test['name'], 'passed': success})
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for r in results if r['passed'])
    total = len(results)
    
    for result in results:
        status = "✓ PASS" if result['passed'] else "✗ FAIL"
        print(f"{status} - {result['test']}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    # Clean up
    if os.path.exists(test_image):
        os.remove(test_image)
        print(f"\n✓ Cleaned up test files")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
