"""
Recommendation model for storing job recommendations
"""
from datetime import datetime
from backend.app import db
import json


class Recommendation(db.Model):
    """Job recommendation model"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    
    # Recommendation score and details
    match_score = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    confidence = db.Column(db.Float)  # AI confidence in recommendation
    
    # Skill matching details
    matched_skills = db.Column(db.Text)  # JSON array of matched skills
    missing_skills = db.Column(db.Text)  # JSON array of skills user needs
    skill_gap_percentage = db.Column(db.Float)  # Percentage of skills missing
    
    # Explanation for the recommendation
    explanation = db.Column(db.Text)
    
    # Learning path suggestions
    suggested_courses = db.Column(db.Text)  # JSON array of course recommendations
    
    # User interaction
    viewed = db.Column(db.Boolean, default=False)
    saved = db.Column(db.Boolean, default=False)
    applied = db.Column(db.Boolean, default=False)
    
    # User feedback
    feedback_rating = db.Column(db.Integer)  # 1-5 stars
    feedback_comment = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    viewed_at = db.Column(db.DateTime)
    applied_at = db.Column(db.DateTime)
    
    def __init__(self, user_id, job_id, match_score):
        self.user_id = user_id
        self.job_id = job_id
        self.match_score = match_score
        self.matched_skills = json.dumps([])
        self.missing_skills = json.dumps([])
        self.suggested_courses = json.dumps([])
    
    def get_matched_skills(self):
        """Get matched skills as Python list"""
        try:
            return json.loads(self.matched_skills) if self.matched_skills else []
        except:
            return []
    
    def set_matched_skills(self, skills_list):
        """Set matched skills from Python list"""
        self.matched_skills = json.dumps(skills_list)
    
    def get_missing_skills(self):
        """Get missing skills as Python list"""
        try:
            return json.loads(self.missing_skills) if self.missing_skills else []
        except:
            return []
    
    def set_missing_skills(self, skills_list):
        """Set missing skills from Python list"""
        self.missing_skills = json.dumps(skills_list)
    
    def get_suggested_courses(self):
        """Get suggested courses as Python list"""
        try:
            return json.loads(self.suggested_courses) if self.suggested_courses else []
        except:
            return []
    
    def set_suggested_courses(self, courses_list):
        """Set suggested courses from Python list"""
        self.suggested_courses = json.dumps(courses_list)
    
    def mark_viewed(self):
        """Mark recommendation as viewed"""
        if not self.viewed:
            self.viewed = True
            self.viewed_at = datetime.utcnow()
    
    def mark_applied(self):
        """Mark as applied"""
        if not self.applied:
            self.applied = True
            self.applied_at = datetime.utcnow()
    
    def to_dict(self, include_job=False, include_user=False):
        """Convert recommendation to dictionary"""
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'match_score': self.match_score,
            'confidence': self.confidence,
            'matched_skills': self.get_matched_skills(),
            'missing_skills': self.get_missing_skills(),
            'skill_gap_percentage': self.skill_gap_percentage,
            'explanation': self.explanation,
            'suggested_courses': self.get_suggested_courses(),
            'viewed': self.viewed,
            'saved': self.saved,
            'applied': self.applied,
            'feedback_rating': self.feedback_rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'viewed_at': self.viewed_at.isoformat() if self.viewed_at else None,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None
        }
        
        if include_job and self.job:
            result['job'] = self.job.to_dict()
        
        if include_user and self.user:
            result['user'] = self.user.to_dict()
        
        return result
    
    def __repr__(self):
        return f'<Recommendation User:{self.user_id} Job:{self.job_id} Score:{self.match_score}>'