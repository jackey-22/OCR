# 🖼️ AI-Powered OCR System

A modern web application that extracts text from images using advanced AI technology. Built with React and Flask, this OCR system provides high-accuracy text recognition with an intuitive user interface.

![OCR System](https://img.shields.io/badge/OCR-AI%20Powered-blue)
![React](https://img.shields.io/badge/React-19.1-61dafb)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Python](https://img.shields.io/badge/Python-3.11-yellow)

## ✨ Features

- 📤 **Drag & Drop Upload** - Easy file upload with drag-and-drop or click to browse
- 🖼️ **Multiple Image Formats** - Supports JPG, PNG, GIF, BMP, TIFF, WebP
- 🌍 **Multi-Language Support** - Recognizes text in 10+ languages
- 🎯 **High Accuracy Mode** - AI-powered fallback for better results
- 📊 **Real-time Processing** - Live progress tracking
- 💾 **Export Options** - Download or copy extracted text
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🛠️ Tech Stack

### Frontend
- **React 19.1** - Modern UI library
- **Vite** - Fast build tool
- **PrimeReact** - Rich UI components
- **Tailwind CSS** - Utility-first styling
- **React Router** - Navigation

### Backend
- **Flask 3.0** - Python web framework
- **EasyOCR** - Primary OCR engine (CRAFT + CRNN)
- **Google Generative AI (Gemini)** - AI fallback for enhanced accuracy
- **Pillow** - Image processing
- **OpenCV** - Computer vision
- **PyTorch** - Deep learning framework

## 🤖 AI Models Explained

This OCR system uses a **two-tier approach** to ensure maximum accuracy:

### Primary OCR Engine: EasyOCR

**EasyOCR** combines two powerful neural networks:

1. **CRAFT (Character Region Awareness for Text detection)**
   - Detects text regions in images
   - Identifies where text is located, even in complex layouts
   - Works with rotated, curved, or multi-oriented text

2. **CRNN (Convolutional Recurrent Neural Network)**
   - Recognizes the actual characters in detected regions
   - Converts images of text into readable strings
   - Trained on millions of text samples

**Supported Languages:** 80+ languages including:
- English, Spanish, French, German, Italian, Portuguese
- Chinese (Simplified & Traditional), Japanese, Korean
- Arabic, Russian, Hindi, and many more

**Typical Accuracy:** 85-95% depending on:
- Image quality and resolution
- Text clarity and font style
- Background complexity

### High Accuracy Fallback: Google Generative AI (Gemini)

When EasyOCR's confidence falls below the threshold (default: 70%), the system automatically uses **Google's Gemini AI** for a second attempt.

**Why Gemini is Better for Difficult Images:**
- **Context Understanding** - Uses AI to understand context and fix recognition errors
- **Advanced Vision** - Better handles low-quality images, handwriting, and complex layouts
- **Error Correction** - Can correct spelling mistakes and formatting issues
- **Layout Intelligence** - Understands document structure (tables, columns, paragraphs)

**Typical Accuracy:** 95-99% even with:
- Blurry or low-resolution images
- Handwritten text
- Complex backgrounds
- Unusual fonts or artistic text

### How They Work Together

```
Image Upload → EasyOCR Processing → Confidence Check
                                           ↓
                                    Is confidence > 70%?
                                    ↙              ↘
                                 YES              NO
                                  ↓                ↓
                          Return Result    Use Gemini AI
                                                   ↓
                                           Enhanced Result
```

**Benefits of this approach:**
- ⚡ **Fast**: EasyOCR handles most images quickly
- 🎯 **Accurate**: Gemini catches difficult cases
- 💰 **Cost-effective**: Only uses AI API when needed
- 🔒 **Reliable**: Multiple fallback options

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **pip** (Python package manager)
- **Git**

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/jackey-22/OCR.git
cd OCR
```

### 2. Setup Backend (Flask Server)

```bash
# Navigate to server directory
cd server-ai

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

The backend server will start at `http://localhost:5000`

### 3. Setup Frontend (React App)

Open a new terminal window:

```bash
# Navigate to client directory
cd client-web

# Install dependencies
npm install

# Create .env file
echo VITE_URL=http://localhost:5000 > .env

# Start development server
npm run dev
```

The frontend will start at `http://localhost:5173`

## 🌐 Deployment

#### Backend Deployment (Render)

1. Push your code to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and configure the service
5. **Copy your Render backend URL** (e.g., `https://your-app.onrender.com`)
6. Add environment variables:
   - `GOOGLE_API_KEY` (optional, for AI fallback)
   - `PORT` (automatically set by Render)

#### Frontend Deployment (Vercel)

**CRITICAL STEP:** You must set the backend URL as an environment variable!

##### Option 1: Using Vercel Dashboard (Recommended)
1. Go to [Vercel Dashboard](https://vercel.com)
2. Import your GitHub repository
3. Set **Root Directory** to `client-web`
4. Go to **Settings** → **Environment Variables**
5. Add: 
   - **Name**: `VITE_URL`
   - **Value**: `https://your-backend-url.onrender.com` (your Render URL)
6. **Important**: Remove the `/api` suffix - just use the base URL
7. Deploy!

##### Option 2: Using Vercel CLI
```bash
cd client-web
vercel --build-env VITE_URL=https://your-backend-url.onrender.com
```

### 🔍 Testing Your Deployment

After deployment, test these URLs:

1. **Backend Health Check**: `https://your-backend.onrender.com/api/health`
   - Should return: `{"status": "healthy", "service": "OCR API"}`

2. **Frontend**: `https://your-app.vercel.app`
   - Should load the UI
   - Try uploading an image - it should work for everyone now!

### 🐛 Common Deployment Issues

#### Problem: "Failed to fetch" or "Network Error"
**Solution**: 
- Make sure `VITE_URL` in Vercel is set to your Render backend URL
- Rebuild your Vercel deployment after adding the environment variable
- Check that your Render backend is actually running

#### Problem: CORS errors in production
**Solution**: 
- Backend `app.py` already has CORS configured for all origins
- If you want to restrict it, change `"origins": "*"` to your Vercel URL in `app.py`

#### Problem: Works on my device but not others
**Cause**: Your frontend is using `localhost:5000` instead of the production backend
**Solution**: 
- Set `VITE_URL` environment variable in Vercel
- Rebuild and redeploy the frontend

## 📁 Project Structure

```
OCR/
├── client-web/              # React frontend
│   ├── src/
│   │   ├── pages/          # Page components
│   │   │   └── Home.jsx    # Main OCR interface
│   │   ├── utils/          # Utility functions
│   │   │   └── ocr.api.js  # API calls
│   │   ├── components/     # Reusable components
│   │   └── assets/         # Static assets
│   ├── public/             # Public files
│   └── package.json        # Frontend dependencies
│
├── server-ai/              # Flask backend
│   ├── app.py             # Main Flask application
│   ├── ocr.py             # OCR processing logic
│   ├── config.py          # Configuration
│   └── requirements.txt   # Python dependencies
│
├── render.yaml            # Render deployment config
└── README.md              # This file
```

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in `server-ai/` (optional but recommended for high accuracy mode):

```env
GOOGLE_API_KEY=your_google_api_key_here  # Required for Gemini AI fallback
PORT=5000
```

**How to get Google API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy and paste it into your `.env` file

**Note:** Without the API key, the system will still work but will only use EasyOCR (no AI fallback).

### Frontend Environment Variables

Create a `.env` file in `client-web/`:

```env
VITE_URL=http://localhost:5000
```

For production, set `VITE_URL` to your deployed backend URL.

## 📖 API Documentation

### Process OCR
```
POST /api/ocr
```
**Body:** FormData with image files
**Response:** Extracted text and metadata

## 🎨 Usage

1. **Upload Image**
   - Drag and drop images or click "Choose Files from Device"
   - Multiple files supported

2. **Configure Settings** (Optional)
   - Select detection languages
   - Enable/disable high accuracy mode
   - Adjust confidence threshold

3. **Process**
   - Click "Process Files" button
   - Wait for extraction to complete

4. **Export Results**
   - Copy text to clipboard
   - Download as .txt file
   - View detailed results

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in app.py or kill the process
lsof -ti:5000 | xargs kill -9  # Mac/Linux
```

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

### Frontend Issues

**Build fails:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS errors:**
- Ensure backend is running
- Check `VITE_URL` in `.env` file

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Jackey**
- GitHub: [@jackey-22](https://github.com/jackey-22)

## 🙏 Acknowledgments

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - CRAFT + CRNN based OCR engine
- [Google Generative AI (Gemini)](https://ai.google.dev/) - Enhanced accuracy with AI
- [PrimeReact](https://primereact.org/) - Beautiful UI components
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [Render](https://render.com) - Backend hosting
- [Vercel](https://vercel.com) - Frontend hosting

## 📧 Support

If you have any questions or need help, please open an issue on GitHub or contact the maintainer.

---

Made with ❤️ by Jackey
