import logging
import json

# Configure logging
logger = logging.getLogger(__name__)

def extract_form_data(webhook_payload):
    """
    Extract form data from Paperform webhook payload.
    
    Args:
        webhook_payload (dict): The raw webhook payload from Paperform.
        
    Returns:
        dict: Extracted form data.
    """
    try:
        # Check if the payload already contains a 'data' field
        if 'data' in webhook_payload:
            return webhook_payload['data']
        
        # If not, try to extract data from different payload structures
        # Paperform webhook structure may vary
        if 'formResponse' in webhook_payload:
            return webhook_payload['formResponse']
        
        if 'submission' in webhook_payload and 'data' in webhook_payload['submission']:
            return webhook_payload['submission']['data']
        
        # If we can't find a standard structure, return the whole payload
        logger.warning("Could not find standard data structure in webhook payload")
        return webhook_payload
    
    except Exception as e:
        logger.error(f"Error extracting form data: {str(e)}")
        return {}

def validate_required_fields(form_data, required_fields):
    """
    Validate that required fields are present in the form data.
    
    Args:
        form_data (dict): The form data to validate.
        required_fields (list): List of field names that are required.
        
    Returns:
        bool: True if all required fields are present, False otherwise.
    """
    missing_fields = [field for field in required_fields if field not in form_data]
    
    if missing_fields:
        logger.warning(f"Missing required fields: {missing_fields}")
        return False
    
    return True

def format_trait_for_display(trait_name):
    """
    Format a trait name for display (convert snake_case to Title Case).
    
    Args:
        trait_name (str): The trait name to format.
        
    Returns:
        str: Formatted trait name.
    """
    return ' '.join(word.capitalize() for word in trait_name.split('_'))

def get_trait_color(score):
    """
    Get a color code based on a trait score for visualization.
    
    Args:
        score (int): Trait score (0-100).
        
    Returns:
        str: Bootstrap color class.
    """
    if score < 33:
        return "text-info"
    elif score < 66:
        return "text-primary"
    else:
        return "text-success"

def categorize_score(score):
    """
    Categorize a score into low, medium, or high.
    
    Args:
        score (int): The score to categorize (0-100).
        
    Returns:
        str: The category ('low', 'medium', or 'high').
    """
    if score < 33:
        return "low"
    elif score < 66:
        return "medium"
    else:
        return "high"
