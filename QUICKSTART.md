# 🚀 Quick Start Guide

Welcome to the AI-Powered Resume Analyzer & Job Match System!

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Python Dependencies

Open PowerShell in this directory and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### Step 2: Initialize Database

```powershell
python init_db.py
```

### Step 3: Run the Application

```powershell
python app.py
```

The application will start at: **http://localhost:5000**

## 🎯 How to Use

### 1. Upload Your Resume
- Click the upload zone or drag & drop your PDF/DOCX resume
- Wait for the analysis to complete

### 2. View Analysis
- See your ATS compatibility score
- Review identified skills and experience
- Get AI-powered recommendations

### 3. Match with Jobs
- Paste a job description
- Click "Match with Job"
- View match percentage and skill gaps

## 🔑 Optional: OpenAI Integration

For enhanced AI recommendations, add your OpenAI API key:

1. Get an API key from https://platform.openai.com/api-keys
2. Edit `.env` file
3. Set `OPENAI_API_KEY=your-key-here`

**Note:** The system works without OpenAI, but recommendations will be rule-based.

## 📊 Features

✅ **Resume Parsing** - Extract skills, experience, education  
✅ **ATS Score** - Check compatibility with tracking systems  
✅ **Job Matching** - Match resume with job descriptions  
✅ **Skill Gap Analysis** - Identify missing skills  
✅ **AI Recommendations** - Get improvement suggestions  
✅ **Visual Analytics** - Beautiful charts and graphs  

## 🛠️ Troubleshooting

### spaCy Model Error
If you see "spaCy model not found":
```powershell
python -m spacy download en_core_web_sm
```

### Port Already in Use
Change the port in `.env`:
```
PORT=8000
```

### File Upload Issues
- Ensure file is PDF or DOCX
- Maximum file size: 16MB
- Check file isn't password protected

## 📝 Sample Resume

Don't have a resume handy? Create a sample PDF with:
- Your contact information
- Skills (Python, JavaScript, etc.)
- Work experience with dates
- Education details

## 🎨 Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **AI/ML:** spaCy, scikit-learn, OpenAI (optional)
- **Database:** SQLite
- **Charts:** Chart.js

## 📧 Need Help?

Check the main README.md for detailed documentation.

---

**Ready to transform your job search? Let's go! 🚀**
