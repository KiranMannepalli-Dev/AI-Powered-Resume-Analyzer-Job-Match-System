# 📖 User Guide - AI Resume Analyzer

## Table of Contents
1. [Getting Started](#getting-started)
2. [Uploading Your Resume](#uploading-your-resume)
3. [Understanding Your Analysis](#understanding-your-analysis)
4. [Job Matching](#job-matching)
5. [Improving Your Resume](#improving-your-resume)
6. [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### First Time Setup
1. Run the setup script: `powershell -ExecutionPolicy Bypass -File setup.ps1`
2. Start the application: `python app.py`
3. Open your browser to: `http://localhost:5000`

### What You'll Need
- Your resume in PDF or DOCX format
- Job descriptions you're interested in (optional)
- 5-10 minutes to review results

---

## Uploading Your Resume

### Supported Formats
✅ **PDF** (.pdf) - Recommended  
✅ **Word Document** (.docx)  
❌ Image files (JPG, PNG)  
❌ Plain text files

### How to Upload
**Method 1: Drag & Drop**
1. Locate your resume file
2. Drag it over the upload zone
3. Drop when the zone highlights

**Method 2: Click to Browse**
1. Click anywhere in the upload zone
2. Select your resume from the file picker
3. Click "Open"

### File Requirements
- **Maximum size**: 16 MB
- **Format**: PDF or DOCX only
- **Content**: Should include skills, experience, education
- **Language**: English (for best results)

### What Happens Next
1. File uploads (progress bar shows status)
2. Text is extracted from your document
3. AI analyzes the content
4. Results appear automatically

---

## Understanding Your Analysis

### ATS Compatibility Score
**What it is**: A score from 0-100 showing how well your resume passes Applicant Tracking Systems

**Letter Grades**:
- **A+ (90-100)**: Excellent! Your resume is highly ATS-friendly
- **A (80-89)**: Very good, minor improvements possible
- **B (70-79)**: Good, but some optimization needed
- **C (60-69)**: Fair, several improvements recommended
- **D (Below 60)**: Needs significant work

**What affects your score**:
- ✅ Simple, clean formatting
- ✅ Standard section headers
- ✅ Relevant keywords and skills
- ✅ Clear contact information
- ✅ Good readability
- ❌ Complex tables or columns
- ❌ Special characters or symbols
- ❌ Missing standard sections
- ❌ Poor keyword optimization

### Skills Analysis
**Identified Skills**: All technical and soft skills found in your resume

**Skill Categories**:
- **Programming**: Languages like Python, Java, JavaScript
- **Web**: Frameworks like React, Angular, Django
- **Database**: SQL, MongoDB, PostgreSQL
- **Cloud**: AWS, Azure, Docker, Kubernetes
- **Data Science**: Machine Learning, TensorFlow, Pandas
- **Tools**: Git, JIRA, VS Code
- **Soft Skills**: Leadership, Communication, Teamwork

**Skills Chart**: Visual breakdown showing skill distribution across categories

### Experience Summary
- **Years of Experience**: Total calculated from date ranges
- **Work Experiences**: Number of jobs listed
- **Education Entries**: Degrees and certifications

### AI Recommendations
Personalized suggestions to improve your resume, categorized by:
- **High Priority**: Critical improvements needed
- **Medium Priority**: Important but not urgent
- **Low Priority**: Nice-to-have enhancements

---

## Job Matching

### How to Match with a Job

1. **Copy the Job Description**
   - Find a job posting you're interested in
   - Copy the entire job description
   - Include requirements, responsibilities, and qualifications

2. **Paste into the Text Area**
   - Scroll to the "Job Matching" section
   - Paste the job description
   - Click "Match with Job"

3. **Review Results**
   - Overall match percentage
   - Detailed breakdown
   - Skill gaps
   - Recommendations

### Understanding Match Scores

**Overall Match Score** (0-100%)
- **80-100%**: Excellent match - Apply with confidence!
- **60-79%**: Good match - Highlight relevant experience
- **40-59%**: Moderate match - Consider if you can learn missing skills
- **Below 40%**: Low match - May need more experience/skills

**Score Components**:
1. **Content Similarity** (40% weight)
   - How similar your resume text is to the job description
   - Based on TF-IDF and cosine similarity

2. **Skill Match** (40% weight)
   - Percentage of required skills you have
   - Most important factor

3. **Experience Match** (20% weight)
   - Whether you meet experience requirements
   - Years of experience comparison

### Skill Gap Analysis

**Matched Skills** ✅
- Skills you have that the job requires
- Your competitive advantages
- Highlight these in your application

**Missing Skills** ❌
- **Critical**: Must-have skills mentioned as "required"
- **Nice-to-Have**: Preferred but not essential

**What to Do**:
- Learn critical skills before applying
- Mention transferable skills for nice-to-haves
- Be honest about skill gaps in interviews

---

## Improving Your Resume

### Based on ATS Score

**If Score < 70**:
1. ✏️ Use standard section headers (Experience, Education, Skills)
2. 🔤 Avoid special characters and symbols
3. 📝 Add more relevant keywords
4. 📧 Ensure contact info is clearly visible
5. 📄 Use simple formatting (no tables, columns)

**If Score 70-89**:
1. ➕ Add more technical skills
2. 📊 Include quantifiable achievements
3. 🎯 Optimize keywords for your industry
4. 📋 Add missing sections (Summary, Projects)

**If Score 90+**:
1. ✨ Minor tweaks only
2. 🎯 Customize for each job application
3. 📈 Keep updating with new skills

### Based on Job Match

**If Match < 60%**:
1. 📚 Learn critical missing skills
2. 💼 Gain relevant experience
3. 🎓 Consider certifications
4. 🔄 Rewrite resume to highlight transferable skills

**If Match 60-79%**:
1. 🎯 Tailor resume to job description
2. 📝 Use exact keywords from job posting
3. 💡 Highlight relevant projects
4. 🔍 Research company and customize

**If Match 80+**:
1. ✅ Apply immediately!
2. 📧 Write a strong cover letter
3. 🌟 Prepare for interviews
4. 🔗 Connect with company employees on LinkedIn

### General Tips

**Content**:
- ✅ Start bullet points with action verbs
- ✅ Include numbers and metrics (increased by 30%, managed team of 5)
- ✅ Tailor resume for each application
- ✅ Keep it concise (1-2 pages)
- ❌ Don't use personal pronouns (I, me, my)
- ❌ Don't include irrelevant information
- ❌ Don't lie or exaggerate

**Formatting**:
- ✅ Use standard fonts (Arial, Calibri, Times New Roman)
- ✅ Font size 10-12pt
- ✅ Consistent formatting throughout
- ✅ Clear section headers
- ✅ Adequate white space
- ❌ No images, graphics, or photos
- ❌ No headers/footers
- ❌ No text boxes or tables

**Keywords**:
- ✅ Include job-specific keywords
- ✅ Use industry terminology
- ✅ List technical skills explicitly
- ✅ Match job description language
- ❌ Don't keyword stuff
- ❌ Don't use outdated terms

---

## Tips & Best Practices

### Before Uploading
- ✅ Proofread for typos and grammar
- ✅ Update with latest experience
- ✅ Remove personal information (if concerned about privacy)
- ✅ Save in PDF format for best compatibility

### Using the Analysis
- 📊 Review all sections carefully
- 📝 Take notes on recommendations
- 🎯 Prioritize high-impact changes
- 🔄 Re-upload after making improvements

### Job Matching
- 🎯 Match with multiple jobs to see patterns
- 📈 Track your scores over time
- 🎓 Focus on learning critical missing skills
- 💼 Build projects to demonstrate skills

### Privacy & Security
- 🔒 Your resume is stored locally in the database
- 🗑️ Delete uploaded resumes when done
- 🔐 Don't include sensitive personal information
- 🌐 Use on trusted networks only

### Getting the Most Value
1. **Baseline**: Upload current resume to see starting score
2. **Improve**: Make recommended changes
3. **Re-test**: Upload improved version
4. **Compare**: See score improvements
5. **Customize**: Tailor for specific jobs
6. **Apply**: Use optimized resume for applications

### Common Mistakes to Avoid
- ❌ Uploading image-based PDFs (text must be selectable)
- ❌ Using creative/artistic resume templates
- ❌ Ignoring ATS score recommendations
- ❌ Not customizing for each job
- ❌ Listing skills you don't actually have
- ❌ Using vague descriptions without metrics

### When to Re-analyze
- ✅ After making significant changes
- ✅ When applying to different industries
- ✅ Every 3-6 months to stay current
- ✅ After gaining new skills or experience
- ✅ When match scores are consistently low

---

## Frequently Asked Questions

**Q: Why is my ATS score low?**  
A: Common reasons include complex formatting, missing keywords, or non-standard section headers. Check the recommendations for specific improvements.

**Q: Can I upload multiple resumes?**  
A: Yes! Upload different versions to compare scores and see which performs better.

**Q: Do I need an OpenAI API key?**  
A: No, it's optional. The system works with rule-based recommendations. OpenAI enhances the quality of suggestions.

**Q: Is my data secure?**  
A: Yes, all data is stored locally on your machine. Nothing is sent to external servers (except OpenAI if you configure it).

**Q: Why doesn't it detect all my skills?**  
A: The system looks for common technical skills. Add any missing skills explicitly to your resume.

**Q: Can I export the analysis?**  
A: Currently, you can screenshot the results. PDF export is a planned feature.

**Q: What if the job match is 100%?**  
A: Congratulations! You're an excellent fit. Apply immediately and prepare for interviews.

---

## Need Help?

- 📖 Check the README.md for technical details
- 🚀 See QUICKSTART.md for setup instructions
- 📊 Review PROJECT_SUMMARY.md for architecture
- 💬 Open an issue on GitHub for bugs or questions

---

**Good luck with your job search! 🎯**
