class MediaProfile:
    """Class to represent a user's media consumption personality profile."""
    
    def __init__(self, submission_id, profile_type, traits, descriptions, recommendations, raw_data=None):
        """
        Initialize a new MediaProfile.
        
        Args:
            submission_id (str): The ID of the submission.
            profile_type (str): The main profile type (e.g., "Digital Native").
            traits (dict): Key-value pairs of trait categories and scores.
            descriptions (dict): Descriptions of what each trait score means.
            recommendations (list): List of content recommendations based on profile.
            raw_data (dict, optional): Raw survey response data for personalized insights.
        """
        self.submission_id = submission_id
        self.profile_type = profile_type
        self.traits = traits
        self.descriptions = descriptions
        self.recommendations = recommendations
        self.raw_data = raw_data or {}
        self.personalized_insights = self._generate_personalized_insights()
    
    def get_primary_trait(self):
        """Get the highest-scoring trait category."""
        if not self.traits:
            return None
        return max(self.traits.items(), key=lambda x: x[1])
    
    def get_trait_description(self, trait):
        """Get the description for a specific trait."""
        return self.descriptions.get(trait, "No description available")
    
    def _generate_personalized_insights(self):
        """Generate personalized insights based on the raw survey data."""
        insights = []
        
        if not self.raw_data:
            return insights
            
        # Media balance insights
        tv_hours = self._safe_float(self.raw_data.get('tv_hours', 0))
        social_media_hours = self._safe_float(self.raw_data.get('social_media_hours', 0))
        book_frequency = self.raw_data.get('book_frequency', '')
        
        total_screen_time = tv_hours + social_media_hours
        if total_screen_time > 5:
            insights.append("You spend significant time on screen-based media. Consider balancing with offline activities.")
        elif total_screen_time < 2 and book_frequency in ['daily', 'weekly']:
            insights.append("You maintain a healthy balance between digital and traditional media consumption.")
        
        # Content diversity insights
        genre_preference = self.raw_data.get('genre_preference', '')
        if isinstance(genre_preference, str):
            genres = genre_preference.split(',')
            if len(genres) > 3:
                insights.append("Your diverse genre preferences indicate an open-minded approach to media consumption.")
            elif len(genres) <= 1:
                insights.append("You might benefit from exploring a wider variety of content genres.")
        
        # Active vs. passive consumption
        content_creation = self.raw_data.get('content_creation', '')
        if content_creation == 'frequently':
            insights.append("As an active content creator, you engage with media more critically than most consumers.")
        elif content_creation == 'rarely' or content_creation == '':
            insights.append("Consider more active engagement with media through discussion or content creation.")
        
        # Information vs. entertainment balance
        news_source = self.raw_data.get('news_source', '')
        binge_watching = self.raw_data.get('binge_watching', '')
        
        if news_source and binge_watching == 'frequently':
            insights.append("You balance information-seeking with entertainment, though entertainment currently dominates.")
        elif news_source and binge_watching in ['rarely', '']:
            insights.append("You prioritize informational content over pure entertainment in your media diet.")
        
        # Podcast engagement
        podcast_frequency = self.raw_data.get('podcast_frequency', '')
        if podcast_frequency == 'daily':
            insights.append("Your high podcast consumption suggests you value efficient, on-the-go media formats.")
        elif podcast_frequency == '':
            insights.append("You might enjoy exploring podcasts as a convenient way to consume content while multitasking.")
        
        # Movie watching habits
        movie_frequency = self.raw_data.get('movie_frequency', '')
        if movie_frequency == 'daily':
            insights.append("Your frequent movie watching indicates a strong appreciation for cinematic storytelling.")
        
        return insights
    
    def _safe_float(self, value, default=0.0):
        """Safely convert a value to float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def to_dict(self):
        """Convert the profile to a dictionary for storage or serialization."""
        return {
            'submission_id': self.submission_id,
            'profile_type': self.profile_type,
            'traits': self.traits,
            'descriptions': self.descriptions,
            'recommendations': self.recommendations,
            'raw_data': self.raw_data,
            'personalized_insights': self.personalized_insights
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a MediaProfile from a dictionary."""
        profile = cls(
            data['submission_id'],
            data['profile_type'],
            data['traits'],
            data['descriptions'],
            data['recommendations'],
            data.get('raw_data', {})
        )
        if 'personalized_insights' in data:
            profile.personalized_insights = data['personalized_insights']
        return profile


class ResponseStorage:
    """
    Simple in-memory storage for survey responses and generated profiles.
    In a production environment, this would be replaced with a database.
    """
    
    def __init__(self):
        """Initialize empty storage containers."""
        self.responses = {}  # submission_id -> response data
        self.profiles = {}   # submission_id -> profile
    
    def add_response(self, submission_id, response_data):
        """Store a response with its submission ID."""
        self.responses[submission_id] = response_data
    
    def get_response(self, submission_id):
        """Retrieve a response by its submission ID."""
        return self.responses.get(submission_id)
    
    def add_profile(self, submission_id, profile):
        """Store a profile with its submission ID."""
        self.profiles[submission_id] = profile
    
    def get_profile(self, submission_id):
        """Retrieve a profile by its submission ID."""
        return self.profiles.get(submission_id)
    
    def delete_response(self, submission_id):
        """Delete a response and its profile."""
        if submission_id in self.responses:
            del self.responses[submission_id]
        if submission_id in self.profiles:
            del self.profiles[submission_id]
    
    def get_all_responses(self):
        """Get all stored responses."""
        return self.responses
    
    def get_all_profiles(self):
        """Get all stored profiles."""
        return self.profiles
