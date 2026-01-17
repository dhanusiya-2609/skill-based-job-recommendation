"""
Chatbot API routes for AI career advisor
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.user import User
from backend.services.chatgpt_service import get_chatgpt_service
from backend.services.watsonx_service import get_watsonx_service
from backend.services.gemini_service import get_gemini_service
import logging
import uuid

logger = logging.getLogger(__name__)
chatbot_bp = Blueprint('chatbot', __name__)

# Store conversation sessions
conversation_sessions = {}


@chatbot_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """Send message to AI chatbot and get response"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        message = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Create session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get user context
        user_context = {
            'skills': user.get_skills(),
            'experience_level': user.experience_level,
            'desired_role': user.desired_role,
            'location': user.location
        }
        
        # Use ChatGPT service by default
        chatgpt_service = get_chatgpt_service()
        response = chatgpt_service.get_career_advice(
            message,
            user_context,
            session_id
        )
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'timestamp': None
        }), 200
        
    except Exception as e:
        logger.error(f"Error in chatbot message: {e}")
        return jsonify({
            'error': 'Failed to get response',
            'response': 'I apologize, but I encountered an error. Please try again.'
        }), 500


@chatbot_bp.route('/suggestions', methods=['GET'])
@jwt_required()
def get_suggestions():
    """Get suggested questions/prompts for the user"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Provide contextual suggestions based on user profile
        suggestions = [
            "What skills should I learn to become a better developer?",
            "How can I improve my resume?",
            "What are the current job market trends?",
            "How do I prepare for technical interviews?",
        ]
        
        # Add personalized suggestions
        if user.desired_role:
            suggestions.insert(0, f"What skills do I need for a {user.desired_role} role?")
        
        if user.get_skills():
            suggestions.append(f"What jobs are best for someone with {', '.join(user.get_skills()[:3])} skills?")
        
        return jsonify({
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/career-path', methods=['POST'])
@jwt_required()
def get_career_path():
    """Get personalized career path recommendations"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        target_role = data.get('target_role') or user.desired_role
        
        if not target_role:
            return jsonify({'error': 'Target role is required'}), 400
        
        # Get career path from Watsonx
        watsonx_service = get_watsonx_service()
        career_path = watsonx_service.generate_skill_recommendations(
            user.get_skills(),
            target_role
        )
        
        return jsonify({
            'career_path': career_path,
            'current_skills': user.get_skills(),
            'target_role': target_role
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting career path: {e}")
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/skill-analysis', methods=['POST'])
@jwt_required()
def analyze_skills():
    """Analyze user's skills and provide recommendations"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.get_skills():
            return jsonify({
                'error': 'No skills found. Please add skills to your profile.'
            }), 400
        
        # Get skill analysis from AI
        chatgpt_service = get_chatgpt_service()
        
        # Analyze current skills
        analysis_prompt = f"""Analyze these skills: {', '.join(user.get_skills())}
        
        Provide:
        1. Skill category breakdown
        2. Skill level assessment
        3. Complementary skills to learn
        4. Career opportunities matching these skills
        
        Be specific and actionable."""
        
        analysis = chatgpt_service.get_career_advice(
            analysis_prompt,
            {
                'skills': user.get_skills(),
                'experience_level': user.experience_level
            }
        )
        
        return jsonify({
            'analysis': analysis,
            'skills': user.get_skills()
        }), 200
        
    except Exception as e:
        logger.error(f"Error analyzing skills: {e}")
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/interview-prep', methods=['POST'])
@jwt_required()
def get_interview_prep():
    """Get interview preparation advice"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        job_title = data.get('job_title', 'Software Engineer')
        
        chatgpt_service = get_chatgpt_service()
        
        prep_prompt = f"""Provide interview preparation advice for a {job_title} position.
        
        Candidate's skills: {', '.join(user.get_skills())}
        Experience level: {user.experience_level}
        
        Include:
        1. Common interview questions
        2. Technical topics to review
        3. Behavioral questions to prepare
        4. Tips for success"""
        
        advice = chatgpt_service.get_career_advice(prep_prompt, {
            'skills': user.get_skills(),
            'experience_level': user.experience_level
        })
        
        return jsonify({
            'advice': advice,
            'job_title': job_title
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting interview prep: {e}")
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/session/<session_id>/clear', methods=['DELETE'])
@jwt_required()
def clear_session(session_id):
    """Clear chatbot conversation session"""
    try:
        chatgpt_service = get_chatgpt_service()
        chatgpt_service.clear_conversation(session_id)
        
        return jsonify({
            'message': 'Session cleared successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/quick-tips', methods=['GET'])
@jwt_required()
def get_quick_tips():
    """Get quick career tips"""
    tips = [
        {
            'title': 'Update Your Profile',
            'description': 'Keep your skills and experience up to date for better job matches',
            'icon': 'user-edit'
        },
        {
            'title': 'Learn Continuously',
            'description': 'The tech industry evolves quickly. Dedicate time to learning new skills',
            'icon': 'graduation-cap'
        },
        {
            'title': 'Network Actively',
            'description': 'Connect with professionals in your field. Many jobs are filled through referrals',
            'icon': 'users'
        },
        {
            'title': 'Practice Coding',
            'description': 'Regular coding practice on platforms like LeetCode can help with interviews',
            'icon': 'code'
        },
        {
            'title': 'Build Projects',
            'description': 'Personal projects demonstrate your skills and passion to potential employers',
            'icon': 'project-diagram'
        }
    ]
    
    return jsonify({
        'tips': tips
    }), 200