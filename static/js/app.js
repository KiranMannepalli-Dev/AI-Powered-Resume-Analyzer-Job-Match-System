/**
 * AI Resume Analyzer - Frontend JavaScript
 * Handles file upload, API calls, and UI interactions
 */

// Global state
let currentResumeId = null;
let currentResumeData = null;
let skillsChart = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeUploadZone();
    addSmoothScrolling();
});

/**
 * Initialize drag & drop upload zone
 */
function initializeUploadZone() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');

    // Click to upload
    uploadZone.addEventListener('click', () => {
        fileInput.click();
    });

    // File selected
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Drag & drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');

        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
}

/**
 * Handle file upload
 */
async function handleFileUpload(file) {
    // Validate file
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
        showNotification('Please upload a PDF or DOCX file', 'error');
        return;
    }

    if (file.size > 16 * 1024 * 1024) {
        showNotification('File size must be less than 16MB', 'error');
        return;
    }

    // Show progress
    document.getElementById('uploadProgress').classList.remove('hidden');
    document.getElementById('uploadSuccess').classList.add('hidden');

    // Create form data
    const formData = new FormData();
    formData.append('resume', file);

    try {
        // Simulate progress
        animateProgress();

        // Upload file
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Complete progress
        completeProgress();

        if (data.success) {
            currentResumeId = data.resume_id;
            currentResumeData = data.data;

            // Show success
            document.getElementById('uploadProgress').classList.add('hidden');
            document.getElementById('uploadSuccess').classList.remove('hidden');

            // Load analysis immediately from the upload response
            const analysisData = {
                success: true,
                resume_data: data.data,
                ats_score: data.analysis.ats_score,
                recommendations: data.analysis.recommendations
            };

            displayAnalysis(analysisData);

            // Show analysis section
            document.getElementById('analyze').classList.remove('hidden');
            document.getElementById('jobMatch').classList.remove('hidden');

            setTimeout(() => {
                scrollToSection('analyze');
            }, 300);

            showNotification('Resume processed instantly!', 'success');
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showNotification(error.message || 'Failed to upload resume', 'error');
        document.getElementById('uploadProgress').classList.add('hidden');
    }
}

/**
 * Animate upload progress
 */
function animateProgress() {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');

    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 25; // Faster increment
        if (progress > 95) progress = 95;

        progressFill.style.width = progress + '%';
        progressText.textContent = `Optimizing... ${Math.round(progress)}%`;

        if (progress >= 95) {
            clearInterval(interval);
        }
    }, 100); // Faster interval (100ms instead of 200ms)

    // Store interval globally to clear it
    window.uploadInterval = interval;
}

/**
 * Instantly complete progress bar
 */
function completeProgress() {
    if (window.uploadInterval) clearInterval(window.uploadInterval);
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    progressFill.style.width = '100%';
    progressText.textContent = 'Analysis Complete!';
}

/**
 * Load and display resume analysis
 */
async function loadAnalysis() {
    if (!currentResumeId) return;

    try {
        // Fetch analysis
        const response = await fetch(`/api/analyze/${currentResumeId}`);
        const data = await response.json();

        if (data.success) {
            displayAnalysis(data);

            // Show analysis section
            document.getElementById('analyze').classList.remove('hidden');
            document.getElementById('jobMatch').classList.remove('hidden');

            // Scroll to analysis
            setTimeout(() => {
                scrollToSection('analyze');
            }, 500);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        showNotification('Failed to analyze resume', 'error');
    }
}

/**
 * Display resume analysis results
 */
function displayAnalysis(data) {
    const { resume_data, ats_score, recommendations } = data;

    // Display ATS Score
    displayATSScore(ats_score);

    // Display Skills
    displaySkills(resume_data.skills, resume_data.skill_categories);

    // Display Experience
    displayExperience(resume_data);

    // Display Recommendations
    displayRecommendations(recommendations);

    // Display Search Results
    displaySearchResults(resume_data.search_results);

    // Create skills chart
    createSkillsChart(resume_data.skill_categories);
}

/**
 * Display Search Results
 */
function displaySearchResults(searchResults) {
    const list = document.getElementById('searchResultsList');

    if (!searchResults || searchResults.length === 0) {
        list.innerHTML = '<p class="text-muted">No search results available</p>';
        return;
    }

    list.innerHTML = searchResults.map(result => `
        <a href="${result.url}" target="_blank" class="btn btn-secondary text-left" style="border-radius: var(--radius-md); padding: 1.5rem; justify-content: flex-start; height: auto;">
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">🔍</span>
                <span style="font-weight: 600;">${result.label}</span>
                <span style="font-size: 0.75rem; color: var(--text-muted);">View on Google</span>
            </div>
        </a>
    `).join('');
}

/**
 * Display ATS score
 */
function displayATSScore(atsScore) {
    const scoreElement = document.getElementById('atsScore');
    const gradeElement = document.getElementById('atsGrade');

    // Animate score
    animateValue(scoreElement, 0, atsScore.overall_score, 1500);

    gradeElement.textContent = `Grade: ${atsScore.grade}`;

    // Set badge color based on grade
    gradeElement.className = 'badge';
    if (atsScore.grade.startsWith('A')) {
        gradeElement.classList.add('badge-success');
    } else if (atsScore.grade.startsWith('B')) {
        gradeElement.classList.add('badge-primary');
    } else {
        gradeElement.classList.add('badge-warning');
    }
}

/**
 * Display skills
 */
function displaySkills(skills, skillCategories) {
    const skillsList = document.getElementById('skillsList');

    if (skills.length === 0) {
        skillsList.innerHTML = '<p class="text-muted">No skills identified</p>';
        return;
    }

    skillsList.innerHTML = skills.map(skill =>
        `<span class="badge badge-primary" style="margin: 0.25rem;">${skill}</span>`
    ).join('');
}

/**
 * Display experience summary
 */
function displayExperience(resumeData) {
    const experienceSummary = document.getElementById('experienceSummary');

    const years = resumeData.total_experience || 0;
    const experienceCount = resumeData.experience?.length || 0;
    const educationCount = resumeData.education?.length || 0;

    experienceSummary.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 1rem;">
            <div>
                <div style="font-size: 2rem; font-weight: 700; color: var(--primary-color);">${years}</div>
                <div class="text-secondary">Years of Experience</div>
            </div>
            <div>
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--accent-color);">${experienceCount}</div>
                <div class="text-secondary">Work Experiences</div>
            </div>
            <div>
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--success-color);">${educationCount}</div>
                <div class="text-secondary">Education Entries</div>
            </div>
        </div>
    `;
}

/**
 * Display recommendations
 */
function displayRecommendations(recommendations) {
    const recommendationsList = document.getElementById('recommendationsList');

    if (!recommendations || recommendations.length === 0) {
        recommendationsList.innerHTML = '<p class="text-muted">No recommendations available</p>';
        return;
    }

    recommendationsList.innerHTML = recommendations.map(rec => `
        <div class="card mb-md">
            <div style="display: flex; align-items: start; gap: 1rem;">
                <span class="badge ${getPriorityBadgeClass(rec.priority)}">${rec.priority}</span>
                <div style="flex: 1;">
                    <h4 style="margin-bottom: 0.5rem;">${rec.category}</h4>
                    <p class="text-secondary">${rec.suggestion}</p>
                    ${rec.impact ? `<p class="text-muted" style="font-size: 0.875rem; margin-top: 0.5rem;">💡 ${rec.impact}</p>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Create skills distribution chart
 */
function createSkillsChart(skillCategories) {
    const ctx = document.getElementById('skillsChart');

    if (!skillCategories || Object.keys(skillCategories).length === 0) {
        ctx.parentElement.innerHTML = '<p class="text-muted text-center">No skill data available</p>';
        return;
    }

    const labels = Object.keys(skillCategories).map(key =>
        key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    );
    const data = Object.values(skillCategories).map(skills => skills.length);

    if (skillsChart) {
        skillsChart.destroy();
    }

    skillsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Skills',
                data: data,
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(118, 75, 162, 0.8)',
                    'rgba(245, 87, 108, 0.8)',
                    'rgba(0, 242, 254, 0.8)',
                    'rgba(254, 225, 64, 0.8)',
                    'rgba(240, 147, 251, 0.8)',
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)',
                    'rgba(245, 87, 108, 1)',
                    'rgba(0, 242, 254, 1)',
                    'rgba(254, 225, 64, 1)',
                    'rgba(240, 147, 251, 1)',
                ],
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        color: '#b8b8d4'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        color: '#b8b8d4'
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Match job with resume
 */
async function matchJob() {
    const jobDescription = document.getElementById('jobDescription').value.trim();

    if (!jobDescription) {
        showNotification('Please enter a job description', 'error');
        return;
    }

    if (!currentResumeId) {
        showNotification('Please upload a resume first', 'error');
        return;
    }

    const matchBtn = document.getElementById('matchBtn');
    matchBtn.disabled = true;
    matchBtn.innerHTML = '<span class="spinner"></span> Matching...';

    try {
        const response = await fetch('/api/match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                resume_id: currentResumeId,
                job_description: jobDescription
            })
        });

        const data = await response.json();

        if (data.success) {
            displayMatchResults(data.match_result);
            document.getElementById('matchResults').classList.remove('hidden');

            setTimeout(() => {
                document.getElementById('matchResults').scrollIntoView({ behavior: 'smooth' });
            }, 300);

            showNotification('Job match completed!', 'success');
        } else {
            throw new Error(data.error || 'Match failed');
        }
    } catch (error) {
        console.error('Match error:', error);
        showNotification('Failed to match job', 'error');
    } finally {
        matchBtn.disabled = false;
        matchBtn.innerHTML = '<span>🎯</span> Match with Job';
    }
}

/**
 * Display job match results
 */
function displayMatchResults(matchResult) {
    // Overall score
    const matchScore = document.getElementById('matchScore');
    animateValue(matchScore, 0, matchResult.overall_score, 1500);

    // Recommendation
    document.getElementById('matchRecommendation').textContent = matchResult.recommendation;

    // Match breakdown
    document.getElementById('skillMatchPercent').textContent = `${matchResult.skill_match_percentage}%`;
    document.getElementById('skillMatchBar').style.width = `${matchResult.skill_match_percentage}%`;

    document.getElementById('similarityPercent').textContent = `${matchResult.similarity_score}%`;
    document.getElementById('similarityBar').style.width = `${matchResult.similarity_score}%`;

    document.getElementById('experiencePercent').textContent = `${matchResult.experience_match}%`;
    document.getElementById('experienceBar').style.width = `${matchResult.experience_match}%`;

    // Matched skills
    const matchedSkillsList = document.getElementById('matchedSkillsList');
    if (matchResult.matched_skills.length > 0) {
        matchedSkillsList.innerHTML = matchResult.matched_skills.map(skill =>
            `<span class="badge badge-success" style="margin: 0.25rem;">${skill}</span>`
        ).join('');
    } else {
        matchedSkillsList.innerHTML = '<p class="text-muted">No matched skills</p>';
    }

    // Missing skills
    const missingSkillsList = document.getElementById('missingSkillsList');
    if (matchResult.missing_skills.length > 0) {
        missingSkillsList.innerHTML = matchResult.missing_skills.map(skill =>
            `<span class="badge badge-warning" style="margin: 0.25rem;">${skill}</span>`
        ).join('');
    } else {
        missingSkillsList.innerHTML = '<p class="text-muted">No missing skills - great match!</p>';
    }
}

/**
 * Utility Functions
 */

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function showDemo() {
    showNotification('Demo feature coming soon!', 'info');
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 16);
}

function getPriorityBadgeClass(priority) {
    switch (priority?.toLowerCase()) {
        case 'high':
            return 'badge-accent';
        case 'medium':
            return 'badge-warning';
        case 'low':
            return 'badge-primary';
        default:
            return 'badge-primary';
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 2rem;
        right: 2rem;
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-md);
        padding: 1rem 1.5rem;
        color: var(--text-primary);
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        max-width: 400px;
    `;

    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 1.5rem;">${icon}</span>
            <span>${message}</span>
        </div>
    `;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function addSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: translateX(0); }
        to { opacity: 0; transform: translateX(20px); }
    }
`;
document.head.appendChild(style);
