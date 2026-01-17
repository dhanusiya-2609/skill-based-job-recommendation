"""
AI-powered skill matching engine for job recommendations
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class SkillMatchingEngine:
    """Advanced skill matching using NLP and semantic similarity"""
    
    def __init__(self):
        """Initialize the matching engine"""
        try:
            # Load sentence transformer model for semantic similarity
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer model loaded successfully")
        except:
            # Fallback to TF-IDF if sentence transformers not available
            self.model = None
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
            logger.warning("Using TF-IDF vectorizer as fallback")
    
    def calculate_skill_match(self, user_skills, job_skills):
        """
        Calculate match score between user skills and job requirements
        
        Args:
            user_skills: List of user's skills
            job_skills: List of required job skills
            
        Returns:
            dict: Match score and detailed breakdown
        """
        if not user_skills or not job_skills:
            return {
                'match_score': 0.0,
                'matched_skills': [],
                'missing_skills': job_skills,
                'skill_gap_percentage': 100.0
            }
        
        # Normalize skills
        user_skills_lower = [s.lower().strip() for s in user_skills]
        job_skills_lower = [s.lower().strip() for s in job_skills]
        
        # Find exact matches
        exact_matches = set(user_skills_lower) & set(job_skills_lower)
        missing_skills = set(job_skills_lower) - set(user_skills_lower)
        
        # Calculate semantic similarity for non-exact matches
        semantic_matches = self._calculate_semantic_matches(
            list(set(user_skills_lower) - exact_matches),
            list(missing_skills)
        )
        
        # Combine exact and semantic matches
        total_matched = len(exact_matches) + len(semantic_matches)
        match_score = total_matched / len(job_skills_lower)
        
        # Update missing skills after semantic matching
        for user_skill, job_skill, similarity in semantic_matches:
            if similarity > 0.7:  # High confidence semantic match
                missing_skills.discard(job_skill)
        
        skill_gap = (len(missing_skills) / len(job_skills_lower)) * 100
        
        return {
            'match_score': round(match_score, 3),
            'matched_skills': list(exact_matches) + [m[0] for m in semantic_matches],
            'missing_skills': list(missing_skills),
            'skill_gap_percentage': round(skill_gap, 2),
            'exact_matches': list(exact_matches),
            'semantic_matches': [(m[0], m[1], round(m[2], 3)) for m in semantic_matches]
        }
    
    def _calculate_semantic_matches(self, user_skills, job_skills, threshold=0.6):
        """Calculate semantic similarity between skills using embeddings"""
        if not user_skills or not job_skills:
            return []
        
        semantic_matches = []
        
        try:
            if self.model:
                # Use sentence transformers
                user_embeddings = self.model.encode(user_skills)
                job_embeddings = self.model.encode(job_skills)
                
                # Calculate cosine similarity
                similarities = cosine_similarity(user_embeddings, job_embeddings)
                
                for i, user_skill in enumerate(user_skills):
                    for j, job_skill in enumerate(job_skills):
                        similarity = similarities[i][j]
                        if similarity >= threshold:
                            semantic_matches.append((user_skill, job_skill, similarity))
            else:
                # Fallback to simple TF-IDF
                all_skills = user_skills + job_skills
                tfidf_matrix = self.vectorizer.fit_transform(all_skills)
                
                user_vectors = tfidf_matrix[:len(user_skills)]
                job_vectors = tfidf_matrix[len(user_skills):]
                
                similarities = cosine_similarity(user_vectors, job_vectors)
                
                for i, user_skill in enumerate(user_skills):
                    for j, job_skill in enumerate(job_skills):
                        similarity = similarities[i][j]
                        if similarity >= threshold:
                            semantic_matches.append((user_skill, job_skill, similarity))
        
        except Exception as e:
            logger.error(f"Error in semantic matching: {e}")
        
        # Sort by similarity score
        semantic_matches.sort(key=lambda x: x[2], reverse=True)
        
        return semantic_matches
    
    def rank_jobs(self, user_profile, jobs):
        """
        Rank jobs based on match score with user profile
        
        Args:
            user_profile: User object with skills and preferences
            jobs: List of Job objects
            
        Returns:
            List of (job, match_details) tuples sorted by match score
        """
        ranked_jobs = []
        user_skills = user_profile.get_skills()
        
        for job in jobs:
            job_skills = job.get_required_skills()
            match_result = self.calculate_skill_match(user_skills, job_skills)
            
            # Apply preference multipliers
            final_score = self._apply_preferences(
                match_result['match_score'],
                user_profile,
                job
            )
            
            match_result['final_score'] = final_score
            ranked_jobs.append((job, match_result))
        
        # Sort by final score
        ranked_jobs.sort(key=lambda x: x[1]['final_score'], reverse=True)
        
        return ranked_jobs
    
    def _apply_preferences(self, base_score, user_profile, job):
        """Apply user preferences to adjust match score"""
        score = base_score
        
        # Location preference
        if user_profile.location and job.location:
            if user_profile.location.lower() in job.location.lower():
                score *= 1.1  # 10% bonus
        
        # Remote work preference
        prefs = user_profile.get_preferences()
        if prefs.get('remote_only') and job.remote:
            score *= 1.15  # 15% bonus
        
        # Experience level match
        if user_profile.experience_level and job.experience_level:
            if user_profile.experience_level == job.experience_level:
                score *= 1.05  # 5% bonus
        
        # Salary range
        if user_profile.salary_expectation and job.salary_min:
            if user_profile.salary_expectation >= job.salary_min:
                score *= 1.05
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def generate_explanation(self, match_details, job):
        """Generate human-readable explanation for recommendation"""
        score = match_details['match_score']
        matched = len(match_details['matched_skills'])
        total = matched + len(match_details['missing_skills'])
        
        explanation = f"You match {matched} out of {total} required skills ({score*100:.0f}% match). "
        
        if match_details['matched_skills']:
            top_matches = match_details['matched_skills'][:3]
            explanation += f"Your skills in {', '.join(top_matches)} align well with this position. "
        
        if match_details['missing_skills']:
            explanation += f"To strengthen your application, consider developing: {', '.join(match_details['missing_skills'][:3])}."
        
        return explanation


# Singleton instance
_matching_engine = None

def get_matching_engine():
    """Get or create matching engine instance"""
    global _matching_engine
    if _matching_engine is None:
        _matching_engine = SkillMatchingEngine()
    return _matching_engine