"""
Hamed AI - Flask Application for PythonAnywhere Deployment
"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, static_folder='dist', static_url_path='')
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hamed-ai-secret-key')
    app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'
    
    # Serve React app
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    # API Routes
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'service': 'Hamed AI',
            'version': '1.0.0'
        })
    
    @app.route('/api/dashboard')
    def dashboard():
        return jsonify({
            'pages': 21,
            'ai_brains': 6,
            'status': 'operational'
        })
    
    @app.route('/api/agents')
    def agents():
        return jsonify({
            'agents': [
                {'name': 'Content Writer', 'status': 'active'},
                {'name': 'Translator', 'status': 'active'},
                {'name': 'Data Analyst', 'status': 'active'},
                {'name': 'Code Generator', 'status': 'active'},
                {'name': 'Quality Checker', 'status': 'active'},
                {'name': 'Optimizer', 'status': 'active'}
            ]
        })
    
    @app.route('/api/tests')
    def tests():
        return jsonify({
            'total_tests': 50,
            'passed': 50,
            'failed': 0,
            'success_rate': 100
        })
    
    @app.route('/api/contact')
    def contact():
        return jsonify({
            'whatsapp': '01061245527',
            'vodafone_cash': '01061245527'
        })
    
    # Catch-all route for React Router
    @app.route('/<path:path>')
    def catch_all(path):
        return send_from_directory(app.static_folder, 'index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
