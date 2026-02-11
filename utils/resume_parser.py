"""
Resume Parser Module
Extracts information from PDF and DOCX files
"""

import PyPDF2
import pdfplumber
import docx
import re
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    # Quietly handle missing spaCy
from collections import Counter
import os
import urllib.parse

class ResumeParser:
    def __init__(self):
        """Initialize the resume parser with NLP model"""
        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except:
                print("Warning: spaCy model not found. Keyword extraction will be limited.")
        
        # Common skill keywords
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'typescript', 'scala', 'r', 'matlab'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'asp.net', 'laravel', 'next.js', 'nuxt'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra', 'dynamodb', 'firebase'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd', 'devops'],
            'data_science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'data analysis', 'statistics'],
            'tools': ['git', 'github', 'jira', 'confluence', 'slack', 'vs code', 'intellij', 'postman', 'figma', 'adobe'],
            'soft_skills': ['leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking', 'time management', 'agile', 'scrum']
        }
    
    def parse(self, filepath):
        """Parse resume and extract information"""
        # Extract text based on file type
        if filepath.endswith('.pdf'):
            text = self._extract_text_from_pdf(filepath)
        elif filepath.endswith('.docx'):
            text = self._extract_text_from_docx(filepath)
        else:
            raise ValueError("Unsupported file format")
        
        # Extract various components
        resume_data = {
            'raw_text': text,
            'contact_info': self._extract_contact_info(text),
            'skills': self._extract_skills(text),
            'skill_categories': self._categorize_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'certifications': self._extract_certifications(text),
            'total_experience': self._calculate_total_experience(text),
            'keywords': self._extract_keywords(text),
            'sections': self._identify_sections(text),
            'search_results': self._generate_search_links(text)
        }
        
        return resume_data
    
    def _extract_text_from_pdf(self, filepath):
        """Improved text extraction using pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Fallback to PyPDF2 if pdfplumber fails to extract text
            if not text.strip():
                with open(filepath, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
        except Exception as e:
            print(f"Error extracting PDF: {e}")
        return text

    
    def _extract_text_from_docx(self, filepath):
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = docx.Document(filepath)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
        return text
    
    def _extract_contact_info(self, text):
        """Extract contact information"""
        contact_info = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contact_info['email'] = emails[0] if emails else None
        
        # Phone
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        contact_info['phone'] = phones[0] if phones else None
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        contact_info['linkedin'] = linkedin[0] if linkedin else None
        
        # GitHub
        github_pattern = r'github\.com/[\w-]+'
        github = re.findall(github_pattern, text, re.IGNORECASE)
        contact_info['github'] = github[0] if github else None
        
        return contact_info
    
    def _extract_skills(self, text):
        """Extract skills from resume"""
        text_lower = text.lower()
        skills = []
        
        for category, keywords in self.skill_keywords.items():
            for skill in keywords:
                if skill.lower() in text_lower:
                    skills.append(skill.title())
        
        return list(set(skills))
    
    def _categorize_skills(self, text):
        """Categorize skills by type"""
        text_lower = text.lower()
        categorized = {}
        
        for category, keywords in self.skill_keywords.items():
            found_skills = []
            for skill in keywords:
                if skill.lower() in text_lower:
                    found_skills.append(skill.title())
            if found_skills:
                categorized[category] = found_skills
        
        return categorized
    
    def _extract_experience(self, text):
        """Extract work experience"""
        experience = []
        
        # Look for common experience patterns
        exp_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4}|present|current)',
            r'(\w+\s+\d{4})\s*[-–]\s*(\w+\s+\d{4}|present|current)'
        ]
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            for pattern in exp_patterns:
                matches = re.findall(pattern, line, re.IGNORECASE)
                if matches:
                    # Try to get job title and company from surrounding lines
                    context = ' '.join(lines[max(0, i-2):min(len(lines), i+3)])
                    experience.append({
                        'period': matches[0],
                        'context': context[:200]
                    })
        
        return experience
    
    def _extract_education(self, text):
        """Extract education information"""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'(bachelor|master|phd|doctorate|associate|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?|mba)',
            r'(b\.?tech|m\.?tech|b\.?e\.?|m\.?e\.?)'
        ]
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            for pattern in degree_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    context = ' '.join(lines[max(0, i-1):min(len(lines), i+2)])
                    education.append(context[:200])
                    break
        
        return list(set(education))
    
    def _extract_certifications(self, text):
        """Extract certifications"""
        certifications = []
        
        # Common certification keywords
        cert_keywords = ['certified', 'certification', 'certificate', 'credential']
        
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in cert_keywords):
                certifications.append(line.strip())
        
        return certifications
    
    def _calculate_total_experience(self, text):
        """Calculate total years of experience"""
        # Look for explicit experience mentions
        exp_pattern = r'(\d+)\+?\s*years?\s*(?:of)?\s*experience'
        matches = re.findall(exp_pattern, text, re.IGNORECASE)
        
        if matches:
            return max([int(m) for m in matches])
        
        # Try to calculate from date ranges
        date_pattern = r'(\d{4})\s*[-–]\s*(\d{4}|present|current)'
        dates = re.findall(date_pattern, text, re.IGNORECASE)
        
        if dates:
            total_years = 0
            for start, end in dates:
                end_year = 2026 if end.lower() in ['present', 'current'] else int(end)
                total_years += end_year - int(start)
            return total_years
        
        return 0
    
    def _extract_keywords(self, text):
        """Extract important keywords using NLP or regex fallback"""
        if not self.nlp:
            # Enhanced regex-based keyword extraction fallback
            text = text.lower()
            
            # Remove common stop words
            stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'of', 'with', 'and', 'or', 'so', 'but', 'is', 'are', 'was', 'were', 'be', 'been', 'has', 'have', 'had', 'do', 'does', 'did', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'what', 'which', 'who', 'whom', 'where', 'when', 'why', 'how', 'experience', 'education', 'skills', 'work', 'project', 'projects', 'summary', 'profile', 'contact', 'email', 'phone', 'address', 'linkedin', 'github', 'year', 'years', 'month', 'months', 'present', 'current', 'date', 'from', 'till'}
            
            # Find words that look like technical terms (n-grams could be better but single words for now)
            # Filter for words > 2 chars, alphanumeric
            words = re.findall(r'\b[a-z][a-z0-9+#]*\b', text)
            
            # Filter stop words and common resume structural words
            filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
            
            # Add known skill keywords to boost their frequency
            known_skills = []
            for category, sk_list in self.skill_keywords.items():
                for sk in sk_list:
                    if sk.lower() in text:
                        known_skills.append(sk.lower())
            
            # Combine filtered words and known skills (giving more weight to known skills)
            all_keywords = filtered_words + (known_skills * 2)
            
            keyword_freq = Counter(all_keywords)
            return [word for word, freq in keyword_freq.most_common(20)]
        
        doc = self.nlp(text.lower())
        
        # Extract nouns and proper nouns
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 3]
        
        # Get most common keywords
        keyword_freq = Counter(keywords)
        return [word for word, freq in keyword_freq.most_common(20)]
    
    def _identify_sections(self, text):
        """Identify resume sections"""
        sections = {
            'has_summary': False,
            'has_experience': False,
            'has_education': False,
            'has_skills': False,
            'has_certifications': False,
            'has_projects': False
        }
        
        text_lower = text.lower()
        
        section_keywords = {
            'has_summary': ['summary', 'objective', 'profile'],
            'has_experience': ['experience', 'employment', 'work history'],
            'has_education': ['education', 'academic'],
            'has_skills': ['skills', 'technical skills', 'competencies'],
            'has_certifications': ['certifications', 'certificates', 'credentials'],
            'has_projects': ['projects', 'portfolio']
        }
        
        for section, keywords in section_keywords.items():
            sections[section] = any(keyword in text_lower for keyword in keywords)
        
        return sections

    def _generate_search_links(self, text):
        """Generate Google Search links based on resume content"""
        # Extract skills and important keywords
        skills = self._extract_skills(text)
        
        # Identify possible roles (simplified)
        roles = []
        role_keywords = ['developer', 'engineer', 'manager', 'analyst', 'scientist', 'designer']
        for line in text.split('\n')[:20]: # Check first 20 lines for titles
            for role in role_keywords:
                if role in line.lower():
                    roles.append(line.strip())
                    break
        
        # Clean roles
        clean_roles = [re.sub(r'[^a-zA-Z\s]', '', r).strip() for r in roles[:3]]
        
        search_queries = []
        
        # Use first identified role or generic
        base_title = clean_roles[0] if clean_roles else "Software Engineer"
        
        # Query 1: Role + Top Skills
        top_skills = skills[:3]
        query1 = f"{base_title} jobs {' '.join(top_skills)}"
        search_queries.append({
            'label': f'Jobs for {base_title} with {", ".join(top_skills)}',
            'url': f"https://www.google.com/search?q={urllib.parse.quote(query1)}"
        })
        
        # Query 2: Role + Remote
        query2 = f"Remote {base_title} jobs"
        search_queries.append({
            'label': f'Remote {base_title} Jobs',
            'url': f"https://www.google.com/search?q={urllib.parse.quote(query2)}"
        })
        
        # Query 3: Trending skills in role
        query3 = f"Trending skills for {base_title} 2026"
        search_queries.append({
            'label': f'Trending Skills for {base_title}',
            'url': f"https://www.google.com/search?q={urllib.parse.quote(query3)}"
        })
        
        return search_queries

