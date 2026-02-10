# 🚀 AI-Powered Resume Analyzer & Job Match System

An intelligent system that analyzes resumes, matches them with job descriptions, and provides actionable insights to improve your job application success rate.

## ✨ Features

### 🎨 Premium User Interface
- **Modern Pastel Theme**: Professional, clean, and eye-catching design
- **Glassmorphism Effects**: Sleek, modern components with subtle animations
- **Responsive Layout**: Optimized for both desktop and mobile viewing
- **Real-time Progress**: Animated feedback during document analysis

### 📄 Resume Analysis & Speed
- **Smart Parsing**: Extract text precisely using `pdfplumber` (High Precision)
- **Instant Result Rendering**: Optimized one-step analysis for <2s feedback
- **Entity Recognition**: Identify skills, experience, and education
- **Automated Summarization**: Quick overview of your career strength

### 🎯 Job Matching
- **Intelligent Matching**: AI-powered TF-IDF matching against job descriptions
- **Skill Gap Analysis**: Identify missing keywords for specific roles
- **Career Search Integration**: Direct Google Search links for relevant job opportunities

### 📊 ATS & AI Recommendations
- **ATS Score**: Detailed compatibility check for Applicant Tracking Systems
- **AI-Powered Suggestions**: Actionable tips and impact statements for improvement
- **Skill Distribution**: Visual representation of your core competencies via Chart.js

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.9+ with Flask
- **AI/ML**: OpenAI API, spaCy, scikit-learn
- **Document Processing**: PyPDF2, python-docx
- **Database**: SQLite
- **Charts**: Chart.js

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Node.js (optional, for development tools)

### Setup Instructions

1. **Clone the repository**
```bash
cd "e:\AI-Powered Resume Analyzer & Job Match System"
```

2. **Create a virtual environment**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Download spaCy language model**
```bash
python -m spacy download en_core_web_sm
```

6. **Set up environment variables**
Create a `.env` file in the root directory:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

7. **Initialize the database**
```bash
python init_db.py
```

8. **Run the application**
```bash
python app.py
```

9. **Open in browser**
Navigate to `http://localhost:5000`

## 🎨 Features Overview

### 1. Upload Resume
- Drag & drop interface
- Support for PDF and DOCX formats
- Real-time file validation

### 2. Analyze Resume
- Extract personal information
- Identify skills and technologies
- Parse work experience and education
- Calculate ATS compatibility score

### 3. Job Matching
- Paste job description
- Get match percentage
- View skill gaps
- Receive tailored recommendations

### 4. Dashboard
- Visual analytics
- Skill distribution charts
- Experience timeline
- ATS score breakdown

## 🔒 Security

- Secure file upload with validation
- Data encryption at rest
- No permanent storage of sensitive data
- CORS protection
- Rate limiting on API endpoints

## 📝 API Endpoints

### Resume Analysis
- `POST /api/upload` - Upload resume file
- `POST /api/analyze` - Analyze uploaded resume
- `GET /api/resume/:id` - Get resume analysis results

### Job Matching
- `POST /api/match` - Match resume with job description
- `POST /api/skill-gap` - Analyze skill gaps
- `GET /api/recommendations/:id` - Get improvement recommendations

### Analytics
- `GET /api/stats/:id` - Get resume statistics
- `GET /api/ats-score/:id` - Get ATS compatibility score

## 🚀 Usage

1. **Upload Your Resume**: Click "Upload Resume" and select your PDF/DOCX file
2. **View Analysis**: See extracted information, skills, and experience
3. **Add Job Description**: Paste the job description you're targeting
4. **Get Match Score**: View compatibility percentage and skill gaps
5. **Improve Resume**: Follow AI-powered recommendations
6. **Download Report**: Export detailed analysis as PDF

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT API
- spaCy for NLP capabilities
- Flask community for excellent documentation
- Chart.js for beautiful visualizations

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for job seekers worldwide**
