# Hamed AI - PythonAnywhere WSGI Configuration
# This file is used by PythonAnywhere to run the Flask application

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/hamed-ai'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from freelance_automation import create_app

# Create the application
application = create_app()

# Enable debug mode in development
if os.environ.get('FLASK_ENV') == 'development':
    application.debug = True
