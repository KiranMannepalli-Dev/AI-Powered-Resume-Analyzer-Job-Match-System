"""
AI Recommender Module
Provides AI-powered recommendations for resume improvement
"""

import os
import re
from openai import OpenAI

class AIRecommender:
    def __init__(self):
        """Initialize AI recommender"""
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key) if api_key and api_key != 'your-openai-api-key-here' else None
    
    def get_recommendations(self, resume_data):
        """Get basic recommendations"""
        recommendations = []
        
        # Check skills
        skills = resume_data.get('skills', [])
        if len(skills) < 10:
            recommendations.append({
                'category': 'Skills',
                'priority': 'High',
                'suggestion': 'Add more technical skills to your resume. Aim for at least 10-15 relevant skills.',
                'impact': 'Increases visibility in ATS searches'
            })
        
        # Check experience
        experience = resume_data.get('experience', [])
        if len(experience) < 2:
            recommendations.append({
                'category': 'Experience',
                'priority': 'High',
                'suggestion': 'Provide more detailed work experience with specific achievements and responsibilities.',
                'impact': 'Demonstrates your career progression'
            })
        
        # Check sections
        sections = resume_data.get('sections', {})
        if not sections.get('has_summary'):
            recommendations.append({
                'category': 'Summary',
                'priority': 'Medium',
                'suggestion': 'Add a professional summary at the top highlighting your key strengths and career goals.',
                'impact': 'Captures recruiter attention immediately'
            })
        
        if not sections.get('has_projects'):
            recommendations.append({
                'category': 'Projects',
                'priority': 'Medium',
                'suggestion': 'Include a projects section showcasing your practical work and achievements.',
                'impact': 'Demonstrates hands-on experience'
            })
        
        # Check certifications
        certifications = resume_data.get('certifications', [])
        if len(certifications) == 0:
            recommendations.append({
                'category': 'Certifications',
                'priority': 'Low',
                'suggestion': 'Consider adding relevant certifications to boost your credibility.',
                'impact': 'Shows commitment to professional development'
            })
        
        return recommendations
    
    def get_detailed_recommendations(self, resume_data):
        """Get detailed AI-powered recommendations"""
        basic_recs = self.get_recommendations(resume_data)
        
        if self.client:
            try:
                ai_recs = self._get_ai_recommendations(resume_data)
                return {
                    'basic_recommendations': basic_recs,
                    'ai_recommendations': ai_recs,
                    'summary': self._generate_summary(resume_data)
                }
            except Exception as e:
                print(f"AI recommendations error: {e}")
                return {
                    'basic_recommendations': basic_recs,
                    'ai_recommendations': [],
                    'note': 'AI recommendations unavailable. Please check OpenAI API key.'
                }
        else:
            return {
                'basic_recommendations': basic_recs,
                'note': 'Set OPENAI_API_KEY environment variable for AI-powered recommendations'
            }
    
    def _get_ai_recommendations(self, resume_data):
        """Get recommendations using OpenAI API"""
        # Prepare resume summary for AI
        resume_summary = f"""
        Skills: {', '.join(resume_data.get('skills', [])[:20])}
        Experience: {resume_data.get('total_experience', 0)} years
        Education: {', '.join(resume_data.get('education', [])[:2])}
        Sections: {resume_data.get('sections', {})}
        """
        
        prompt = f"""
        As a professional career coach and resume expert, analyze this resume summary and provide 5 specific, actionable recommendations to improve it:
        
        {resume_summary}
        
        Provide recommendations in the following format:
        1. [Category]: [Specific actionable suggestion]
        2. [Category]: [Specific actionable suggestion]
        ...
        
        Focus on:
        - Content improvements
        - Missing elements
        - Better ways to present information
        - Industry best practices
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert resume consultant and career coach."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse AI response into structured recommendations
            recommendations = []
            lines = ai_response.strip().split('\n')
            for line in lines:
                if line.strip() and (line[0].isdigit() or line.startswith('-')):
                    # Remove numbering
                    clean_line = re.sub(r'^\d+\.\s*|-\s*', '', line)
                    if ':' in clean_line:
                        category, suggestion = clean_line.split(':', 1)
                        recommendations.append({
                            'category': category.strip(),
                            'suggestion': suggestion.strip()
                        })
            
            return recommendations
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return []
    
    def _generate_summary(self, resume_data):
        """Generate a summary of the resume"""
        skills_count = len(resume_data.get('skills', []))
        experience_years = resume_data.get('total_experience', 0)
        education_count = len(resume_data.get('education', []))
        
        summary = f"""
        Your resume contains {skills_count} identified skills, {experience_years} years of experience, 
        and {education_count} education entries. 
        """
        
        # Add strength assessment
        if skills_count >= 15 and experience_years >= 3:
            summary += "Your resume shows strong technical depth and experience. "
        elif skills_count >= 10 or experience_years >= 2:
            summary += "Your resume has a solid foundation. "
        else:
            summary += "Your resume could benefit from more detail. "
        
        return summary.strip()
    
    def get_skill_recommendations(self, current_skills, target_role):
        """Get skill recommendations for a target role"""
        # Common skills by role
        role_skills = {
            'software engineer': ['Python', 'Java', 'Git', 'Docker', 'AWS', 'SQL', 'React', 'Node.js'],
            'data scientist': ['Python', 'R', 'Machine Learning', 'SQL', 'Pandas', 'TensorFlow', 'Statistics'],
            'web developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Git', 'REST APIs'],
            'devops engineer': ['Docker', 'Kubernetes', 'AWS', 'Jenkins', 'Terraform', 'Linux', 'Python'],
            'product manager': ['Agile', 'Scrum', 'JIRA', 'Analytics', 'SQL', 'Communication', 'Leadership']
        }
        
        target_role_lower = target_role.lower()
        recommended_skills = []
        
        for role, skills in role_skills.items():
            if role in target_role_lower:
                current_skills_lower = [s.lower() for s in current_skills]
                missing = [s for s in skills if s.lower() not in current_skills_lower]
                recommended_skills = missing
                break
        
        return {
            'target_role': target_role,
            'recommended_skills': recommended_skills,
            'priority': 'High' if len(recommended_skills) > 5 else 'Medium'
        }
