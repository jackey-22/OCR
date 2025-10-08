// Simple API utility for Flask OCR service
const API_BASE_URL = 'http://localhost:5000/api';

export async function processOCR(files, options = {}) {
  try {
    const formData = new FormData();
    
    // Add files
    files.forEach(file => {
      formData.append('files', file);
    });
    
    // Add options
    formData.append('languages', JSON.stringify(options.languages || ['en']));
    formData.append('useHighAccuracy', options.useHighAccuracy || 'true');
    formData.append('confidenceThreshold', options.confidenceThreshold || '0.7');
    
    const response = await fetch(`${API_BASE_URL}/process`, {
      method: 'POST',
      body: formData, // Don't set Content-Type, let browser set it for FormData
    });
    
    const result = await response.json();
    return result;
    
  } catch (error) {
    console.error('OCR API Error:', error);
    return {
      success: false,
      error: `Connection failed: ${error.message}`
    };
  }
}

export async function quickExtract(file, languages = ['en']) {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('languages', languages.join(','));
    
    const response = await fetch(`${API_BASE_URL}/quick`, {
      method: 'POST',
      body: formData,
    });
    
    const result = await response.json();
    return result;
    
  } catch (error) {
    console.error('Quick Extract Error:', error);
    return {
      success: false,
      error: `Connection failed: ${error.message}`
    };
  }
}

export async function getLanguages() {
  try {
    const response = await fetch(`${API_BASE_URL}/languages`);
    const result = await response.json();
    return result;
    
  } catch (error) {
    console.error('Get Languages Error:', error);
    return {
      success: false,
      error: `Connection failed: ${error.message}`
    };
  }
}

export async function healthCheck() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const result = await response.json();
    return result;
    
  } catch (error) {
    console.error('Health Check Error:', error);
    return {
      success: false,
      error: `Connection failed: ${error.message}`
    };
  }
}