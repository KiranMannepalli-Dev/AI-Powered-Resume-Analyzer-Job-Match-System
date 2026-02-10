"""
Database Manager Module
Handles all database operations for the resume analyzer
"""

import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='resume_analyzer.db'):
        """Initialize database manager"""
        self.db_path = db_path
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Resumes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                raw_text TEXT,
                contact_info TEXT,
                skills TEXT,
                skill_categories TEXT,
                experience TEXT,
                education TEXT,
                certifications TEXT,
                total_experience INTEGER,
                keywords TEXT,
                sections TEXT,
                search_results TEXT
            )
        ''')
        
        # Job matches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                job_description TEXT,
                match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                overall_score REAL,
                similarity_score REAL,
                skill_match_percentage REAL,
                experience_match REAL,
                matched_skills TEXT,
                missing_skills TEXT,
                FOREIGN KEY (resume_id) REFERENCES resumes (id)
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                event_type TEXT,
                event_data TEXT,
                event_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("[DB] Database initialized successfully")
    
    def save_resume(self, resume_data, filename):
        """Save resume data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resumes (
                filename, raw_text, contact_info, skills, skill_categories,
                experience, education, certifications, total_experience,
                keywords, sections, search_results
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            resume_data.get('raw_text', ''),
            json.dumps(resume_data.get('contact_info', {})),
            json.dumps(resume_data.get('skills', [])),
            json.dumps(resume_data.get('skill_categories', {})),
            json.dumps(resume_data.get('experience', [])),
            json.dumps(resume_data.get('education', [])),
            json.dumps(resume_data.get('certifications', [])),
            resume_data.get('total_experience', 0),
            json.dumps(resume_data.get('keywords', [])),
            json.dumps(resume_data.get('sections', {})),
            json.dumps(resume_data.get('search_results', []))
        ))
        
        resume_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return resume_id
    
    def get_resume(self, resume_id):
        """Get resume data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'filename': row[1],
            'upload_date': row[2],
            'raw_text': row[3],
            'contact_info': json.loads(row[4]) if row[4] else {},
            'skills': json.loads(row[5]) if row[5] else [],
            'skill_categories': json.loads(row[6]) if row[6] else {},
            'experience': json.loads(row[7]) if row[7] else [],
            'education': json.loads(row[8]) if row[8] else [],
            'certifications': json.loads(row[9]) if row[9] else [],
            'total_experience': row[10],
            'keywords': json.loads(row[11]) if row[11] else [],
            'sections': json.loads(row[12]) if row[12] else {},
            'search_results': json.loads(row[13]) if row[13] else []
        }
    
    def save_job_match(self, resume_id, job_description, match_result):
        """Save job match results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO job_matches (
                resume_id, job_description, overall_score, similarity_score,
                skill_match_percentage, experience_match, matched_skills, missing_skills
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            resume_id,
            job_description,
            match_result.get('overall_score', 0),
            match_result.get('similarity_score', 0),
            match_result.get('skill_match_percentage', 0),
            match_result.get('experience_match', 0),
            json.dumps(match_result.get('matched_skills', [])),
            json.dumps(match_result.get('missing_skills', []))
        ))
        
        conn.commit()
        conn.close()
    
    def get_job_matches(self, resume_id):
        """Get all job matches for a resume"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM job_matches WHERE resume_id = ? ORDER BY match_date DESC', (resume_id,))
        rows = cursor.fetchall()
        conn.close()
        
        matches = []
        for row in rows:
            matches.append({
                'id': row[0],
                'resume_id': row[1],
                'job_description': row[2],
                'match_date': row[3],
                'overall_score': row[4],
                'similarity_score': row[5],
                'skill_match_percentage': row[6],
                'experience_match': row[7],
                'matched_skills': json.loads(row[8]) if row[8] else [],
                'missing_skills': json.loads(row[9]) if row[9] else []
            })
        
        return matches
    
    def log_analytics(self, resume_id, event_type, event_data):
        """Log analytics event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics (resume_id, event_type, event_data)
            VALUES (?, ?, ?)
        ''', (resume_id, event_type, json.dumps(event_data)))
        
        conn.commit()
        conn.close()
    
    def get_all_resumes(self):
        """Get all resumes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, filename, upload_date FROM resumes ORDER BY upload_date DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [{'id': row[0], 'filename': row[1], 'upload_date': row[2]} for row in rows]
