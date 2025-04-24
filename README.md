# VerifAI: Where AI Meets Forensic Verification

VerifAI is a research-driven tool designed to detect AI-generated images by analyzing metadata (EXIF), byte-level structures (chunk signatures and watermark indicators), and leveraging machine learning models for classification. The tool helps digital forensics investigators, journalists, and cybersecurity professionals validate the authenticity of visual media.

## 📦 Prerequisites

Before running the tool, make sure you have the following installed:

### Global Requirements

- **Python 3.9+**
- **Node.js (v18+)** and **npm**
- **Git** (for cloning the repo)

### Python Backend Requirements

Navigate to the backend folder and install:

```bash
cd verifai-backend
pip install -r requirements.txt
```

### Install ExifTool CLI:

Download from: https://exiftool.org/

Ensure exiftool is added to your system PATH.

## ▶️ How to Run the Project
Step 1: Start the Backend
```bash
cd verifai-backend
python app.py
```
This launches the Flask server on http://localhost:5000.

Step 2: Start the Frontend
```bash
cd verifai-react
npm run dev
```
This launches the frontend on http://localhost:5173 (default Vite port).

## 📤 Upload & Output
Upload Interface
Users can upload one image (PNG, JPG, or WebP). The analysis is triggered immediately.

### Output Format
The result will display:

✅ Metadata Analysis (via ExifTool)

🧠 ML Detection Verdict (via SightEngine)

🧬 Byte-Level Signature Match
 
🔍 C2PA Detection (for WebP watermarks)

⚠️ Final Verdict: Real Image / Real Image with modifications by an AI model / Real Image with modifications by an AI model & the metadata was manipulated / AI Generated Image / AI Generated Image with metadata manipulation.

Each result is accompanied by a reason and breakdown.

## 📌 Notes
C2PA watermark analysis only applies to WebP images.

Signature matching is based on known chunk signatures in the SQLite database.

SightEngine API credentials must be stored securely in a .env file (excluded via .gitignore).
##

© 2025 Rita Tamer Ayoub - Project EXPO © 2025 School of Computing, Coventry University – Egypt branch
