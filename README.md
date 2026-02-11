# AI-Powered Resume Analyzer & Job Match System

A comprehensive AI-powered platform for resume analysis, ATS compatibility checking, and intelligent job matching with real-time market intelligence.

## 🚀 Features

- **Resume Upload & Parsing**: Support for PDF and DOCX formats
- **ATS Compatibility Analysis**: Detailed scoring and recommendations
- **AI-Powered Recommendations**: Intelligent suggestions for resume improvement
- **Job Matching**: Smart matching algorithm with skill gap analysis
- **Market Intelligence**: Latest tech news and job openings from Hacker News
- **Interactive Dashboard**: Beautiful, responsive UI with real-time analytics

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI/ML**: OpenAI API (optional), Custom NLP algorithms
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Deployment**: Vercel-ready, Render-compatible

## 📦 Installation

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/KiranMannepalli-Dev/AI-Powered-Resume-Analyzer-Job-Match-System.git
cd AI-Powered-Resume-Analyzer-Job-Match-System
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY (optional)
```

5. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## 🌐 Deployment

### Vercel Deployment

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will auto-detect the `vercel.json` configuration

3. **Set Environment Variables** (Important!)
   - `VERCEL=1` (automatically set by Vercel)
   - `OPENAI_API_KEY=your-key-here` (optional, for AI features)

4. **Deploy**
   - Click "Deploy" and your app will be live!

### Render Deployment

1. Create a new Web Service on [render.com](https://render.com)
2. Connect your GitHub repository
3. Set build command: `bash render-build.sh`
4. Set start command: `gunicorn app:app`
5. Add environment variables:
   - `OPENAI_API_KEY` (optional)
   - `DATABASE_PATH=/tmp/resume_analyzer.db`

## 📝 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI recommendations | No | - |
| `SECRET_KEY` | Flask secret key | No | `dev-secret-key` |
| `DATABASE_PATH` | Path to SQLite database | No | `resume_analyzer.db` |
| `UPLOAD_FOLDER` | Directory for uploaded files | No | `uploads` |
| `PORT` | Server port | No | `5000` |

## 🎯 Usage

1. **Upload Resume**: Drag and drop or select a PDF/DOCX file
2. **View Analysis**: Get instant ATS score and recommendations
3. **Match Jobs**: Paste a job description to see compatibility
4. **Explore Market**: Check latest tech news and job openings
5. **Download Report**: Export your analysis results

## 🔧 API Endpoints

- `POST /api/upload` - Upload and analyze resume
- `GET /api/analyze/<resume_id>` - Get detailed analysis
- `POST /api/match` - Match resume with job description
- `POST /api/skill-gap` - Analyze skill gaps
- `GET /api/recommendations/<resume_id>` - Get AI recommendations
- `GET /api/news-jobs` - Get latest news and jobs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Kiran Mannepalli**
- GitHub: [@KiranMannepalli-Dev](https://github.com/KiranMannepalli-Dev)

## 🙏 Acknowledgments

- OpenAI for GPT API
- Hacker News for job/news data
- Flask community for excellent documentation
