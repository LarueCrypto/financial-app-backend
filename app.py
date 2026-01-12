from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Enable CORS for all routes (allows Bolt frontend to connect)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Import and register blueprints (routes)
from routes.blockchain import blockchain_bp
from routes.banking import banking_bp
from routes.trading import trading_bp
from routes.ai import ai_bp
from routes.news import news_bp

app.register_blueprint(blockchain_bp, url_prefix='/api/blockchain')
app.register_blueprint(banking_bp, url_prefix='/api/banking')
app.register_blueprint(trading_bp, url_prefix='/api/trading')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(news_bp, url_prefix='/api/news')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'Backend is running',
        'version': '1.0.0',
        'endpoints': [
            '/api/blockchain/wallet/<address>',
            '/api/banking/connect',
            '/api/banking/spending/<token>',
            '/api/trading/connect',
            '/api/trading/portfolio/<token>',
            '/api/ai/chat',
            '/api/ai/upload-document',
            '/api/ai/analyze',
            '/api/news'
        ]
    }), 200

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Unified Finance Tracker API',
        'health_check': '/api/health'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
