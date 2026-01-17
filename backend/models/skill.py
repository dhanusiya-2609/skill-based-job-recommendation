"""
Skill model for skill taxonomy and metadata
"""
from datetime import datetime
from backend.app import db
import json


class Skill(db.Model):
    """Skill taxonomy model"""
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50))  # Programming, Design, Data, etc.
    subcategory = db.Column(db.String(50))  # Languages, Frameworks, Tools, etc.
    
    # Skill metadata
    description = db.Column(db.Text)
    difficulty_level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced, Expert
    
    # Related skills (JSON array of skill names/IDs)
    related_skills = db.Column(db.Text)
    
    # Learning resources
    learning_resources = db.Column(db.Text)  # JSON array of resource objects
    
    # Popularity and demand
    popularity_score = db.Column(db.Float, default=0.0)  # Based on job postings
    demand_trend = db.Column(db.String(20))  # Rising, Stable, Declining
    
    # IBM SkillsBuild integration
    skillsbuild_id = db.Column(db.String(100))
    skillsbuild_courses = db.Column(db.Text)  # JSON array
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, category=None):
        self.name = name
        self.category = category
        self.related_skills = json.dumps([])
        self.learning_resources = json.dumps([])
        self.skillsbuild_courses = json.dumps([])
    
    def get_related_skills(self):
        """Get related skills as Python list"""
        try:
            return json.loads(self.related_skills) if self.related_skills else []
        except:
            return []
    
    def set_related_skills(self, skills_list):
        """Set related skills from Python list"""
        self.related_skills = json.dumps(skills_list)
    
    def get_learning_resources(self):
        """Get learning resources as Python list"""
        try:
            return json.loads(self.learning_resources) if self.learning_resources else []
        except:
            return []
    
    def add_learning_resource(self, resource):
        """Add a learning resource"""
        resources = self.get_learning_resources()
        resources.append(resource)
        self.learning_resources = json.dumps(resources)
    
    def get_skillsbuild_courses(self):
        """Get IBM SkillsBuild courses"""
        try:
            return json.loads(self.skillsbuild_courses) if self.skillsbuild_courses else []
        except:
            return []
    
    def set_skillsbuild_courses(self, courses_list):
        """Set IBM SkillsBuild courses"""
        self.skillsbuild_courses = json.dumps(courses_list)
    
    def to_dict(self):
        """Convert skill to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'subcategory': self.subcategory,
            'description': self.description,
            'difficulty_level': self.difficulty_level,
            'related_skills': self.get_related_skills(),
            'learning_resources': self.get_learning_resources(),
            'popularity_score': self.popularity_score,
            'demand_trend': self.demand_trend,
            'skillsbuild_id': self.skillsbuild_id,
            'skillsbuild_courses': self.get_skillsbuild_courses()
        }
    
    def __repr__(self):
        return f'<Skill {self.name}>'