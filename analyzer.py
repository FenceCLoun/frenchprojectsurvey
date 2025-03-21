import pandas as pd
import logging
from models import MediaProfile

# Configure logging
logger = logging.getLogger(__name__)

class MediaProfileAnalyzer:
    """
    Analyzes media consumption survey responses to generate personalized 
    media personality profiles.
    """
    
    def __init__(self):
        """Initialize the analyzer with profile types and trait categories."""
        # Define media consumption personality profile types
        self.profile_types = {
            "Digital Native": "You were born into the digital age and navigate various media platforms with ease.",
            "Classic Consumer": "You prefer traditional media formats and value quality over quantity.",
            "Content Creator": "You not only consume media but actively create and share your own content.",
            "Information Seeker": "You primarily use media to stay informed and educated on current events.",
            "Entertainment Enthusiast": "You're all about entertainment and use media primarily for enjoyment.",
            "Balanced Consumer": "You maintain a healthy balance across different media platforms.",
            "Social Media Maven": "Social media dominates your media consumption habits."
        }
        
        # Define trait categories for analysis
        self.trait_categories = [
            "digital_engagement",
            "traditional_media_preference",
            "content_creation_tendency",
            "information_seeking",
            "entertainment_focus",
            "consumption_balance",
            "social_media_engagement"
        ]
        
        # Define descriptions for trait scores
        self.trait_descriptions = {
            "digital_engagement": {
                "low": "You tend to limit your engagement with digital media platforms.",
                "medium": "You have a moderate level of engagement with digital media.",
                "high": "You're highly engaged with various digital media platforms."
            },
            "traditional_media_preference": {
                "low": "You rarely consume traditional media formats like print or broadcast TV.",
                "medium": "You occasionally engage with traditional media alongside digital options.",
                "high": "You strongly prefer traditional media formats over newer digital options."
            },
            "content_creation_tendency": {
                "low": "You primarily consume content rather than creating your own.",
                "medium": "You occasionally create and share your own media content.",
                "high": "You regularly create and share your own media content across platforms."
            },
            "information_seeking": {
                "low": "Entertainment is your primary media motivation, rather than information.",
                "medium": "You balance entertainment with staying informed through media.",
                "high": "Your media habits are strongly driven by a desire to stay informed and educated."
            },
            "entertainment_focus": {
                "low": "You use media primarily for practical purposes rather than entertainment.",
                "medium": "Entertainment is important in your media diet, but balanced with other goals.",
                "high": "Entertainment is the primary driver of your media consumption habits."
            },
            "consumption_balance": {
                "low": "Your media consumption tends to focus heavily on just one or two types.",
                "medium": "You have some variety in your media consumption patterns.",
                "high": "You maintain a diverse and balanced media diet across multiple formats."
            },
            "social_media_engagement": {
                "low": "You limit your time on social media platforms.",
                "medium": "You use social media regularly but in moderation.",
                "high": "Social media is a central component of your daily media consumption."
            }
        }
        
        # Content recommendations based on profile types
        self.recommendations = {
            "Digital Native": [
                "Explore digital detox apps to balance your screen time",
                "Try interactive content like choice-based streaming shows",
                "Check out emerging media formats like AR/VR experiences"
            ],
            "Classic Consumer": [
                "Explore subscription services for traditional media formats",
                "Consider high-quality documentary series on streaming platforms",
                "Look into podcasts that cover classic literature or film analysis"
            ],
            "Content Creator": [
                "Invest time in learning advanced editing software",
                "Join creator communities for your preferred media format",
                "Explore monetization strategies for your content"
            ],
            "Information Seeker": [
                "Consider premium news subscriptions for in-depth reporting",
                "Try curated newsletter services that aggregate quality journalism",
                "Explore educational podcasts and documentaries"
            ],
            "Entertainment Enthusiast": [
                "Look into niche streaming services specialized in your favorite genres",
                "Try recommendation algorithms from multiple platforms",
                "Consider interactive entertainment experiences"
            ],
            "Balanced Consumer": [
                "Set up a media schedule to maintain your healthy balance",
                "Try content curation tools to optimize your media diet",
                "Join discussion groups about mindful media consumption"
            ],
            "Social Media Maven": [
                "Explore content creation tools specialized for your preferred platforms",
                "Consider social media management tools to optimize your experience",
                "Try digital wellbeing apps to maintain healthy boundaries"
            ]
        }
    
    def analyze_response(self, response_data):
        """
        Analyze a survey response to generate a media profile.
        
        Args:
            response_data (dict): The survey response data from Paperform.
            
        Returns:
            MediaProfile: A personalized media consumption profile.
        """
        try:
            # Extract the submission ID
            submission_id = response_data.get('id', 'unknown')
            
            # Extract the actual form data
            if 'data' in response_data:
                form_data = response_data['data']
            else:
                form_data = response_data  # The data might be at the top level
            
            logger.debug(f"Analyzing data for submission {submission_id}: {form_data}")
            
            # Calculate trait scores based on survey responses
            trait_scores = self._calculate_trait_scores(form_data)
            
            # Determine the primary profile type based on trait scores
            profile_type = self._determine_profile_type(trait_scores)
            
            # Generate trait descriptions based on scores
            trait_descriptions = self._generate_trait_descriptions(trait_scores)
            
            # Get content recommendations based on profile type
            profile_recommendations = self.recommendations.get(profile_type, [])
            
            # Create and return the media profile with raw data
            profile = MediaProfile(
                submission_id=submission_id,
                profile_type=profile_type,
                traits=trait_scores,
                descriptions=trait_descriptions,
                recommendations=profile_recommendations,
                raw_data=form_data
            )
            
            logger.info(f"Generated profile for submission {submission_id}: {profile_type}")
            return profile
            
        except Exception as e:
            logger.error(f"Error analyzing response: {str(e)}")
            raise
    
    def _calculate_trait_scores(self, form_data):
        """
        Calculate scores for each trait category based on survey responses.
        
        Args:
            form_data (dict): The form response data.
            
        Returns:
            dict: Scores for each trait category (0-100).
        """
        # Initialize scores
        trait_scores = {
            "digital_engagement": 50,
            "traditional_media_preference": 50,
            "content_creation_tendency": 50,
            "information_seeking": 50,
            "entertainment_focus": 50,
            "consumption_balance": 50,
            "social_media_engagement": 50
        }
        
        # Analyze TV watching habits
        if 'tv_hours' in form_data:
            try:
                tv_hours = float(form_data['tv_hours'])
                # More TV hours increases entertainment focus and traditional media
                trait_scores["entertainment_focus"] += min(tv_hours * 5, 30)
                trait_scores["traditional_media_preference"] += min(tv_hours * 4, 25)
            except (ValueError, TypeError):
                pass
        
        # Analyze movie watching frequency
        if 'movie_frequency' in form_data:
            movie_freq = form_data['movie_frequency']
            if movie_freq == 'daily':
                trait_scores["entertainment_focus"] += 20
                trait_scores["consumption_balance"] -= 10
            elif movie_freq == 'weekly':
                trait_scores["entertainment_focus"] += 10
                trait_scores["consumption_balance"] += 5
        
        # Analyze book reading habits
        if 'book_frequency' in form_data:
            book_freq = form_data['book_frequency']
            if book_freq == 'daily':
                trait_scores["traditional_media_preference"] += 20
                trait_scores["information_seeking"] += 15
                trait_scores["digital_engagement"] -= 10
            elif book_freq == 'weekly':
                trait_scores["traditional_media_preference"] += 10
                trait_scores["information_seeking"] += 10
        
        # Analyze news consumption
        if 'news_source' in form_data:
            news_source = form_data['news_source']
            trait_scores["information_seeking"] += 15
            if news_source == 'print':
                trait_scores["traditional_media_preference"] += 20
                trait_scores["digital_engagement"] -= 10
            elif news_source == 'online':
                trait_scores["digital_engagement"] += 15
                trait_scores["traditional_media_preference"] -= 5
            elif news_source == 'social_media':
                trait_scores["social_media_engagement"] += 20
                trait_scores["digital_engagement"] += 10
        
        # Analyze social media usage
        if 'social_media_hours' in form_data:
            try:
                sm_hours = float(form_data['social_media_hours'])
                trait_scores["social_media_engagement"] += min(sm_hours * 8, 40)
                trait_scores["digital_engagement"] += min(sm_hours * 5, 30)
                # High social media use might reduce consumption balance
                if sm_hours > 4:
                    trait_scores["consumption_balance"] -= 15
            except (ValueError, TypeError):
                pass
        
        # Analyze podcast consumption
        if 'podcast_frequency' in form_data:
            podcast_freq = form_data['podcast_frequency']
            trait_scores["digital_engagement"] += 10
            if podcast_freq == 'daily':
                trait_scores["information_seeking"] += 15 
                trait_scores["consumption_balance"] += 10
            elif podcast_freq == 'weekly':
                trait_scores["information_seeking"] += 10
                trait_scores["consumption_balance"] += 5
        
        # Analyze genre preferences
        if 'genre_preference' in form_data:
            genres = form_data['genre_preference']
            if isinstance(genres, str):
                genres = genres.split(',')
            else:
                genres = [genres]
            
            # More diverse genres indicate better consumption balance
            if len(genres) > 2:
                trait_scores["consumption_balance"] += 15
            
            for genre in genres:
                if genre.lower() in ['news', 'documentary', 'educational']:
                    trait_scores["information_seeking"] += 10
                elif genre.lower() in ['comedy', 'drama', 'action', 'romance']:
                    trait_scores["entertainment_focus"] += 10
        
        # Analyze content creation habits
        if 'content_creation' in form_data:
            creation = form_data['content_creation']
            if creation == 'frequently':
                trait_scores["content_creation_tendency"] += 30
                trait_scores["digital_engagement"] += 15
            elif creation == 'sometimes':
                trait_scores["content_creation_tendency"] += 20
                trait_scores["digital_engagement"] += 10
            elif creation == 'rarely':
                trait_scores["content_creation_tendency"] += 5
        
        # Analyze binge-watching tendencies
        if 'binge_watching' in form_data:
            binge = form_data['binge_watching']
            if binge == 'frequently':
                trait_scores["entertainment_focus"] += 20
                trait_scores["consumption_balance"] -= 15
                trait_scores["digital_engagement"] += 10
            elif binge == 'occasionally':
                trait_scores["entertainment_focus"] += 10
                trait_scores["consumption_balance"] -= 5
        
        # Ensure all scores are within 0-100 range
        for trait in trait_scores:
            trait_scores[trait] = max(0, min(100, trait_scores[trait]))
        
        return trait_scores
    
    def _determine_profile_type(self, trait_scores):
        """
        Determine the primary profile type based on trait scores.
        
        Args:
            trait_scores (dict): Scores for each trait category.
            
        Returns:
            str: The primary profile type.
        """
        # Find the highest scoring trait
        primary_trait = max(trait_scores.items(), key=lambda x: x[1])
        
        # Map trait categories to profile types
        profile_mapping = {
            "digital_engagement": "Digital Native",
            "traditional_media_preference": "Classic Consumer",
            "content_creation_tendency": "Content Creator",
            "information_seeking": "Information Seeker",
            "entertainment_focus": "Entertainment Enthusiast",
            "consumption_balance": "Balanced Consumer",
            "social_media_engagement": "Social Media Maven"
        }
        
        # Return the corresponding profile type
        return profile_mapping.get(primary_trait[0], "Balanced Consumer")
    
    def _generate_trait_descriptions(self, trait_scores):
        """
        Generate personalized descriptions for each trait based on scores.
        
        Args:
            trait_scores (dict): Scores for each trait category.
            
        Returns:
            dict: Personalized descriptions for each trait.
        """
        descriptions = {}
        
        for trait, score in trait_scores.items():
            if score < 33:
                level = "low"
            elif score < 66:
                level = "medium"
            else:
                level = "high"
            
            descriptions[trait] = self.trait_descriptions[trait][level]
        
        return descriptions
