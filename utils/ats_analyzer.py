"""
ATS Analyzer Module
Analyzes resume compatibility with Applicant Tracking Systems
"""

import re
from textstat import flesch_reading_ease

class ATSAnalyzer:
    def __init__(self):
        """Initialize ATS analyzer"""
        self.ats_friendly_sections = [
            'summary', 'experience', 'education', 'skills',
            'certifications', 'projects', 'achievements'
        ]
    
    def analyze(self, resume_data):
        """Analyze resume for ATS compatibility"""
        scores = {
            'formatting': self._check_formatting(resume_data),
            'keywords': self._check_keywords(resume_data),
            'sections': self._check_sections(resume_data),
            'readability': self._check_readability(resume_data),
            'contact_info': self._check_contact_info(resume_data)
        }
        
        # Calculate overall ATS score (weighted average)
        overall_score = (
            scores['formatting'] * 0.25 +
            scores['keywords'] * 0.30 +
            scores['sections'] * 0.20 +
            scores['readability'] * 0.15 +
            scores['contact_info'] * 0.10
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'category_scores': scores,
            'grade': self._get_grade(overall_score),
            'issues': self._identify_issues(scores, resume_data),
            'recommendations': self._get_ats_recommendations(scores)
        }
    
    def detailed_analysis(self, resume_data):
        """Get detailed ATS analysis"""
        basic_analysis = self.analyze(resume_data)
        
        # Add more detailed checks
        detailed = {
            **basic_analysis,
            'file_format_check': self._check_file_format(),
            'special_characters': self._check_special_characters(resume_data),
            'bullet_points': self._check_bullet_points(resume_data),
            'date_formats': self._check_date_formats(resume_data),
            'action_verbs': self._check_action_verbs(resume_data),
            'quantifiable_achievements': self._check_quantifiable_achievements(resume_data)
        }
        
        return detailed
    
    def _check_formatting(self, resume_data):
        """Check formatting compatibility"""
        score = 100
        text = resume_data.get('raw_text', '')
        
        # Check for problematic characters
        problematic_chars = ['•', '◆', '★', '→', '©', '®', '™']
        if any(char in text for char in problematic_chars):
            score -= 15
        
        # Check for tables (hard to detect in plain text, but look for patterns)
        if re.search(r'\|.*\|.*\|', text):
            score -= 10
        
        # Check for excessive formatting (multiple spaces, tabs)
        if re.search(r'  {3,}', text):
            score -= 10
        
        return max(0, score)
    
    def _check_keywords(self, resume_data):
        """Check keyword optimization"""
        skills = resume_data.get('skills', [])
        keywords = resume_data.get('keywords', [])
        
        # More skills and keywords = better ATS score
        skill_count = len(skills)
        keyword_count = len(keywords)
        
        if skill_count >= 15 and keyword_count >= 15:
            return 100
        elif skill_count >= 10 and keyword_count >= 10:
            return 80
        elif skill_count >= 5 and keyword_count >= 5:
            return 60
        else:
            return 40
    
    def _check_sections(self, resume_data):
        """Check for standard resume sections"""
        sections = resume_data.get('sections', {})
        
        # Count how many standard sections are present
        present_sections = sum(1 for has_section in sections.values() if has_section)
        total_sections = len(sections)
        
        if total_sections == 0:
            return 50
        
        return (present_sections / total_sections) * 100
    
    def _check_readability(self, resume_data):
        """Check text readability"""
        text = resume_data.get('raw_text', '')
        
        if not text:
            return 50
        
        try:
            # Flesch reading ease score (higher is better, 60-70 is ideal)
            reading_score = flesch_reading_ease(text)
            
            if 60 <= reading_score <= 70:
                return 100
            elif 50 <= reading_score <= 80:
                return 85
            elif 40 <= reading_score <= 90:
                return 70
            else:
                return 50
        except:
            return 50
    
    def _check_contact_info(self, resume_data):
        """Check if contact information is present"""
        contact = resume_data.get('contact_info', {})
        
        score = 0
        if contact.get('email'):
            score += 40
        if contact.get('phone'):
            score += 30
        if contact.get('linkedin'):
            score += 15
        if contact.get('github'):
            score += 15
        
        return score
    
    def _get_grade(self, score):
        """Get letter grade based on score"""
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        else:
            return 'D'
    
    def _identify_issues(self, scores, resume_data):
        """Identify specific ATS issues"""
        issues = []
        
        if scores['formatting'] < 70:
            issues.append({
                'category': 'Formatting',
                'severity': 'High',
                'issue': 'Resume contains ATS-unfriendly formatting elements',
                'fix': 'Remove special characters, tables, and complex formatting'
            })
        
        if scores['keywords'] < 60:
            issues.append({
                'category': 'Keywords',
                'severity': 'High',
                'issue': 'Insufficient keywords and skills',
                'fix': 'Add more relevant skills and industry keywords'
            })
        
        if scores['sections'] < 70:
            issues.append({
                'category': 'Structure',
                'severity': 'Medium',
                'issue': 'Missing standard resume sections',
                'fix': 'Include sections like Summary, Experience, Education, Skills'
            })
        
        if scores['contact_info'] < 70:
            issues.append({
                'category': 'Contact Info',
                'severity': 'High',
                'issue': 'Incomplete contact information',
                'fix': 'Add email, phone, and professional profiles (LinkedIn)'
            })
        
        return issues
    
    def _get_ats_recommendations(self, scores):
        """Get recommendations to improve ATS score"""
        recommendations = []
        
        if scores['formatting'] < 80:
            recommendations.append('Use simple, clean formatting without tables or special characters')
        
        if scores['keywords'] < 80:
            recommendations.append('Include more industry-specific keywords and technical skills')
        
        if scores['sections'] < 80:
            recommendations.append('Add standard sections: Summary, Experience, Education, Skills')
        
        if scores['readability'] < 80:
            recommendations.append('Use clear, concise language with active voice')
        
        if scores['contact_info'] < 80:
            recommendations.append('Ensure all contact information is clearly visible at the top')
        
        return recommendations
    
    def _check_file_format(self):
        """Check file format compatibility"""
        return {
            'recommended': ['PDF', 'DOCX'],
            'avoid': ['JPG', 'PNG', 'Pages'],
            'note': 'PDF and DOCX are most ATS-friendly formats'
        }
    
    def _check_special_characters(self, resume_data):
        """Check for special characters that ATS might not parse"""
        text = resume_data.get('raw_text', '')
        problematic = []
        
        special_chars = {
            '•': 'Use hyphens (-) instead',
            '◆': 'Use asterisks (*) instead',
            '★': 'Avoid decorative symbols',
            '→': 'Use "to" or "->" instead',
            '©®™': 'Avoid copyright symbols'
        }
        
        for char, suggestion in special_chars.items():
            if char in text:
                problematic.append({'character': char, 'suggestion': suggestion})
        
        return {
            'found': len(problematic) > 0,
            'issues': problematic
        }
    
    def _check_bullet_points(self, resume_data):
        """Check bullet point usage"""
        text = resume_data.get('raw_text', '')
        
        # Count bullet-like patterns
        bullet_patterns = [r'^\s*[-*•]\s', r'^\s*\d+\.\s']
        bullet_count = 0
        
        for line in text.split('\n'):
            if any(re.match(pattern, line) for pattern in bullet_patterns):
                bullet_count += 1
        
        return {
            'count': bullet_count,
            'recommendation': 'Use simple hyphens (-) or asterisks (*) for bullets',
            'status': 'Good' if bullet_count > 5 else 'Add more bullet points for better readability'
        }
    
    def _check_date_formats(self, resume_data):
        """Check date format consistency"""
        text = resume_data.get('raw_text', '')
        
        date_patterns = {
            'MM/YYYY': r'\d{2}/\d{4}',
            'Month YYYY': r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',
            'YYYY-YYYY': r'\d{4}\s*[-–]\s*\d{4}'
        }
        
        found_formats = []
        for format_name, pattern in date_patterns.items():
            if re.search(pattern, text):
                found_formats.append(format_name)
        
        return {
            'formats_found': found_formats,
            'consistent': len(found_formats) <= 1,
            'recommendation': 'Use consistent date format throughout (e.g., "Month YYYY")'
        }
    
    def _check_action_verbs(self, resume_data):
        """Check for strong action verbs"""
        text = resume_data.get('raw_text', '').lower()
        
        strong_verbs = [
            'achieved', 'improved', 'developed', 'created', 'managed',
            'led', 'increased', 'reduced', 'implemented', 'designed',
            'analyzed', 'optimized', 'streamlined', 'launched', 'delivered'
        ]
        
        found_verbs = [verb for verb in strong_verbs if verb in text]
        
        return {
            'count': len(found_verbs),
            'verbs': found_verbs,
            'status': 'Excellent' if len(found_verbs) >= 8 else 'Good' if len(found_verbs) >= 5 else 'Add more action verbs'
        }
    
    def _check_quantifiable_achievements(self, resume_data):
        """Check for quantifiable achievements"""
        text = resume_data.get('raw_text', '')
        
        # Look for numbers and percentages
        number_patterns = [
            r'\d+%',  # Percentages
            r'\$\d+',  # Dollar amounts
            r'\d+\+',  # Numbers with plus
            r'\d+[KMB]',  # Thousands, millions, billions
        ]
        
        achievements = []
        for pattern in number_patterns:
            matches = re.findall(pattern, text)
            achievements.extend(matches)
        
        return {
            'count': len(achievements),
            'examples': achievements[:10],
            'status': 'Excellent' if len(achievements) >= 5 else 'Good' if len(achievements) >= 3 else 'Add more quantifiable achievements'
        }
