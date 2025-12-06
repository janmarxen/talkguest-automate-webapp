"""
Health Check Router
===================
Provides health check endpoint for Docker and load balancers.
"""

from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'talkguest-api',
        'version': '1.0.0'
    }), 200
