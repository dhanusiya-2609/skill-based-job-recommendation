"""
Database seeding script with sample data
"""
from backend.app import db
from backend.models.user import User
from backend.models.job import Job
from backend.models.skill import Skill
from backend.models.recommendation import Recommendation
import json


def seed_database():
    """Seed database with sample data"""
    
    print("Seeding database with sample data...")
    
    # Clear existing data
    db.session.query(Recommendation).delete()
    db.session.query(Job).delete()
    db.session.query(Skill).delete()
    db.session.query(User).delete()
    db.session.commit()
    
    # Seed skills
    seed_skills()
    
    # Seed sample users
    seed_users()
    
    # Seed sample jobs
    seed_jobs()
    
    print("Database seeded successfully!")


def seed_skills():
    """Seed skill taxonomy"""
    skills_data = [
        # Programming Languages
        {"name": "Python", "category": "Programming", "subcategory": "Languages", "difficulty_level": "Intermediate"},
        {"name": "JavaScript", "category": "Programming", "subcategory": "Languages", "difficulty_level": "Intermediate"},
        {"name": "Java", "category": "Programming", "subcategory": "Languages", "difficulty_level": "Intermediate"},
        {"name": "C++", "category": "Programming", "subcategory": "Languages", "difficulty_level": "Advanced"},
        {"name": "SQL", "category": "Data", "subcategory": "Languages", "difficulty_level": "Beginner"},
        
        # Frameworks
        {"name": "React", "category": "Programming", "subcategory": "Frameworks", "difficulty_level": "Intermediate"},
        {"name": "Django", "category": "Programming", "subcategory": "Frameworks", "difficulty_level": "Intermediate"},
        {"name": "Flask", "category": "Programming", "subcategory": "Frameworks", "difficulty_level": "Beginner"},
        {"name": "Spring Boot", "category": "Programming", "subcategory": "Frameworks", "difficulty_level": "Advanced"},
        
        # Cloud & DevOps
        {"name": "AWS", "category": "Cloud", "subcategory": "Platforms", "difficulty_level": "Intermediate"},
        {"name": "Docker", "category": "DevOps", "subcategory": "Tools", "difficulty_level": "Intermediate"},
        {"name": "Kubernetes", "category": "DevOps", "subcategory": "Tools", "difficulty_level": "Advanced"},
        {"name": "CI/CD", "category": "DevOps", "subcategory": "Practices", "difficulty_level": "Intermediate"},
        
        # Data Science & AI
        {"name": "Machine Learning", "category": "AI/ML", "subcategory": "Techniques", "difficulty_level": "Advanced"},
        {"name": "TensorFlow", "category": "AI/ML", "subcategory": "Frameworks", "difficulty_level": "Advanced"},
        {"name": "Data Analysis", "category": "Data", "subcategory": "Analysis", "difficulty_level": "Intermediate"},
        {"name": "pandas", "category": "Data", "subcategory": "Libraries", "difficulty_level": "Intermediate"},
        
        # Soft Skills
        {"name": "Communication", "category": "Soft Skills", "subcategory": "Interpersonal", "difficulty_level": "Beginner"},
        {"name": "Problem Solving", "category": "Soft Skills", "subcategory": "Analytical", "difficulty_level": "Beginner"},
        {"name": "Leadership", "category": "Soft Skills", "subcategory": "Management", "difficulty_level": "Intermediate"},
    ]
    
    for skill_data in skills_data:
        skill = Skill(**skill_data)
        skill.description = f"Professional skill in {skill_data['name']}"
        skill.popularity_score = 0.8
        skill.demand_trend = "Rising"
        db.session.add(skill)
    
    db.session.commit()
    print(f"✓ Seeded {len(skills_data)} skills")


def seed_users():
    """Seed sample users"""
    users_data = [
        {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123",
            "full_name": "John Doe",
            "experience_level": "Mid-Level",
            "desired_role": "Full Stack Developer",
            "skills": ["Python", "JavaScript", "React", "SQL", "Docker"]
        },
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "password": "password123",
            "full_name": "Jane Smith",
            "experience_level": "Senior",
            "desired_role": "Data Scientist",
            "skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis", "pandas"]
        },
        {
            "username": "demo_user",
            "email": "demo@example.com",
            "password": "demo123",
            "full_name": "Demo User",
            "experience_level": "Entry",
            "desired_role": "Software Engineer",
            "skills": ["Python", "JavaScript", "SQL"]
        }
    ]
    
    for user_data in users_data:
        skills = user_data.pop('skills')
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        user.full_name = user_data.get('full_name')
        user.experience_level = user_data.get('experience_level')
        user.desired_role = user_data.get('desired_role')
        user.set_skills(skills)
        user.location = "San Francisco, CA"
        user.bio = f"Passionate {user_data.get('desired_role', 'professional')} looking for opportunities"
        user.is_verified = True
        user.points = 100
        
        db.session.add(user)
    
    db.session.commit()
    print(f"✓ Seeded {len(users_data)} users")


def seed_jobs():
    """Seed sample job postings"""
    jobs_data = [
        {
            "title": "Senior Python Developer",
            "company": "Tech Innovators Inc.",
            "location": "San Francisco, CA",
            "remote": True,
            "description": "We're looking for an experienced Python developer to join our growing team.",
            "required_skills": ["Python", "Django", "SQL", "Docker", "AWS"],
            "preferred_skills": ["React", "Kubernetes"],
            "employment_type": "Full-time",
            "experience_level": "Senior",
            "salary_min": 120000,
            "salary_max": 160000,
            "category": "Software Engineering",
            "industry": "Technology"
        },
        {
            "title": "Full Stack JavaScript Developer",
            "company": "StartupXYZ",
            "location": "Remote",
            "remote": True,
            "description": "Join our innovative startup as a full stack developer working with modern JavaScript technologies.",
            "required_skills": ["JavaScript", "React", "Node.js", "SQL", "Git"],
            "preferred_skills": ["TypeScript", "MongoDB", "AWS"],
            "employment_type": "Full-time",
            "experience_level": "Mid-Level",
            "salary_min": 90000,
            "salary_max": 130000,
            "category": "Software Engineering",
            "industry": "Technology"
        },
        {
            "title": "Data Scientist",
            "company": "DataCorp Analytics",
            "location": "New York, NY",
            "remote": False,
            "description": "Seeking a data scientist to help drive insights from large datasets.",
            "required_skills": ["Python", "Machine Learning", "pandas", "Data Analysis", "SQL"],
            "preferred_skills": ["TensorFlow", "AWS", "Spark"],
            "employment_type": "Full-time",
            "experience_level": "Mid-Level",
            "salary_min": 100000,
            "salary_max": 140000,
            "category": "Data Science",
            "industry": "Analytics"
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudOps Solutions",
            "location": "Austin, TX",
            "remote": True,
            "description": "Looking for DevOps engineer to manage cloud infrastructure and CI/CD pipelines.",
            "required_skills": ["Docker", "Kubernetes", "AWS", "CI/CD", "Python"],
            "preferred_skills": ["Terraform", "Ansible", "Jenkins"],
            "employment_type": "Full-time",
            "experience_level": "Mid-Level",
            "salary_min": 110000,
            "salary_max": 150000,
            "category": "DevOps",
            "industry": "Cloud Services"
        },
        {
            "title": "Junior Software Engineer",
            "company": "Growing Tech Co.",
            "location": "Seattle, WA",
            "remote": False,
            "description": "Entry-level position for recent graduates or career changers.",
            "required_skills": ["Python", "JavaScript", "SQL", "Git"],
            "preferred_skills": ["React", "Docker"],
            "employment_type": "Full-time",
            "experience_level": "Entry",
            "salary_min": 70000,
            "salary_max": 90000,
            "category": "Software Engineering",
            "industry": "Technology"
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Innovations",
            "location": "Boston, MA",
            "remote": True,
            "description": "Build and deploy machine learning models at scale.",
            "required_skills": ["Python", "Machine Learning", "TensorFlow", "AWS", "Docker"],
            "preferred_skills": ["Kubernetes", "MLOps", "PyTorch"],
            "employment_type": "Full-time",
            "experience_level": "Senior",
            "salary_min": 130000,
            "salary_max": 180000,
            "category": "AI/ML",
            "industry": "Artificial Intelligence"
        },
        {
            "title": "Frontend Developer",
            "company": "Web Design Studio",
            "location": "Los Angeles, CA",
            "remote": True,
            "description": "Create beautiful, responsive web applications.",
            "required_skills": ["JavaScript", "React", "CSS", "HTML"],
            "preferred_skills": ["TypeScript", "Next.js", "Tailwind"],
            "employment_type": "Full-time",
            "experience_level": "Mid-Level",
            "salary_min": 85000,
            "salary_max": 120000,
            "category": "Frontend Development",
            "industry": "Digital Agency"
        },
        {
            "title": "Backend Engineer",
            "company": "Enterprise Solutions",
            "location": "Chicago, IL",
            "remote": False,
            "description": "Design and implement scalable backend systems.",
            "required_skills": ["Java", "Spring Boot", "SQL", "Microservices"],
            "preferred_skills": ["Kubernetes", "MongoDB", "Kafka"],
            "employment_type": "Full-time",
            "experience_level": "Senior",
            "salary_min": 115000,
            "salary_max": 155000,
            "category": "Backend Development",
            "industry": "Enterprise Software"
        }
    ]
    
    for job_data in jobs_data:
        job = Job(
            title=job_data['title'],
            company=job_data['company'],
            required_skills=job_data['required_skills']
        )
        
        # Set other fields
        for key, value in job_data.items():
            if key not in ['title', 'company', 'required_skills'] and hasattr(job, key):
                if key == 'preferred_skills':
                    job.set_preferred_skills(value)
                else:
                    setattr(job, key, value)
        
        job.set_requirements([
            "Bachelor's degree or equivalent experience",
            "Strong problem-solving skills",
            "Excellent communication abilities"
        ])
        
        job.set_responsibilities([
            "Write clean, maintainable code",
            "Collaborate with team members",
            "Participate in code reviews"
        ])
        
        job.application_url = f"https://example.com/apply/{job_data['company'].lower().replace(' ', '-')}"
        
        db.session.add(job)
    
    db.session.commit()
    print(f"✓ Seeded {len(jobs_data)} jobs")


if __name__ == '__main__':
    from backend.app import create_app
    from config import get_config
    
    app = create_app(get_config())
    with app.app_context():
        seed_database()