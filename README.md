# Media Personality Profiler

A Flask-based web application that processes survey responses to generate personalized media consumption personality profiles.

## Features

- Webhook endpoint to receive survey data from Paperform
- Analysis engine that categorizes media consumption habits
- Personalized profile generation based on survey responses
- Visual representation of media traits with radar charts
- Detailed insights based on individual consumption patterns
- Social sharing capabilities

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Data Visualization**: Chart.js
- **Form Processing**: Paperform webhook integration

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/media-personality-profiler.git
cd media-personality-profiler
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

The application will be available at `http://localhost:5000`.

## Configuration

The application requires the following environment variables:
- `SESSION_SECRET`: A random string for session encryption

## Usage

### Paperform Integration

1. Create a survey on Paperform
2. Set up a webhook to send form responses to your application's `/webhook` endpoint
3. Configure the form to redirect users to your application's `/result/{submission_id}` after submission

### Demo Mode

The application includes a demo mode that generates a sample profile with simulated data. This can be accessed via the homepage.

## Project Structure

- `main.py`: Entry point for the application
- `app.py`: Flask application setup and routes
- `models.py`: Data models for storing profiles and responses
- `analyzer.py`: Analysis engine for generating profiles from survey data
- `utils.py`: Helper functions for data processing
- `templates/`: HTML templates
- `static/`: Static assets (CSS, JS, images)

## License

MIT