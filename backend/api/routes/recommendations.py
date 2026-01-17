"""
Recommendations API routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app import db
from backend.models.user import User
from backend.models.job import Job
from backend.models.recommendation import Recommendation
from backend.services.matching_engine import get_matching_engine
from backend.services.chatgpt_service import get_chatgpt_service
from backend.services.watsonx_service import get_watsonx_service
import logging

logger = logging.getLogger(__name__)
recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get job recommendations for current user"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if user has skills
        if not user.get_skills():
            return jsonify({
                'message': 'Please add skills to your profile to get recommendations',
                'recommendations': []
            }), 200
        
        # Get active jobs
        jobs = Job.query.filter_by(is_active=True).all()
        
        if not jobs:
            return jsonify({
                'message': 'No active jobs available',
                'recommendations': []
            }), 200
        
        # Get matching engine and rank jobs
        matching_engine = get_matching_engine()
        ranked_jobs = matching_engine.rank_jobs(user, jobs)
        
        # Store or update recommendations in database
        recommendations = []
        for job, match_details in ranked_jobs[:20]:  # Top 20 recommendations
            
            # Check if recommendation exists
            rec = Recommendation.query.filter_by(
                user_id=user.id,
                job_id=job.id
            ).first()
            
            if not rec:
                rec = Recommendation(
                    user_id=user.id,
                    job_id=job.id,
                    match_score=match_details['final_score']
                )
            else:
                rec.match_score = match_details['final_score']
            
            # Update recommendation details
            rec.confidence = match_details.get('final_score', 0.0)
            rec.set_matched_skills(match_details.get('matched_skills', []))
            rec.set_missing_skills(match_details.get('missing_skills', []))
            rec.skill_gap_percentage = match_details.get('skill_gap_percentage', 0.0)
            rec.explanation = matching_engine.generate_explanation(match_details, job)
            
            db.session.add(rec)
            
            recommendations.append({
                **rec.to_dict(),
                'job': job.to_dict()
            })
        
        db.session.commit()
        
        return jsonify({
            'recommendations': recommendations,
            'total': len(recommendations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/<int:rec_id>', methods=['GET'])
@jwt_required()
def get_recommendation_detail(rec_id):
    """Get detailed recommendation"""
    try:
        current_user_id = get_jwt_identity()
        rec = Recommendation.query.get(rec_id)
        
        if not rec or rec.user_id != current_user_id:
            return jsonify({'error': 'Recommendation not found'}), 404
        
        # Mark as viewed
        rec.mark_viewed()
        db.session.commit()
        
        return jsonify({
            'recommendation': rec.to_dict(include_job=True)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting recommendation detail: {e}")
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/<int:rec_id>/save', methods=['POST'])
@jwt_required()
def save_recommendation(rec_id):
    """Save recommendation for later"""
    try:
        current_user_id = get_jwt_identity()
        rec = Recommendation.query.get(rec_id)
        
        if not rec or rec.user_id != current_user_id:
            return jsonify({'error': 'Recommendation not found'}), 404
        
        rec.saved = not rec.saved  # Toggle saved status
        db.session.commit()
        
        return jsonify({
            'message': 'Saved' if rec.saved else 'Unsaved',
            'saved': rec.saved
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error saving recommendation: {e}")
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/<int:rec_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_job(rec_id):
    """Mark recommendation as applied"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        rec = Recommendation.query.get(rec_id)
        
        if not rec or rec.user_id != current_user_id:
            return jsonify({'error': 'Recommendation not found'}), 404
        
        rec.mark_applied()
        
        # Award points for applying
        user.add_points(10)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Application recorded successfully',
            'points_earned': 10
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error applying to job: {e}")
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/<int:rec_id>/feedback', methods=['POST'])
@jwt_required()
def submit_feedback(rec_id):
    """Submit feedback on recommendation"""
    try:
        current_user_id = get_jwt_identity()
        rec = Recommendation.query.get(rec_id)
        
        if not rec or rec.user_id != current_user_id:
            return jsonify({'error': 'Recommendation not found'}), 404
        
        data = request.get_json()
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if rating and 1 <= rating <= 5:
            rec.feedback_rating = rating
            rec.feedback_comment = comment
            db.session.commit()
            
            return jsonify({
                'message': 'Feedback submitted successfully'
            }), 200
        else:
            return jsonify({'error': 'Invalid rating. Must be 1-5'}), 400
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error submitting feedback: {e}")
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/skill-gap/<int:job_id>', methods=['GET'])
@jwt_required()
def get_skill_gap_analysis(job_id):
    """Get detailed skill gap analysis for a job"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        job = Job.query.get(job_id)
        
        if not user or not job:
            return jsonify({'error': 'User or job not found'}), 404
        
        # Get skill gap analysis from AI
        chatgpt_service = get_chatgpt_service()
        gap_analysis = chatgpt_service.analyze_skill_gap(
            user.get_skills(),
            job.get_required_skills()
        )
        
        # Get learning path suggestions
        watsonx_service = get_watsonx_service()
        learning_path = watsonx_service.generate_skill_recommendations(
            user.get_skills(),
            job.title
        )
        
        return jsonify({
            'job': job.to_dict(),
            'gap_analysis': gap_analysis,
            'learning_path': learning_path
        }), 200
        
    except Exception as e:
        logger.error(f"Error in skill gap analysis: {e}")
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_recommendations():
    """Force refresh recommendations"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete old recommendations
        Recommendation.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        
        # Trigger new recommendations
        return get_recommendations()
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error refreshing recommendations: {e}")
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/saved', methods=['GET'])
@jwt_required()
def get_saved_recommendations():
    """Get all saved recommendations"""
    try:
        current_user_id = get_jwt_identity()
        
        saved_recs = Recommendation.query.filter_by(
            user_id=current_user_id,
            saved=True
        ).all()
        
        recommendations = [rec.to_dict(include_job=True) for rec in saved_recs]
        
        return jsonify({
            'recommendations': recommendations,
            'total': len(recommendations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting saved recommendations: {e}")
        return jsonify({'error': str(e)}), 500


@recommendations_bp.route('/applied', methods=['GET'])
@jwt_required()
def get_applied_recommendations():
    """Get all applied recommendations"""
    try:
        current_user_id = get_jwt_identity()
        
        applied_recs = Recommendation.query.filter_by(
            user_id=current_user_id,
            applied=True
        ).all()
        
        recommendations = [rec.to_dict(include_job=True) for rec in applied_recs]
        
        return jsonify({
            'recommendations': recommendations,
            'total': len(recommendations)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting applied recommendations: {e}")
        return jsonify({'error': str(e)}), 500