"""
IBM Watsonx AI integration service
"""
import os
import logging
from ibm_watson_machine_learning import APIClient
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

logger = logging.getLogger(__name__)


class WatsonxService:
    """Service for IBM Watsonx AI integration"""
    
    def __init__(self):
        """Initialize Watsonx service"""
        self.api_key = os.getenv('IBM_WATSONX_API_KEY')
        self.project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
        self.url = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
        
        self.credentials = {
            "url": self.url,
            "apikey": self.api_key
        }
        
        self.client = None
        self.model = None
        
        if self.api_key and self.project_id:
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Watson ML client"""
        try:
            self.client = APIClient(self.credentials)
            logger.info("Watsonx client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Watsonx client: {e}")
    
    def generate_job_description_analysis(self, job_description):
        """
        Analyze job description and extract key information
        
        Args:
            job_description: Job description text
            
        Returns:
            dict: Analyzed job information
        """
        if not self.client:
            logger.warning("Watsonx client not initialized, using fallback")
            return self._fallback_analysis(job_description)
        
        try:
            model_id = os.getenv('IBM_GRANITE_MODEL_ID', 'ibm/granite-13b-chat-v2')
            
            parameters = {
                GenParams.DECODING_METHOD: "greedy",
                GenParams.MAX_NEW_TOKENS: 500,
                GenParams.TEMPERATURE: 0.3,
            }
            
            model = Model(
                model_id=model_id,
                params=parameters,
                credentials=self.credentials,
                project_id=self.project_id
            )
            
            prompt = f"""Analyze this job description and extract:
1. Required skills (list)
2. Preferred skills (list)
3. Experience level required
4. Key responsibilities (list)
5. Job category

Job Description:
{job_description}

Provide response in JSON format."""
            
            response = model.generate_text(prompt=prompt)
            
            # Parse and return the response
            return self._parse_watsonx_response(response)
            
        except Exception as e:
            logger.error(f"Watsonx analysis error: {e}")
            return self._fallback_analysis(job_description)
    
    def generate_skill_recommendations(self, current_skills, target_role):
        """
        Generate skill recommendations for a target role
        
        Args:
            current_skills: List of current skills
            target_role: Desired job role
            
        Returns:
            dict: Skill recommendations and learning path
        """
        if not self.client:
            return self._fallback_recommendations(current_skills, target_role)
        
        try:
            model_id = os.getenv('IBM_GRANITE_MODEL_ID', 'ibm/granite-13b-chat-v2')
            
            parameters = {
                GenParams.DECODING_METHOD: "sample",
                GenParams.MAX_NEW_TOKENS: 600,
                GenParams.TEMPERATURE: 0.7,
            }
            
            model = Model(
                model_id=model_id,
                params=parameters,
                credentials=self.credentials,
                project_id=self.project_id
            )
            
            prompt = f"""Given a person with these skills: {', '.join(current_skills)}

Who wants to become a {target_role}, provide:
1. Skills they should learn (prioritized list)
2. Estimated learning timeline for each skill
3. Recommended learning sequence
4. Industry certifications that would help

Provide response in JSON format."""
            
            response = model.generate_text(prompt=prompt)
            
            return self._parse_skill_recommendations(response)
            
        except Exception as e:
            logger.error(f"Watsonx skill recommendations error: {e}")
            return self._fallback_recommendations(current_skills, target_role)
    
    def generate_career_advice(self, user_profile, question):
        """
        Generate personalized career advice using Watsonx
        
        Args:
            user_profile: User profile information
            question: User's career question
            
        Returns:
            str: AI-generated career advice
        """
        if not self.client:
            return "I apologize, but the AI service is currently unavailable. Please try again later."
        
        try:
            model_id = os.getenv('IBM_GRANITE_MODEL_ID', 'ibm/granite-13b-chat-v2')
            
            parameters = {
                GenParams.DECODING_METHOD: "sample",
                GenParams.MAX_NEW_TOKENS: 400,
                GenParams.TEMPERATURE: 0.7,
            }
            
            model = Model(
                model_id=model_id,
                params=parameters,
                credentials=self.credentials,
                project_id=self.project_id
            )
            
            context = f"""User Profile:
Skills: {', '.join(user_profile.get('skills', []))}
Experience Level: {user_profile.get('experience_level', 'Not specified')}
Desired Role: {user_profile.get('desired_role', 'Not specified')}

Question: {question}

Provide helpful, actionable career advice."""
            
            response = model.generate_text(prompt=context)
            
            return response
            
        except Exception as e:
            logger.error(f"Watsonx career advice error: {e}")
            return "I'm having trouble generating advice right now. Please try rephrasing your question."
    
    def _parse_watsonx_response(self, response):
        """Parse Watsonx JSON response"""
        try:
            import json
            # Try to extract JSON from response
            if isinstance(response, str):
                # Find JSON in response
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response[start:end]
                    return json.loads(json_str)
            return response
        except:
            return {"raw_response": response}
    
    def _parse_skill_recommendations(self, response):
        """Parse skill recommendations from Watsonx"""
        try:
            import json
            if isinstance(response, str):
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    return json.loads(response[start:end])
            return response
        except:
            return {"recommendations": [], "raw_response": response}
    
    def _fallback_analysis(self, job_description):
        """Fallback analysis when Watsonx is unavailable"""
        # Simple keyword-based extraction
        common_skills = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes']
        found_skills = [skill for skill in common_skills if skill.lower() in job_description.lower()]
        
        return {
            "required_skills": found_skills,
            "preferred_skills": [],
            "experience_level": "Mid-Level",
            "responsibilities": [],
            "category": "Technology"
        }
    
    def _fallback_recommendations(self, current_skills, target_role):
        """Fallback recommendations when Watsonx is unavailable"""
        return {
            "recommended_skills": ["Communication", "Problem Solving", "Leadership"],
            "timeline": "3-6 months",
            "sequence": ["Start with fundamentals", "Build practical projects", "Get certified"]
        }


# Singleton instance
_watsonx_service = None

def get_watsonx_service():
    """Get or create Watsonx service instance"""
    global _watsonx_service
    if _watsonx_service is None:
        _watsonx_service = WatsonxService()
    return _watsonx_service