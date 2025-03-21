# Setup Instructions

## Local Development

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```
   export SESSION_SECRET="your-secret-key"
   ```
4. Run the application:
   ```
   python main.py
   ```

## Deployment

### Deploying to Heroku
1. Create a Heroku account and install the Heroku CLI
2. Login to Heroku:
   ```
   heroku login
   ```
3. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```
4. Set environment variables:
   ```
   heroku config:set SESSION_SECRET="your-secret-key"
   ```
5. Deploy the application:
   ```
   git push heroku main
   ```

### Deploying to PythonAnywhere or similar:
1. Upload your code to the server
2. Set up a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure the WSGI file to point to your Flask application
4. Set necessary environment variables

## Paperform Integration

1. Create your survey on Paperform
2. In Paperform settings, set up a webhook to send form data to your application's `/webhook` endpoint
3. Configure the form to redirect users to your application's `/result/{submission_id}` after submission

## Important Files

- `main.py`: Entry point for the application
- `app.py`: Flask routes and application setup
- `models.py`: Data models
- `analyzer.py`: Survey analysis logic
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and other static assets