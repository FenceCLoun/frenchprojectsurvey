import os
import logging
import json
from flask import Flask, request, render_template, redirect, url_for, flash, session
from models import MediaProfile, ResponseStorage
from analyzer import MediaProfileAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret")

# Initialize in-memory storage
response_storage = ResponseStorage()

# Initialize analyzer
analyzer = MediaProfileAnalyzer()

@app.route('/')
def index():
    """Render the homepage with information about the service."""
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive data from Paperform.
    This endpoint expects a JSON payload from Paperform's webhook.
    """
    try:
        # Get the payload from the request
        data = request.json
        logger.debug(f"Received webhook data: {data}")
        
        if not data:
            logger.error("No data received in webhook")
            return {"status": "error", "message": "No data received"}, 400
        
        # Process the form submission
        submission_id = data.get('id', str(len(response_storage.responses) + 1))
        
        # Store the response data
        response_storage.add_response(submission_id, data)
        
        # Process the response to generate a media profile
        profile = analyzer.analyze_response(data)
        
        # Store the profile
        response_storage.add_profile(submission_id, profile)
        
        logger.info(f"Successfully processed submission {submission_id}")
        return {"status": "success", "submission_id": submission_id}, 200
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": str(e)}, 500

@app.route('/result/<submission_id>')
def result(submission_id):
    """
    Display the profile result for a specific submission.
    This is the page users will be redirected to after completing the Paperform survey.
    """
    try:
        profile = response_storage.get_profile(submission_id)
        
        if not profile:
            logger.warning(f"Profile not found for submission {submission_id}")
            flash("Profile not found. The survey may still be processing.", "warning")
            return render_template('error.html', error="Profile not found"), 404
        
        logger.info(f"Displaying results for submission {submission_id}")
        return render_template('profile.html', profile=profile)
    
    except Exception as e:
        logger.error(f"Error displaying results: {str(e)}")
        flash("An error occurred while retrieving your profile.", "danger")
        return render_template('error.html', error=str(e)), 500

@app.route('/demo')
def demo():
    """
    Generate a demo profile for demonstration purposes.
    This allows users to see what a profile looks like without taking the survey.
    """
    try:
        # Create a demo profile with sample data
        demo_data = {
            "formId": "demo",
            "formName": "Media Consumption Survey",
            "data": {
                "tv_hours": "3",
                "movie_frequency": "weekly",
                "book_frequency": "daily",
                "news_source": "online",
                "social_media_hours": "2",
                "podcast_frequency": "weekly",
                "genre_preference": "drama,comedy",
                "content_creation": "sometimes",
                "binge_watching": "occasionally"
            }
        }
        
        profile = analyzer.analyze_response(demo_data)
        submission_id = "demo-" + str(len(response_storage.responses) + 1)
        response_storage.add_response(submission_id, demo_data)
        response_storage.add_profile(submission_id, profile)
        
        logger.info(f"Generated demo profile with ID {submission_id}")
        
        # Redirect to the result page with the demo submission ID
        return redirect(url_for('result', submission_id=submission_id))
    
    except Exception as e:
        logger.error(f"Error generating demo profile: {str(e)}")
        flash("An error occurred while generating a demo profile.", "danger")
        return render_template('error.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
