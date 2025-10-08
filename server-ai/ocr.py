# ocr.py
import easyocr
from pdf2image import convert_from_path
from PIL import Image
import sys
import os
import json
import argparse
from typing import List, Dict, Union
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize EasyOCR once (lazy loading for better performance)
_reader = None

def get_reader(languages: List[str] = ['en']) -> easyocr.Reader:
    """
    Get or initialize the EasyOCR reader with specified languages.
    Lazy initialization to improve startup time.
    """
    global _reader
    if _reader is None:
        logger.info(f"Initializing EasyOCR reader with languages: {languages}")
        _reader = easyocr.Reader(languages, gpu=False)  # Set gpu=True if CUDA is available
    return _reader


def extract_text_from_image(image_path: str, languages: List[str] = ['en'], 
                           detail: bool = False) -> Union[str, Dict]:
    """
    Extract text from an image (JPG, PNG, etc.)
    
    Args:
        image_path: Path to the image file
        languages: List of language codes (e.g., ['en', 'es', 'fr'])
        detail: If True, return detailed info including confidence scores
        
    Returns:
        Extracted text as string, or dict with detailed information
    """
    try:
        reader = get_reader(languages)
        results = reader.readtext(image_path, detail=1)  # Always get details first
        
        if detail:
            # Return structured data with confidence scores
            extracted_data = []
            for bbox, text, confidence in results:
                extracted_data.append({
                    'text': text,
                    'confidence': float(confidence),
                    'bbox': [[int(coord) for coord in point] for point in bbox]
                })
            return {
                'status': 'success',
                'file': os.path.basename(image_path),
                'text_blocks': extracted_data,
                'full_text': '\n'.join([item['text'] for item in extracted_data])
            }
        else:
            # Return simple text
            return "\n".join([text for (_, text, _) in results])
            
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {str(e)}")
        if detail:
            return {
                'status': 'error',
                'file': os.path.basename(image_path),
                'error': str(e)
            }
        return f"Error processing image: {str(e)}"



def extract_text_from_pdf(pdf_path: str, languages: List[str] = ['en'], 
                         detail: bool = False, dpi: int = 300) -> Union[str, Dict]:
    """
    Extract text from a PDF by converting pages to images
    
    Args:
        pdf_path: Path to the PDF file
        languages: List of language codes
        detail: If True, return detailed info including confidence scores
        dpi: DPI for PDF to image conversion (higher = better quality but slower)
        
    Returns:
        Extracted text as string, or dict with detailed information
    """
    try:
        logger.info(f"Converting PDF to images with DPI={dpi}")
        images = convert_from_path(pdf_path, dpi=dpi)
        logger.info(f"Processing {len(images)} pages from PDF")
        
        reader = get_reader(languages)
        all_text = []
        all_pages_data = []
        
        for page_num, img in enumerate(images, start=1):
            logger.info(f"Processing page {page_num}/{len(images)}")
            results = reader.readtext(img, detail=1)
            
            if detail:
                page_data = []
                for bbox, text, confidence in results:
                    page_data.append({
                        'text': text,
                        'confidence': float(confidence),
                        'bbox': [[int(coord) for coord in point] for point in bbox]
                    })
                all_pages_data.append({
                    'page': page_num,
                    'text_blocks': page_data,
                    'page_text': '\n'.join([item['text'] for item in page_data])
                })
            else:
                all_text.extend([text for (_, text, _) in results])
        
        if detail:
            return {
                'status': 'success',
                'file': os.path.basename(pdf_path),
                'total_pages': len(images),
                'pages': all_pages_data,
                'full_text': '\n'.join([page['page_text'] for page in all_pages_data])
            }
        else:
            return "\n".join(all_text)
            
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
        if detail:
            return {
                'status': 'error',
                'file': os.path.basename(pdf_path),
                'error': str(e)
            }
        return f"Error processing PDF: {str(e)}"



def process_file(file_path: str, languages: List[str] = ['en'], 
                detail: bool = False, dpi: int = 300, use_fallback: bool = False) -> Union[str, Dict]:
    """
    Process a file and extract text based on file type
    
    Args:
        file_path: Path to the file
        languages: List of language codes
        detail: Return detailed information
        dpi: DPI for PDF conversion
        use_fallback: Use fallback processing for higher accuracy (compatibility parameter)
        
    Returns:
        Extracted text or detailed results
    """
    if not os.path.exists(file_path):
        error_msg = f"File does not exist: {file_path}"
        logger.error(error_msg)
        if detail:
            return {'status': 'error', 'error': error_msg}
        return error_msg

    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif', '.webp']:
        return extract_text_from_image(file_path, languages, detail)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path, languages, detail, dpi)
    else:
        error_msg = f"Unsupported file type: {ext}"
        logger.warning(error_msg)
        if detail:
            return {'status': 'error', 'error': error_msg}
        return error_msg


def batch_process(file_paths: List[str], languages: List[str] = ['en'], 
                 detail: bool = False, dpi: int = 300, use_fallback: bool = False) -> Dict:
    """
    Process multiple files in batch
    
    Args:
        file_paths: List of file paths to process
        languages: List of language codes
        detail: Return detailed information
        dpi: DPI for PDF conversion
        use_fallback: Use fallback processing for higher accuracy (compatibility parameter)
        
    Returns:
        Dict containing results for all files
    """
    results = {
        'total_files': len(file_paths),
        'processed': 0,
        'failed': 0,
        'files': []
    }
    
    for file_path in file_paths:
        logger.info(f"Processing file: {file_path}")
        result = process_file(file_path, languages, detail=True, dpi=dpi, use_fallback=use_fallback)
        
        if isinstance(result, dict) and result.get('status') == 'success':
            results['processed'] += 1
        else:
            results['failed'] += 1
            
        results['files'].append(result)
    
    return results


def main():
    """
    Main function to be called from command line or Node.js
    Enhanced with argument parsing and multiple output formats
    """
    parser = argparse.ArgumentParser(
        description='OCR tool for extracting text from images and PDFs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ocr.py image.png
  python ocr.py document.pdf --json
  python ocr.py image.jpg --languages en es --detail
  python ocr.py document.pdf --dpi 400 --json
  python ocr.py file1.png file2.pdf --batch --json
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        help='Path to image or PDF file(s) to process'
    )
    
    parser.add_argument(
        '--languages', '-l',
        nargs='+',
        default=['en'],
        help='Languages to detect (e.g., en es fr de). Default: en'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    parser.add_argument(
        '--detail',
        action='store_true',
        help='Include detailed information (confidence scores, bounding boxes)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='DPI for PDF to image conversion (default: 300)'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process multiple files in batch mode'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file path (optional). If not specified, prints to stdout'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--use-fallback',
        action='store_true',
        help='Use fallback processing for higher accuracy (compatibility option)'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    
    # Process files
    if args.batch or len(args.files) > 1:
        result = batch_process(args.files, args.languages, args.detail or args.json, args.dpi, args.use_fallback)
        output = json.dumps(result, indent=2) if args.json else result.get('full_text', str(result))
    else:
        file_path = args.files[0]
        result = process_file(file_path, args.languages, args.detail or args.json, args.dpi, args.use_fallback)
        
        if args.json:
            output = json.dumps(result, indent=2) if isinstance(result, dict) else json.dumps({'text': result})
        else:
            output = result.get('full_text', result) if isinstance(result, dict) else result
    
    # Output results
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(str(output))
            logger.info(f"Results written to {args.output}")
        except Exception as e:
            logger.error(f"Error writing to file: {str(e)}")
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()

