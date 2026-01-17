/**
 * Dashboard JavaScript - Handles user dashboard interactions
 */

// API Configuration
const API_BASE_URL = '/api';
let authToken = localStorage.getItem('auth_token');
let currentUser = null;

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
    loadUserProfile();
    loadRecommendations();
    setupEventListeners();
});

/**
 * Check if user is authenticated
 */
function checkAuthentication() {
    if (!authToken) {
        window.location.href = '/login';
        return;
    }
}

/**
 * Load user profile data
 */
async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load profile');
        }
        
        const data = await response.json();
        currentUser = data.user;
        
        // Update UI with user data
        displayUserInfo(currentUser);
        displayUserSkills(currentUser.skills);
        displayUserBadges(currentUser.badges);
        updateStats(currentUser);
        
    } catch (error) {
        console.error('Error loading profile:', error);
        showNotification('Failed to load profile', 'error');
    }
}

/**
 * Display user information
 */
function displayUserInfo(user) {
    document.getElementById('userName').textContent = user.full_name || user.username;
    document.getElementById('userPoints').textContent = user.points || 0;
}

/**
 * Display user skills
 */
function displayUserSkills(skills) {
    const container = document.getElementById('skillsContainer');
    
    if (!skills || skills.length === 0) {
        container.innerHTML = '<p class="text-muted">No skills added yet. <a href="/profile">Add skills</a></p>';
        return;
    }
    
    container.innerHTML = skills.map(skill => 
        `<span class="skill-badge">${escapeHtml(skill)}</span>`
    ).join('');
}

/**
 * Display user badges
 */
function displayUserBadges(badges) {
    const container = document.getElementById('badgesContainer');
    
    if (!badges || badges.length === 0) {
        container.innerHTML = '<p class="text-muted">No badges earned yet</p>';
        return;
    }
    
    const badgeIcons = {
        'first_job': '🎯',
        'skill_master': '🏆',
        'profile_complete': '✅',
        'learner': '📚',
        'networker': '🤝'
    };
    
    container.innerHTML = badges.map(badge => 
        `<div class="badge-item">
            <span class="badge-icon">${badgeIcons[badge] || '⭐'}</span>
            <small>${badge.replace('_', ' ').toUpperCase()}</small>
        </div>`
    ).join('');
}

/**
 * Update dashboard statistics
 */
function updateStats(user) {
    // These would be loaded from actual API endpoints
    document.getElementById('matchedJobs').textContent = '24';
    document.getElementById('applications').textContent = '8';
    document.getElementById('skillMatch').textContent = '87%';
}

/**
 * Load job recommendations
 */
async function loadRecommendations() {
    try {
        const response = await fetch(`${API_BASE_URL}/recommendations`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to load recommendations');
        }
        
        const data = await response.json();
        displayRecommendations(data.recommendations || []);
        
    } catch (error) {
        console.error('Error loading recommendations:', error);
        document.getElementById('recommendationsContainer').innerHTML = 
            '<p class="text-muted">Failed to load recommendations. Please try again later.</p>';
    }
}

/**
 * Display job recommendations
 */
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendationsContainer');
    
    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p class="text-muted">No recommendations yet. Complete your profile to get matched with jobs!</p>';
        return;
    }
    
    const html = recommendations.slice(0, 5).map(rec => `
        <div class="job-card" onclick="viewJobDetails(${rec.job.id})">
            <div class="job-card-header">
                <h6>${escapeHtml(rec.job.title)}</h6>
                <span class="match-score">${Math.round(rec.match_score * 100)}% Match</span>
            </div>
            <p class="company-name">
                <i class="fas fa-building"></i> ${escapeHtml(rec.job.company)}
            </p>
            <p class="job-location">
                <i class="fas fa-map-marker-alt"></i> ${escapeHtml(rec.job.location || 'Remote')}
            </p>
            <div class="job-skills">
                ${rec.matched_skills.slice(0, 3).map(skill => 
                    `<span class="skill-tag">${escapeHtml(skill)}</span>`
                ).join('')}
                ${rec.matched_skills.length > 3 ? `<span class="skill-tag">+${rec.matched_skills.length - 3} more</span>` : ''}
            </div>
            <div class="job-card-footer">
                <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); saveJob(${rec.job.id})">
                    <i class="fas fa-bookmark"></i> Save
                </button>
                <button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); applyToJob(${rec.job.id})">
                    <i class="fas fa-paper-plane"></i> Apply
                </button>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

/**
 * View job details
 */
function viewJobDetails(jobId) {
    window.location.href = `/job/${jobId}`;
}

/**
 * Save job for later
 */
async function saveJob(jobId) {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/save`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            showNotification('Job saved successfully!', 'success');
        }
    } catch (error) {
        console.error('Error saving job:', error);
        showNotification('Failed to save job', 'error');
    }
}

/**
 * Apply to job
 */
async function applyToJob(jobId) {
    if (confirm('Are you ready to apply to this job?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/apply`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                showNotification('Application submitted!', 'success');
            }
        } catch (error) {
            console.error('Error applying to job:', error);
            showNotification('Failed to submit application', 'error');
        }
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Chat input enter key
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
}

/**
 * Toggle chatbot visibility
 */
function toggleChatbot() {
    const widget = document.getElementById('chatbotWidget');
    widget.classList.toggle('active');
}

/**
 * Send message to chatbot
 */
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    input.value = '';
    
    try {
        const response = await fetch(`${API_BASE_URL}/chatbot/message`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                user_context: currentUser
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get response');
        }
        
        const data = await response.json();
        addMessageToChat(data.response, 'bot');
        
    } catch (error) {
        console.error('Error sending message:', error);
        addMessageToChat('Sorry, I had trouble processing that. Please try again.', 'bot');
    }
}

/**
 * Add message to chat
 */
function addMessageToChat(message, sender) {
    const chatBody = document.getElementById('chatbotBody');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}-message`;
    messageDiv.innerHTML = `<p>${escapeHtml(message)}</p>`;
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

/**
 * Logout user
 */
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}