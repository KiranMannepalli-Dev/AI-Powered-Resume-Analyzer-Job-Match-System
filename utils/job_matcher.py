import re
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    # Quietly use fallback matching

class JobMatcher:
    def __init__(self):
        """Initialize job matcher"""
        if SKLEARN_AVAILABLE:
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        else:
            self.vectorizer = None
    
    def match(self, resume_data, job_description):
        """Match resume with job description"""
        # Extract resume text
        resume_text = self._prepare_resume_text(resume_data)
        
        # Calculate similarity score
        similarity_score = self._calculate_similarity(resume_text, job_description)
        
        # Extract job requirements
        job_skills = self._extract_job_skills(job_description)
        resume_skills = set([s.lower() for s in resume_data.get('skills', [])])
        
        # Calculate skill match
        matched_skills = resume_skills.intersection(set(job_skills))
        skill_match_percentage = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
        
        # Calculate experience match
        required_experience = self._extract_required_experience(job_description)
        candidate_experience = resume_data.get('total_experience', 0)
        experience_match = self._calculate_experience_match(candidate_experience, required_experience)
        
        # Overall match score (weighted average)
        overall_score = (
            similarity_score * 0.4 +
            skill_match_percentage * 0.4 +
            experience_match * 0.2
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'similarity_score': round(similarity_score, 2),
            'skill_match_percentage': round(skill_match_percentage, 2),
            'experience_match': round(experience_match, 2),
            'matched_skills': list(matched_skills),
            'missing_skills': list(set(job_skills) - resume_skills),
            'required_experience': required_experience,
            'candidate_experience': candidate_experience,
            'recommendation': self._get_recommendation(overall_score)
        }
    
    def analyze_skill_gap(self, resume_data, job_description):
        """Analyze skill gaps between resume and job"""
        job_skills = self._extract_job_skills(job_description)
        resume_skills = set([s.lower() for s in resume_data.get('skills', [])])
        
        matched_skills = resume_skills.intersection(set(job_skills))
        missing_skills = set(job_skills) - resume_skills
        extra_skills = resume_skills - set(job_skills)
        
        # Categorize missing skills by priority
        critical_skills = self._identify_critical_skills(job_description, missing_skills)
        nice_to_have = missing_skills - critical_skills
        
        return {
            'matched_skills': list(matched_skills),
            'missing_skills': {
                'critical': list(critical_skills),
                'nice_to_have': list(nice_to_have)
            },
            'extra_skills': list(extra_skills),
            'match_percentage': round(len(matched_skills) / len(job_skills) * 100, 2) if job_skills else 0,
            'learning_recommendations': self._get_learning_recommendations(critical_skills)
        }
    
    def _prepare_resume_text(self, resume_data):
        """Prepare resume text for comparison"""
        text_parts = [
            resume_data.get('raw_text', ''),
            ' '.join(resume_data.get('skills', [])),
            ' '.join([exp.get('context', '') for exp in resume_data.get('experience', [])]),
            ' '.join(resume_data.get('education', []))
        ]
        return ' '.join(text_parts)
    
    def _calculate_similarity(self, resume_text, job_description):
        """Calculate cosine similarity between resume and job description"""
        try:
            if not SKLEARN_AVAILABLE or not self.vectorizer:
                # Simple fallback: Jaccard similarity of words
                resume_words = set(re.findall(r'\w+', resume_text.lower()))
                job_words = set(re.findall(r'\w+', job_description.lower()))
                
                intersection = resume_words.intersection(job_words)
                union = resume_words.union(job_words)
                
                if not union:
                    return 0
                
                return (len(intersection) / len(union)) * 100

            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_description])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return similarity * 100
        except Exception as e:
            print(f"Similarity calculation error: {e}")
            return 0
    
    def _extract_job_skills(self, job_description):
        """Extract skills from job description"""
        # Common technical skills
        skill_patterns = [
            r'\b(python|java|javascript|c\+\+|c#|ruby|php|swift|kotlin|go|rust)\b',
            r'\b(react|angular|vue|node\.js|django|flask|spring|express)\b',
            r'\b(sql|mysql|postgresql|mongodb|redis|oracle)\b',
            r'\b(aws|azure|gcp|docker|kubernetes|jenkins)\b',
            r'\b(machine learning|deep learning|ai|data science|analytics)\b',
            r'\b(git|agile|scrum|devops|ci/cd)\b'
        ]
        
        skills = []
        job_lower = job_description.lower()
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, job_lower, re.IGNORECASE)
            skills.extend(matches)
        
        # Also look for skills in bullet points
        lines = job_description.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['required', 'must have', 'skills', 'experience with']):
                # Extract potential skills from this line
                words = re.findall(r'\b[a-z]+(?:\.[a-z]+)?\b', line.lower())
                skills.extend([w for w in words if len(w) > 2])
        
        return list(set(skills))
    
    def _extract_required_experience(self, job_description):
        """Extract required years of experience from job description"""
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'minimum\s*(?:of)?\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            if matches:
                return max([int(m) for m in matches])
        
        return 0
    
    def _calculate_experience_match(self, candidate_exp, required_exp):
        """Calculate experience match percentage"""
        if required_exp == 0:
            return 100
        
        if candidate_exp >= required_exp:
            return 100
        else:
            return (candidate_exp / required_exp) * 100
    
    def _get_recommendation(self, score):
        """Get recommendation based on match score"""
        if score >= 80:
            return "Excellent match! You should definitely apply."
        elif score >= 60:
            return "Good match. Consider applying and highlighting relevant skills."
        elif score >= 40:
            return "Moderate match. You may need to acquire some skills first."
        else:
            return "Low match. Consider gaining more relevant experience and skills."
    
    def _identify_critical_skills(self, job_description, missing_skills):
        """Identify critical skills from missing skills"""
        critical_keywords = ['required', 'must have', 'essential', 'mandatory']
        critical = set()
        
        job_lower = job_description.lower()
        
        for skill in missing_skills:
            # Check if skill appears near critical keywords
            for keyword in critical_keywords:
                pattern = f'{keyword}.*{skill}|{skill}.*{keyword}'
                if re.search(pattern, job_lower, re.IGNORECASE):
                    critical.add(skill)
                    break
        
        # If no critical skills found, mark first 3 missing skills as critical
        if not critical and missing_skills:
            critical = set(list(missing_skills)[:3])
        
        return critical
    
    def _get_learning_recommendations(self, critical_skills):
        """Get learning recommendations for critical skills"""
        recommendations = []
        
        learning_resources = {
            'python': 'Python.org tutorials, Coursera Python courses',
            'javascript': 'MDN Web Docs, freeCodeCamp',
            'react': 'React official docs, Scrimba React course',
            'aws': 'AWS Training and Certification, A Cloud Guru',
            'docker': 'Docker official docs, Docker Mastery course',
            'machine learning': 'Coursera ML course, fast.ai',
            'sql': 'SQLZoo, Mode Analytics SQL tutorial'
        }
        
        for skill in critical_skills:
            resource = learning_resources.get(skill.lower(), 'Search online courses and tutorials')
            recommendations.append({
                'skill': skill,
                'resources': resource,
                'priority': 'High'
            })
        
        return recommendations
