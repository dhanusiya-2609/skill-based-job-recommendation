# Skill-Based Job Recommendation System
## Comprehensive Documentation

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Installation Guide](#installation-guide)
5. [Configuration](#configuration)
6. [API Documentation](#api-documentation)
7. [AI Models & Integration](#ai-models--integration)
8. [Database Schema](#database-schema)
9. [Frontend Components](#frontend-components)
10. [Workflow Automation](#workflow-automation)
11. [Testing](#testing)
12. [Deployment](#deployment)
13. [Security](#security)
14. [Performance Optimization](#performance-optimization)
15. [Troubleshooting](#troubleshooting)

---

## 1. Project Overview

### Purpose
The Skill-Based Job Recommendation System is an AI-powered platform that matches job seekers with relevant opportunities based on their skills, experience, and preferences. The system leverages IBM Watsonx, IBM Granite models, and multiple AI APIs to provide personalized recommendations.

### Key Features
- **AI-Powered Matching**: Advanced algorithms using IBM Watsonx and Granite models
- **Skill Gap Analysis**: Detailed analysis of missing skills with learning recommendations
- **Interactive Chatbot**: AI career advisor powered by ChatGPT and Gemini
- **Learning Paths**: Personalized course recommendations via IBM SkillsBuild
- **Workflow Automation**: Automated job alerts and notifications
- **Gamification**: Points, badges, and progress tracking

### Target Users
- Job seekers looking for career opportunities
- Career changers exploring new fields
- Students entering the job market
- Professionals seeking skill development

---

## 2. System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Web Browser  │  │ Mobile App   │  │   Desktop    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │   HTML/CSS/JavaScript (Bootstrap, React Components)  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Flask API  │  │   Auth Mgr   │  │  JWT Tokens  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Matching   │  │  Chatbot     │  │  Analytics   │      │
│  │   Engine     │  │  Service     │  │  Service     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                       AI INTEGRATION LAYER                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ IBM Watsonx  │  │   ChatGPT    │  │    Gemini    │      │
│  │  / Granite   │  │     API      │  │     API      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ SkillsBuild  │  │    Relay     │                         │
│  │     API      │  │ Automation   │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                        DATA LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │    Redis     │  │  File Store  │      │
│  │   Database   │  │    Cache     │  │   (Uploads)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **User Registration/Login**
   - User submits credentials
   - Backend validates and creates JWT token
   - Token stored in client for subsequent requests

2. **Profile Creation**
   - User adds skills, experience, preferences
   - Data validated and stored in database
   - Triggers initial recommendation generation

3. **Job Recommendation**
   - Matching engine retrieves active jobs
   - Calculates similarity scores using NLP
   - Ranks jobs based on match score and preferences
   - Results cached in Redis for performance

4. **AI Chatbot Interaction**
   - User sends message
   - System routes to appropriate AI service
   - Context maintained in conversation history
   - Response returned with citations/sources

5. **Skill Gap Analysis**
   - System compares user skills with job requirements
   - AI generates learning path recommendations
   - IBM SkillsBuild courses suggested
   - Results displayed with visualizations

---

## 3. Technology Stack

### Backend Technologies

#### Core Framework
- **Python 3.9+**: Primary programming language
- **Flask 3.0.0**: Web framework for API development
- **SQLAlchemy**: ORM for database operations
- **Flask-JWT-Extended**: JWT authentication

#### AI/ML Libraries
- **sentence-transformers**: Semantic similarity matching
- **scikit-learn**: Machine learning utilities
- **NLTK**: Natural language processing
- **TensorFlow/PyTorch**: Deep learning (optional)

#### AI Service Integrations
- **IBM Watsonx AI**: Enterprise AI platform
- **IBM Granite Models**: Large language models
- **OpenAI ChatGPT API**: Conversational AI
- **Google Gemini API**: Multimodal AI capabilities
- **IBM SkillsBuild API**: Learning resources

### Frontend Technologies

- **HTML5/CSS3**: Structure and styling
- **JavaScript (ES6+)**: Client-side logic
- **Bootstrap 5**: UI framework
- **Chart.js**: Data visualizations
- **Font Awesome**: Icons

### Data Storage

- **PostgreSQL**: Primary database (production)
- **SQLite**: Development database
- **Redis**: Caching and session management

### DevOps & Deployment

- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Gunicorn**: WSGI HTTP server
- **Nginx**: Reverse proxy and load balancing
- **Celery**: Asynchronous task queue

---

## 4. Installation Guide

### Prerequisites

```bash
# System Requirements
- Python 3.9 or higher
- pip 21.0 or higher
- Git
- PostgreSQL 13+ (production) or SQLite (development)
- Redis 6+ (for caching)
```

### Step-by-Step Installation

#### 1. Clone Repository

```bash
git clone https://github.com/dhanusiya-2609/skill-based-job-recommendation/
cd skill-based-job-recommendation
```

#### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

#### 5. Initialize Database

```bash
# Create database tables
python scripts/setup_database.py

# Seed with sample data
python scripts/populate_jobs.py
```

#### 6. Run Application

```bash
# Development mode
python run.py

# Or using Flask CLI
flask run
```

#### 7. Access Application

```
Open browser and navigate to: http://localhost:5000
```

### Docker Installation (Alternative)

```bash
# Build and run with Docker Compose
docker-compose -f deployment/docker-compose.yml up -d

# View logs
docker-compose logs -f web

# Stop containers
docker-compose down
```

---

## 5. Configuration

### Environment Variables

#### Required Variables

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/jobmatch

# IBM Watsonx
IBM_WATSONX_API_KEY=your-api-key
IBM_WATSONX_PROJECT_ID=your-project-id

# OpenAI
OPENAI_API_KEY=your-openai-key

# Google Gemini
GEMINI_API_KEY=your-gemini-key
```

#### Optional Variables

```bash
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-password

# Redis
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Application Settings

Edit `config.py` to customize:

```python
# Skill Matching
SKILL_MATCHING_THRESHOLD = 0.65  # Similarity threshold
RECOMMENDATION_LIMIT = 10         # Max recommendations

# Pagination
JOBS_PER_PAGE = 20
RECOMMENDATIONS_PER_PAGE = 10

# Agent Settings
JOB_ALERT_FREQUENCY = 'daily'
NOTIFICATION_ENABLED = True
```

---

## 6. API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securePassword123",
  "full_name": "John Doe"
}

Response: 201 Created
{
  "message": "User registered successfully",
  "user": {...},
  "access_token": "eyJ0eXAiOiJKV1...",
  "refresh_token": "eyJ0eXAiOiJKV1..."
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securePassword123"
}

Response: 200 OK
{
  "message": "Login successful",
  "user": {...},
  "access_token": "...",
  "refresh_token": "..."
}
```

### User Endpoints

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer {access_token}

Response: 200 OK
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "skills": ["Python", "JavaScript"],
    "points": 150
  }
}
```

### Recommendation Endpoints

#### Get Recommendations
```http
GET /api/recommendations
Authorization: Bearer {access_token}

Response: 200 OK
{
  "recommendations": [
    {
      "id": 1,
      "job": {...},
      "match_score": 0.87,
      "matched_skills": ["Python", "SQL"],
      "missing_skills": ["AWS"],
      "explanation": "..."
    }
  ],
  "total": 10
}
```

#### Get Skill Gap Analysis
```http
GET /api/recommendations/skill-gap/5
Authorization: Bearer {access_token}

Response: 200 OK
{
  "job": {...},
  "gap_analysis": {
    "gap_analysis": "...",
    "missing_skills": ["AWS", "Docker"]
  },
  "learning_path": {...}
}
```

### Chatbot Endpoints

#### Send Message
```http
POST /api/chatbot/message
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "message": "What skills do I need for a data scientist role?",
  "session_id": "optional-session-id"
}

Response: 200 OK
{
  "response": "For a data scientist role...",
  "session_id": "uuid-session-id"
}
```

---

## 7. AI Models & Integration

### Skill Matching Engine

**Technology**: Sentence Transformers (all-MiniLM-L6-v2)

**Algorithm**:
1. Convert skills to embeddings
2. Calculate cosine similarity
3. Apply threshold for semantic matches
4. Rank jobs by combined score

**Code Example**:
```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')
user_embeddings = model.encode(user_skills)
job_embeddings = model.encode(job_skills)
similarities = cosine_similarity(user_embeddings, job_embeddings)
```

### IBM Watsonx Integration

**Purpose**: Job description analysis, career path generation

**Configuration**:
```python
credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": WATSONX_API_KEY
}
client = APIClient(credentials)
```

**Usage**:
- Analyze job descriptions
- Extract required skills
- Generate learning recommendations
- Career path planning

### ChatGPT Integration

**Purpose**: Conversational AI career advisor

**Features**:
- Career guidance
- Interview preparation
- Resume tips
- Skill recommendations

**Implementation**:
```python
response = openai.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
)
```

### IBM SkillsBuild Integration

**Purpose**: Learning resource recommendations

**Features**:
- Course recommendations
- Skill-specific learning paths
- Progress tracking
- Certifications

---

## 8. Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120),
    skills TEXT,  -- JSON array
    experience_level VARCHAR(50),
    desired_role VARCHAR(100),
    points INTEGER DEFAULT 0,
    badges TEXT,  -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Jobs Table
```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(100) NOT NULL,
    required_skills TEXT NOT NULL,  -- JSON array
    preferred_skills TEXT,
    employment_type VARCHAR(50),
    experience_level VARCHAR(50),
    salary_min INTEGER,
    salary_max INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Recommendations Table
```sql
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    job_id INTEGER REFERENCES jobs(id),
    match_score FLOAT NOT NULL,
    matched_skills TEXT,
    missing_skills TEXT,
    skill_gap_percentage FLOAT,
    explanation TEXT,
    viewed BOOLEAN DEFAULT FALSE,
    saved BOOLEAN DEFAULT FALSE,
    applied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 9. Frontend Components

### Dashboard Component

**Location**: `frontend/templates/dashboard.html`

**Features**:
- User statistics cards
- Skills overview
- Top job recommendations
- Skill gap visualization
- AI chatbot widget

**Key JavaScript Functions**:
```javascript
loadUserProfile()      // Load user data
loadRecommendations()  // Fetch job matches
displayUserSkills()    // Render skill badges
sendMessage()          // Chatbot interaction
```

### Profile Component

**Features**:
- Skill tag input
- Experience level selector
- Preference settings
- Progress indicators

---

## 10. Workflow Automation

### Job Alert Agent

**Trigger**: Daily cron job

**Process**:
1. Find users with job alert preference
2. Get new jobs matching their skills
3. Send email notifications
4. Log activity

**Code**: `backend/agents/job_alert_agent.py`

### Notification Agent

**Triggers**:
- New job match
- Skill gap closed
- Badge earned
- Application status update

### Relay Integration

**Purpose**: Complex workflow automation

**Use Cases**:
- Multi-step application processes
- Scheduled skill assessments
- Batch recommendation updates

---

## 11. Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_api/test_users.py

# Run with coverage
pytest --cov=backend tests/
```

### Test Structure

```
tests/
├── test_api/
│   ├── test_auth.py
│   ├── test_recommendations.py
│   └── test_chatbot.py
├── test_services/
│   ├── test_matching_engine.py
│   └── test_watsonx.py
└── test_models/
    └── test_user.py
```

---

## 12. Deployment

### Production Deployment

#### Using Docker

```bash
# Build production image
docker build -t jobmatch-app -f deployment/Dockerfile .

# Run with docker-compose
docker-compose -f deployment/docker-compose.yml up -d
```

#### Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set production environment
export FLASK_ENV=production

# Run with Gunicorn
gunicorn -c deployment/gunicorn_config.py run:app
```

### Environment Setup

1. Set all required environment variables
2. Configure PostgreSQL database
3. Setup Redis for caching
4. Configure Nginx as reverse proxy
5. Enable SSL/TLS certificates

---

## 13. Security

### Best Practices

1. **Authentication**
   - JWT tokens with expiration
   - Secure password hashing (bcrypt)
   - HTTPS only in production

2. **Data Protection**
   - Input validation
   - SQL injection prevention (SQLAlchemy ORM)
   - XSS protection
   - CSRF tokens

3. **API Security**
   - Rate limiting
   - Authentication required
   - CORS configuration

---

## 14. Performance Optimization

### Caching Strategy

```python
# Cache expensive operations
@cache.memoize(timeout=300)
def get_recommendations(user_id):
    # Expensive calculation
    return results
```

### Database Optimization

- Indexes on frequently queried fields
- Query optimization with SQLAlchemy
- Connection pooling

### Frontend Optimization

- Lazy loading
- Asset minification
- CDN for static files
- Browser caching

---

## 15. Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check DATABASE_URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL
```

#### API Key Errors
```bash
# Verify API keys are set
printenv | grep API_KEY
```

#### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python run.py
```

---

## Appendix

### Useful Commands

```bash
# Database migration
flask db upgrade

# Create admin user
python scripts/create_admin.py

# Backup database
pg_dump jobmatch > backup.sql

# Clear cache
redis-cli FLUSHALL
```

### Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [IBM Watsonx Docs](https://www.ibm.com/watsonx)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Sentence Transformers](https://www.sbert.net/)

---

**Last Updated**: January 2026  
**Version**: 1.0.0  
