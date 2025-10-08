/**
 * OCR Service Integration Module
 * Provides Node.js interface to the Python OCR service
 */

const { spawn } = require('child_process');
const path = require('path');

class OCRService {
  constructor(pythonPath = 'python', scriptPath = path.join(__dirname, 'ocr.py')) {
    this.pythonPath = pythonPath;
    this.scriptPath = scriptPath;
  }

  /**
   * Extract text from a file (image or PDF)
   * @param {string} filePath - Path to the file
   * @param {Object} options - OCR options
   * @param {string[]} options.languages - Languages to detect (default: ['en'])
   * @param {boolean} options.detail - Include confidence scores and bounding boxes
   * @param {number} options.dpi - DPI for PDF conversion (default: 300)
   * @param {boolean} options.json - Return JSON format
   * @returns {Promise<string|Object>} - Extracted text or detailed results
   */
  extractText(filePath, options = {}) {
    return new Promise((resolve, reject) => {
      const args = [this.scriptPath, filePath];

      // Add optional arguments
      if (options.languages && Array.isArray(options.languages)) {
        args.push('--languages', ...options.languages);
      }

      if (options.detail) {
        args.push('--detail');
      }

      if (options.json || options.detail) {
        args.push('--json');
      }

      if (options.dpi) {
        args.push('--dpi', options.dpi.toString());
      }

      const python = spawn(this.pythonPath, args);
      let output = '';
      let errorOutput = '';

      python.stdout.on('data', (data) => {
        output += data.toString();
      });

      python.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      python.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(errorOutput || `OCR process exited with code ${code}`));
          return;
        }

        try {
          // Try to parse as JSON if requested
          if (options.json || options.detail) {
            const result = JSON.parse(output);
            resolve(result);
          } else {
            resolve(output.trim());
          }
        } catch (e) {
          // If JSON parsing fails, return raw output
          resolve(output.trim());
        }
      });

      python.on('error', (error) => {
        reject(new Error(`Failed to start OCR process: ${error.message}`));
      });
    });
  }

  /**
   * Extract text from multiple files in batch
   * @param {string[]} filePaths - Array of file paths
   * @param {Object} options - OCR options
   * @returns {Promise<Object>} - Batch processing results
   */
  extractTextBatch(filePaths, options = {}) {
    return new Promise((resolve, reject) => {
      const args = [this.scriptPath, ...filePaths, '--batch', '--json'];

      // Add optional arguments
      if (options.languages && Array.isArray(options.languages)) {
        args.push('--languages', ...options.languages);
      }

      if (options.detail) {
        args.push('--detail');
      }

      if (options.dpi) {
        args.push('--dpi', options.dpi.toString());
      }

      const python = spawn(this.pythonPath, args);
      let output = '';
      let errorOutput = '';

      python.stdout.on('data', (data) => {
        output += data.toString();
      });

      python.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      python.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(errorOutput || `OCR process exited with code ${code}`));
          return;
        }

        try {
          const result = JSON.parse(output);
          resolve(result);
        } catch (e) {
          reject(new Error('Failed to parse batch results'));
        }
      });

      python.on('error', (error) => {
        reject(new Error(`Failed to start OCR process: ${error.message}`));
      });
    });
  }

  /**
   * Quick text extraction without details (faster)
   * @param {string} filePath - Path to the file
   * @param {string[]} languages - Languages to detect
   * @returns {Promise<string>} - Extracted text
   */
  async quickExtract(filePath, languages = ['en']) {
    return this.extractText(filePath, { languages });
  }

  /**
   * Detailed extraction with confidence scores and bounding boxes
   * @param {string} filePath - Path to the file
   * @param {string[]} languages - Languages to detect
   * @returns {Promise<Object>} - Detailed extraction results
   */
  async detailedExtract(filePath, languages = ['en']) {
    return this.extractText(filePath, { languages, detail: true, json: true });
  }

  /**
   * Extract text from PDF with custom DPI
   * @param {string} pdfPath - Path to the PDF file
   * @param {number} dpi - DPI for conversion (default: 300)
   * @param {string[]} languages - Languages to detect
   * @returns {Promise<string>} - Extracted text
   */
  async extractFromPDF(pdfPath, dpi = 300, languages = ['en']) {
    return this.extractText(pdfPath, { languages, dpi });
  }
}

// Export the class and a default instance
module.exports = OCRService;

// Convenience export
module.exports.default = new OCRService();

// Example usage (uncomment to test):
/*
const ocrService = new OCRService();

// Simple extraction
ocrService.quickExtract('image.png')
  .then(text => console.log('Extracted text:', text))
  .catch(err => console.error('Error:', err));

// Detailed extraction
ocrService.detailedExtract('image.png', ['en', 'es'])
  .then(result => {
    console.log('Status:', result.status);
    console.log('Full text:', result.full_text);
    console.log('Text blocks:', result.text_blocks);
  })
  .catch(err => console.error('Error:', err));

// Batch processing
ocrService.extractTextBatch(['file1.png', 'file2.pdf'], { languages: ['en'] })
  .then(result => {
    console.log('Total files:', result.total_files);
    console.log('Processed:', result.processed);
    console.log('Failed:', result.failed);
  })
  .catch(err => console.error('Error:', err));

// PDF extraction
ocrService.extractFromPDF('document.pdf', 400, ['en', 'fr'])
  .then(text => console.log('PDF text:', text))
  .catch(err => console.error('Error:', err));
*/
