"""
Job model for storing job postings
"""
from datetime import datetime
from backend.app import db
import json


class Job(db.Model):
    """Job posting model"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    company = db.Column(db.String(100), nullable=False, index=True)
    location = db.Column(db.String(100))
    remote = db.Column(db.Boolean, default=False)
    
    # Job details
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)  # JSON array
    responsibilities = db.Column(db.Text)  # JSON array
    
    # Skills required (JSON array)
    required_skills = db.Column(db.Text, nullable=False)
    preferred_skills = db.Column(db.Text)
    
    # Employment details
    employment_type = db.Column(db.String(50))  # Full-time, Part-time, Contract, etc.
    experience_level = db.Column(db.String(50))  # Entry, Mid, Senior, etc.
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    salary_currency = db.Column(db.String(10), default='USD')
    
    # Category and industry
    category = db.Column(db.String(100))  # Software, Data, Design, etc.
    industry = db.Column(db.String(100))  # Tech, Finance, Healthcare, etc.
    
    # Application details
    application_url = db.Column(db.String(500))
    application_email = db.Column(db.String(120))
    
    # Status
    is_active = db.Column(db.Boolean, default=True, index=True)
    featured = db.Column(db.Boolean, default=False)
    
    # Timestamps
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='job', lazy='dynamic')
    
    def __init__(self, title, company, required_skills):
        self.title = title
        self.company = company
        if isinstance(required_skills, list):
            self.required_skills = json.dumps(required_skills)
        else:
            self.required_skills = required_skills
        self.preferred_skills = json.dumps([])
        self.requirements = json.dumps([])
        self.responsibilities = json.dumps([])
    
    def get_required_skills(self):
        """Get required skills as Python list"""
        try:
            return json.loads(self.required_skills) if self.required_skills else []
        except:
            return []
    
    def set_required_skills(self, skills_list):
        """Set required skills from Python list"""
        self.required_skills = json.dumps(skills_list)
    
    def get_preferred_skills(self):
        """Get preferred skills as Python list"""
        try:
            return json.loads(self.preferred_skills) if self.preferred_skills else []
        except:
            return []
    
    def set_preferred_skills(self, skills_list):
        """Set preferred skills from Python list"""
        self.preferred_skills = json.dumps(skills_list)
    
    def get_requirements(self):
        """Get requirements as Python list"""
        try:
            return json.loads(self.requirements) if self.requirements else []
        except:
            return []
    
    def set_requirements(self, req_list):
        """Set requirements from Python list"""
        self.requirements = json.dumps(req_list)
    
    def get_responsibilities(self):
        """Get responsibilities as Python list"""
        try:
            return json.loads(self.responsibilities) if self.responsibilities else []
        except:
            return []
    
    def set_responsibilities(self, resp_list):
        """Set responsibilities from Python list"""
        self.responsibilities = json.dumps(resp_list)
    
    def to_dict(self):
        """Convert job to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'remote': self.remote,
            'description': self.description,
            'requirements': self.get_requirements(),
            'responsibilities': self.get_responsibilities(),
            'required_skills': self.get_required_skills(),
            'preferred_skills': self.get_preferred_skills(),
            'employment_type': self.employment_type,
            'experience_level': self.experience_level,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'salary_currency': self.salary_currency,
            'category': self.category,
            'industry': self.industry,
            'application_url': self.application_url,
            'application_email': self.application_email,
            'is_active': self.is_active,
            'featured': self.featured,
            'posted_date': self.posted_date.isoformat() if self.posted_date else None,
            'deadline': self.deadline.isoformat() if self.deadline else None
        }
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'