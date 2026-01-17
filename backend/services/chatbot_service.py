"""
ChatGPT integration service for the AI career chatbot
"""
import openai
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class ChatGPTService:
    """Service for interacting with OpenAI ChatGPT API"""
    
    def __init__(self, api_key=None):
        """Initialize ChatGPT service"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        self.conversation_history = {}
    
    def get_career_advice(self, user_message: str, user_context: Dict = None, conversation_id: str = None) -> str:
        """
        Get career advice from ChatGPT
        
        Args:
            user_message: User's question or message
            user_context: User profile information (skills, experience, etc.)
            conversation_id: ID to maintain conversation context
            
        Returns:
            ChatGPT response as string
        """
        try:
            # Build system message with context
            system_message = self._build_system_message(user_context)
            
            # Get or create conversation history
            if conversation_id:
                messages = self.conversation_history.get(conversation_id, [])
            else:
                messages = []
            
            # Add system message if new conversation
            if not messages:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract assistant response
            assistant_message = response.choices[0].message.content
            
            # Add to conversation history
            messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Save conversation history
            if conversation_id:
                self.conversation_history[conversation_id] = messages[-10:]  # Keep last 10 messages
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"ChatGPT API error: {e}")
            return "I apologize, but I'm having trouble connecting right now. Please try again later."
    
    def _build_system_message(self, user_context: Dict = None) -> str:
        """Build system message with user context"""
        base_message = """You are an expert career advisor and job recommendation assistant. 
        Your role is to help users with:
        - Career guidance and planning
        - Job search strategies
        - Skill development recommendations
        - Resume and interview tips
        - Understanding job market trends
        
        Be encouraging, professional, and provide actionable advice."""
        
        if user_context:
            context_info = "\n\nUser Context:\n"
            
            if user_context.get('skills'):
                context_info += f"Skills: {', '.join(user_context['skills'])}\n"
            
            if user_context.get('experience_level'):
                context_info += f"Experience Level: {user_context['experience_level']}\n"
            
            if user_context.get('desired_role'):
                context_info += f"Desired Role: {user_context['desired_role']}\n"
            
            base_message += context_info
        
        return base_message
    
    def suggest_skills_for_job(self, job_title: str, job_description: str) -> List[str]:
        """Suggest skills needed for a specific job"""
        try:
            prompt = f"""Based on this job posting, list the top 10 most important skills needed:
            
            Job Title: {job_title}
            Description: {job_description}
            
            Provide only the skill names, one per line."""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            skills_text = response.choices[0].message.content
            skills = [s.strip('- ').strip() for s in skills_text.split('\n') if s.strip()]
            
            return skills[:10]
            
        except Exception as e:
            logger.error(f"Error suggesting skills: {e}")
            return []
    
    def generate_learning_path(self, current_skills: List[str], target_skills: List[str]) -> str:
        """Generate a personalized learning path"""
        try:
            prompt = f"""Create a learning path for someone with these current skills: {', '.join(current_skills)}
            
            Who wants to learn these skills: {', '.join(target_skills)}
            
            Provide a structured learning plan with recommended sequence and estimated timeline."""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=600
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating learning path: {e}")
            return "Unable to generate learning path at this time."
    
    def analyze_skill_gap(self, user_skills: List[str], job_skills: List[str]) -> Dict:
        """Analyze skill gap and provide recommendations"""
        try:
            missing_skills = set(job_skills) - set(user_skills)
            
            if not missing_skills:
                return {
                    'gap_analysis': 'You have all the required skills!',
                    'recommendations': []
                }
            
            prompt = f"""A candidate has these skills: {', '.join(user_skills)}
            
            A job requires: {', '.join(job_skills)}
            
            Provide:
            1. Brief analysis of the skill gap
            2. Top 3 priority skills to learn first
            3. How long it might take to acquire them
            
            Be concise and encouraging."""
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=400
            )
            
            return {
                'gap_analysis': response.choices[0].message.content,
                'missing_skills': list(missing_skills)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing skill gap: {e}")
            return {
                'gap_analysis': 'Unable to analyze skill gap.',
                'missing_skills': list(set(job_skills) - set(user_skills))
            }
    
    def clear_conversation(self, conversation_id: str):
        """Clear conversation history"""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]


# Singleton instance
_chatgpt_service = None

def get_chatgpt_service():
    """Get or create ChatGPT service instance"""
    global _chatgpt_service
    if _chatgpt_service is None:
        _chatgpt_service = ChatGPTService()
    return _chatgpt_service