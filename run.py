"""
Main entry point for the Skill-Based Job Recommendation System
"""
import os
import logging
from backend.app import create_app
from config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create Flask application
app = create_app(get_config())

if __name__ == '__main__':
    # Ensure upload and log directories exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    logger.info(f"Starting application on {host}:{port}")
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=app.config['DEBUG']
    )