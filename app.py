"""
AI-Powered Resume Analyzer & Job Match System
Main Flask Application
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Import custom modules
from utils.resume_parser import ResumeParser
from utils.job_matcher import JobMatcher
from utils.ats_analyzer import ATSAnalyzer
from utils.ai_recommender import AIRecommender
from database.db_manager import DatabaseManager

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = set(os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx').split(','))

# Enable CORS
CORS(app)

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize utilities
resume_parser = ResumeParser()
job_matcher = JobMatcher()
ats_analyzer = ATSAnalyzer()
ai_recommender = AIRecommender()
db_manager = DatabaseManager()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_resume():
    """Handle resume file upload"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX allowed'}), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Parse resume
        resume_data = resume_parser.parse(filepath)
        
        # Save to database
        resume_id = db_manager.save_resume(resume_data, unique_filename)
        
        # Immediate Analysis (Increase speed by combining requests)
        ats_score = ats_analyzer.analyze(resume_data)
        recommendations = ai_recommender.get_recommendations(resume_data)
        
        return jsonify({
            'success': True,
            'resume_id': resume_id,
            'filename': unique_filename,
            'data': resume_data,
            'analysis': {
                'ats_score': ats_score,
                'recommendations': recommendations
            }
        }), 200
        
    except Exception as e:
        logger.exception("Error during resume upload and parsing")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze/<int:resume_id>', methods=['GET'])
def analyze_resume(resume_id):
    """Get detailed resume analysis"""
    try:
        # Get resume data from database
        resume_data = db_manager.get_resume(resume_id)
        
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Perform ATS analysis
        ats_score = ats_analyzer.analyze(resume_data)
        
        # Get AI recommendations
        recommendations = ai_recommender.get_recommendations(resume_data)
        
        return jsonify({
            'success': True,
            'resume_data': resume_data,
            'ats_score': ats_score,
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        logger.exception("Error during analysis")
        return jsonify({'error': str(e)}), 500


@app.route('/api/match', methods=['POST'])
def match_job():
    """Match resume with job description"""
    try:
        data = request.get_json()
        
        if not data or 'resume_id' not in data or 'job_description' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        resume_id = data['resume_id']
        job_description = data['job_description']
        
        # Get resume data
        resume_data = db_manager.get_resume(resume_id)
        
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Perform job matching
        match_result = job_matcher.match(resume_data, job_description)
        
        # Save job match to database
        db_manager.save_job_match(resume_id, job_description, match_result)
        
        return jsonify({
            'success': True,
            'match_result': match_result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/skill-gap', methods=['POST'])
def analyze_skill_gap():
    """Analyze skill gaps between resume and job"""
    try:
        data = request.get_json()
        
        if not data or 'resume_id' not in data or 'job_description' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        resume_id = data['resume_id']
        job_description = data['job_description']
        
        # Get resume data
        resume_data = db_manager.get_resume(resume_id)
        
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Analyze skill gaps
        skill_gap = job_matcher.analyze_skill_gap(resume_data, job_description)
        
        return jsonify({
            'success': True,
            'skill_gap': skill_gap
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recommendations/<int:resume_id>', methods=['GET'])
def get_recommendations(resume_id):
    """Get AI-powered improvement recommendations"""
    try:
        # Get resume data
        resume_data = db_manager.get_resume(resume_id)
        
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Get recommendations
        recommendations = ai_recommender.get_detailed_recommendations(resume_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats/<int:resume_id>', methods=['GET'])
def get_stats(resume_id):
    """Get resume statistics for dashboard"""
    try:
        # Get resume data
        resume_data = db_manager.get_resume(resume_id)
        
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Calculate statistics
        stats = {
            'total_skills': len(resume_data.get('skills', [])),
            'years_experience': resume_data.get('total_experience', 0),
            'education_level': resume_data.get('highest_education', 'N/A'),
            'certifications': len(resume_data.get('certifications', [])),
            'skill_categories': resume_data.get('skill_categories', {}),
            'experience_breakdown': resume_data.get('experience_breakdown', [])
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ats-score/<int:resume_id>', methods=['GET'])
def get_ats_score(resume_id):
    """Get detailed ATS compatibility score"""
    try:
        # Get resume data
        resume_data = db_manager.get_resume(resume_id)
        
        if not resume_data:
            return jsonify({'error': 'Resume not found'}), 404
        
        # Get detailed ATS analysis
        ats_analysis = ats_analyzer.detailed_analysis(resume_data)
        
        return jsonify({
            'success': True,
            'ats_analysis': ats_analysis
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Initialize database
    db_manager.init_db()
    
    # Run app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"Server running at: http://localhost:{port}")
    print(f"Environment: {'Development' if debug else 'Production'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
