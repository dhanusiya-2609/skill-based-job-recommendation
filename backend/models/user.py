"""
User model for authentication and profile management
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app import db
import json


class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    
    # Profile information
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    experience_level = db.Column(db.String(50))  # Entry, Mid, Senior, Expert
    desired_role = db.Column(db.String(100))
    salary_expectation = db.Column(db.Integer)
    
    # Skills (stored as JSON array)
    skills = db.Column(db.Text)  # JSON array of skill objects
    
    # Preferences
    preferences = db.Column(db.Text)  # JSON object
    
    # Gamification
    points = db.Column(db.Integer, default=0)
    badges = db.Column(db.Text)  # JSON array of badge IDs
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='user', lazy='dynamic')
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
        self.skills = json.dumps([])
        self.badges = json.dumps([])
        self.preferences = json.dumps({})
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def get_skills(self):
        """Get skills as Python list"""
        try:
            return json.loads(self.skills) if self.skills else []
        except:
            return []
    
    def set_skills(self, skills_list):
        """Set skills from Python list"""
        self.skills = json.dumps(skills_list)
    
    def add_skill(self, skill):
        """Add a single skill"""
        skills = self.get_skills()
        if skill not in skills:
            skills.append(skill)
            self.set_skills(skills)
    
    def remove_skill(self, skill):
        """Remove a skill"""
        skills = self.get_skills()
        if skill in skills:
            skills.remove(skill)
            self.set_skills(skills)
    
    def get_badges(self):
        """Get badges as Python list"""
        try:
            return json.loads(self.badges) if self.badges else []
        except:
            return []
    
    def add_badge(self, badge_id):
        """Award a badge"""
        badges = self.get_badges()
        if badge_id not in badges:
            badges.append(badge_id)
            self.badges = json.dumps(badges)
    
    def get_preferences(self):
        """Get preferences as Python dict"""
        try:
            return json.loads(self.preferences) if self.preferences else {}
        except:
            return {}
    
    def set_preferences(self, prefs_dict):
        """Set preferences from Python dict"""
        self.preferences = json.dumps(prefs_dict)
    
    def add_points(self, points):
        """Add gamification points"""
        self.points += points
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'bio': self.bio,
            'location': self.location,
            'experience_level': self.experience_level,
            'desired_role': self.desired_role,
            'salary_expectation': self.salary_expectation,
            'skills': self.get_skills(),
            'preferences': self.get_preferences(),
            'points': self.points,
            'badges': self.get_badges(),
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'