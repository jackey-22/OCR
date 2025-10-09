import { useState, useRef } from 'react';
import { Button } from 'primereact/button';
import { FileUpload } from 'primereact/fileupload';
import { Card } from 'primereact/card';
import { ProgressBar } from 'primereact/progressbar';
import { Dropdown } from 'primereact/dropdown';
import { InputSwitch } from 'primereact/inputswitch';
import { Toast } from 'primereact/toast';
import { Dialog } from 'primereact/dialog';
import { ScrollPanel } from 'primereact/scrollpanel';
import { Chip } from 'primereact/chip';
import { Divider } from 'primereact/divider';
import { FiUpload, FiImage, FiFileText, FiDownload, FiEye, FiSettings } from 'react-icons/fi';
// import { processOCR, getLanguages, healthCheck } from '../utils/ocr.api';
import { processOCR } from '../utils/ocr.api';

function Home() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [extractedText, setExtractedText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [selectedLanguages, setSelectedLanguages] = useState(['en']);
  const [useHighAccuracy, setUseHighAccuracy] = useState(true);
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.7);
  const [results, setResults] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  
  const toast = useRef(null);
  const fileUploadRef = useRef(null);

  // Language options
  const languages = [
    { label: 'English', value: 'en' },
    { label: 'Spanish', value: 'es' },
    { label: 'French', value: 'fr' },
    { label: 'German', value: 'de' },
    { label: 'Italian', value: 'it' },
    { label: 'Portuguese', value: 'pt' },
    { label: 'Russian', value: 'ru' },
    { label: 'Chinese', value: 'zh' },
    { label: 'Japanese', value: 'ja' },
    { label: 'Korean', value: 'ko' }
  ];

  // Confidence threshold options
  const thresholdOptions = [
    { label: 'Low (0.5)', value: 0.5 },
    { label: 'Medium (0.7)', value: 0.7 },
    { label: 'High (0.8)', value: 0.8 },
    { label: 'Very High (0.9)', value: 0.9 }
  ];

  const handleFileSelect = (event) => {
    const files = Array.from(event.files);
    setSelectedFiles(files);
    
    if (files.length > 0) {
      toast.current.show({
        severity: 'info',
        summary: 'Files Selected',
        detail: `${files.length} file(s) ready for processing`,
        life: 3000
      });
    }
  };

  const processFiles = async () => {
    if (selectedFiles.length === 0) {
      toast.current.show({
        severity: 'warn',
        summary: 'No Files',
        detail: 'Please select files to process',
        life: 3000
      });
      return;
    }

    setIsProcessing(true);
    setProgress(0);
    setExtractedText('');
    setResults(null);

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 500);

      // Call Flask OCR API
      const response = await processOCR(selectedFiles, {
        languages: selectedLanguages,
        useHighAccuracy: useHighAccuracy,
        confidenceThreshold: confidenceThreshold
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (response && response.success) {
        setResults(response.data);
        setExtractedText(response.data.extractedText || response.data.text || response.data.full_text || '');
        setShowResults(true);
        
        toast.current.show({
          severity: 'success',
          summary: 'Processing Complete',
          detail: `Text extracted successfully from ${selectedFiles.length} file(s)`,
          life: 5000
        });
      } else {
        throw new Error(response?.message || 'OCR processing failed');
      }

    } catch (error) {
      console.error('OCR Error:', error);
      toast.current.show({
        severity: 'error',
        summary: 'Processing Failed',
        detail: error.message || 'Failed to process files',
        life: 5000
      });
    } finally {
      setIsProcessing(false);
      setTimeout(() => setProgress(0), 1000);
    }
  };

  const downloadText = () => {
    if (!extractedText) return;
    
    const blob = new Blob([extractedText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `extracted-text-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = () => {
    if (extractedText) {
      navigator.clipboard.writeText(extractedText);
      toast.current.show({
        severity: 'success',
        summary: 'Copied',
        detail: 'Text copied to clipboard',
        life: 2000
      });
    }
  };

  const clearAll = () => {
    setSelectedFiles([]);
    setExtractedText('');
    setResults(null);
    setShowResults(false);
    setProgress(0);
    fileUploadRef.current?.clear();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-2 sm:p-4 md:p-6">
      <Toast ref={toast} />
      
      <div className="max-w-6xl mx-auto space-y-4 sm:space-y-6">
        {/* Header */}
        <div className="text-center py-4 sm:py-6 md:py-8">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-800 mb-2 sm:mb-4 px-4">
            AI-Powered OCR System
          </h1>
          <p className="text-sm sm:text-base md:text-lg text-gray-600 max-w-2xl mx-auto px-4">
            Extract text from images (JPG/JPEG or PNG) with advanced AI technology.
          </p>
        </div>

        {/* Main Content */}
        <div className="grid gap-4 sm:gap-6">
          {/* Upload Section */}
          <div className="lg:col-span-2">
            <Card className="h-full">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-2">
                <h2 className="text-lg sm:text-xl font-semibold flex items-center gap-2">
                  <FiUpload className="text-blue-600" />
                  Upload Files
                </h2>
                {/* <Button
                  icon={<FiSettings />}
                  label="Settings"
                  outlined
                  size="small"
                  onClick={() => setShowSettings(true)}
                /> */}
              </div>

              <FileUpload
                ref={fileUploadRef}
                name="files"
                multiple
                accept="image/*"
                maxFileSize={10000000} // 10MB
                onSelect={handleFileSelect}
                chooseLabel="Choose Files from Device"
                chooseOptions={{ icon: 'pi pi-upload', className: 'p-button-outlined' }}
                emptyTemplate={
                  <div className="text-center p-4 sm:p-6 md:p-8">
                    <FiImage className="mx-auto text-3xl sm:text-4xl text-gray-400 mb-3 sm:mb-4" />
                    <p className="text-sm sm:text-base text-gray-500 mb-2">Drag and drop files here or click the button above</p>
                    <p className="text-xs sm:text-sm text-gray-400">
                      Supports: JPG, PNG, GIF, BMP (max 10MB each)
                    </p>
                  </div>
                }
                headerTemplate={(options) => {
                  const { chooseButton } = options;
                  return (
                    <div className="flex justify-center mb-4">
                      {chooseButton}
                    </div>
                  );
                }}
                itemTemplate={(file, props) => (
                  <div className="flex items-center justify-between p-2 sm:p-3 border rounded-lg mb-2">
                    <div className="flex items-center gap-2 sm:gap-3 flex-1 min-w-0">
                      <FiFileText className="text-blue-600 flex-shrink-0" />
                      <div className="min-w-0 flex-1">
                        <p className="font-medium text-sm sm:text-base truncate">{file.name}</p>
                        <p className="text-xs sm:text-sm text-gray-500">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                    </div>
                    <Button
                      icon="pi pi-times"
                      className="p-button-text p-button-danger p-button-sm flex-shrink-0"
                      onClick={() => props.onRemove()}
                    />
                  </div>
                )}
              />

              {selectedFiles.length > 0 && (
                <div className="mt-3 sm:mt-4 space-y-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <Chip 
                      label={`${selectedFiles.length} file(s) selected`}
                      className="bg-blue-100 text-blue-800 text-xs sm:text-sm"
                    />
                    {/* {useHighAccuracy && (
                      <Chip 
                        label="High Accuracy Mode"
                        className="bg-green-100 text-green-800"
                      />
                    )} */}
                  </div>
                  
                  {isProcessing && (
                    <div>
                      <div className="flex justify-between text-xs sm:text-sm mb-1">
                        <span>Processing...</span>
                        <span>{progress}%</span>
                      </div>
                      <ProgressBar value={progress} className="h-2" />
                    </div>
                  )}

                  <div className="flex flex-col sm:flex-row gap-2">
                    <Button
                      label="Process Files"
                      icon={<FiEye />}
                      onClick={processFiles}
                      disabled={isProcessing}
                      className="flex-1 text-sm sm:text-base"
                    />
                    <Button
                      label="Clear"
                      icon="pi pi-trash"
                      outlined
                      onClick={clearAll}
                      disabled={isProcessing}
                      className="sm:w-auto text-sm sm:text-base"
                    />
                  </div>
                </div>
              )}
            </Card>
          </div>

          {/* Settings Panel
          <div>
            <Card>
              <h3 className="text-lg font-semibold mb-4">Quick Settings</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Languages</label>
                  <Dropdown
                    value={selectedLanguages}
                    options={languages}
                    onChange={(e) => setSelectedLanguages(e.value)}
                    placeholder="Select languages"
                    multiple
                    className="w-full"
                  />
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">High Accuracy Mode</span>
                  <InputSwitch
                    checked={useHighAccuracy}
                    onChange={(e) => setUseHighAccuracy(e.value)}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">
                    Confidence Threshold
                  </label>
                  <Dropdown
                    value={confidenceThreshold}
                    options={thresholdOptions}
                    onChange={(e) => setConfidenceThreshold(e.value)}
                    className="w-full"
                  />
                </div>
              </div>
            </Card>
          </div> */}
        </div>

        {/* Results Section */}
        {extractedText && (
          <Card>
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-3">
              <h3 className="text-base sm:text-lg font-semibold flex items-center gap-2">
                <FiFileText className="text-green-600" />
                Extracted Text
              </h3>
              <div className="flex flex-wrap gap-2 w-full sm:w-auto">
                <Button
                  icon="pi pi-copy"
                  label="Copy"
                  outlined
                  size="small"
                  onClick={copyToClipboard}
                  className="flex-1 sm:flex-none text-xs sm:text-sm"
                />
                <Button
                  icon={<FiDownload />}
                  label="Download"
                  outlined
                  size="small"
                  onClick={downloadText}
                  className="flex-1 sm:flex-none text-xs sm:text-sm"
                />
                <Button
                  icon={<FiEye />}
                  label="Details"
                  outlined
                  size="small"
                  onClick={() => setShowResults(true)}
                  className="flex-1 sm:flex-none text-xs sm:text-sm"
                />
              </div>
            </div>
            
            <div className="bg-gray-50 p-3 sm:p-4 rounded-lg border">
              <ScrollPanel style={{ width: '100%', height: '200px' }}>
                <pre className="whitespace-pre-wrap text-xs sm:text-sm font-mono">
                  {extractedText}
                </pre>
              </ScrollPanel>
            </div>
          </Card>
        )}
      </div>

      {/* Settings Dialog */}
      <Dialog
        header="Advanced Settings"
        visible={showSettings}
        style={{ width: '90vw', maxWidth: '450px' }}
        onHide={() => setShowSettings(false)}
        className="m-2"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Detection Languages</label>
            <Dropdown
              value={selectedLanguages}
              options={languages}
              onChange={(e) => setSelectedLanguages(e.value)}
              placeholder="Select languages"
              multiple
              className="w-full"
            />
            <small className="text-gray-500">
              Select multiple languages for better detection accuracy
            </small>
          </div>

          <Divider />

          <div className="flex justify-between items-center">
            <div>
              <span className="font-medium">High Accuracy Mode</span>
              <p className="text-sm text-gray-500">
                Use Google AI fallback for low confidence results
              </p>
            </div>
            <InputSwitch
              checked={useHighAccuracy}
              onChange={(e) => setUseHighAccuracy(e.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Confidence Threshold
            </label>
            <Dropdown
              value={confidenceThreshold}
              options={thresholdOptions}
              onChange={(e) => setConfidenceThreshold(e.value)}
              className="w-full"
            />
            <small className="text-gray-500">
              Lower values trigger AI fallback more often
            </small>
          </div>
        </div>
      </Dialog>

      {/* Results Dialog */}
      <Dialog
        header="Processing Results"
        visible={showResults}
        style={{ width: '95vw', maxWidth: '800px' }}
        onHide={() => setShowResults(false)}
        maximizable
        className="m-2"
      >
        {results && (
          <div className="space-y-3 sm:space-y-4">
            <div className="grid">
              {/* <Card> */}
                {/* <h4 className="font-semibold mb-2">Processing Summary</h4> */}
                {/* <div className="space-y-1 text-sm"> */}
                  {/* <p><span className="font-medium">Method:</span> {results.method || 'EasyOCR'}</p> */}
                  {/* <p><span className="font-medium">Confidence:</span> 
                  {
                    results.average_confidence ? 
                    (results.average_confidence * 100).toFixed(1) + '%' : 
                    'N/A'
                  }</p> */}
                  {/* {results.fallback_used && (
                    <Chip label="AI Fallback Used" className="bg-orange-100 text-orange-800" />
                  )} */}
                {/* </div> */}
              {/* </Card> */}
              
              <Card>
                <h4 className="font-semibold mb-2 text-sm sm:text-base">Text Statistics</h4>
                <div className="space-y-1 text-xs sm:text-sm">
                  <p><span className="font-medium">Characters:</span> {extractedText.length}</p>
                  <p><span className="font-medium">Words:</span> {extractedText.split(/\s+/).length}</p>
                  <p><span className="font-medium">Lines:</span> {extractedText.split('\n').length}</p>
                </div>
              </Card>
            </div>

            <div>
              <h4 className="font-semibold mb-2 text-sm sm:text-base">Extracted Text</h4>
              <div className="bg-gray-50 p-3 sm:p-4 rounded border">
                <ScrollPanel style={{ width: '100%', height: '250px' }}>
                  <pre className="whitespace-pre-wrap text-xs sm:text-sm">
                    {extractedText}
                  </pre>
                </ScrollPanel>
              </div>
            </div>
          </div>
        )}
      </Dialog>
    </div>
  );
}

export default Home;
