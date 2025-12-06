"""
Results Router
==============
Provides access to processed data results.
"""

from flask import Blueprint, jsonify, current_app

results_bp = Blueprint('results', __name__)


@results_bp.route('/results', methods=['GET'])
def get_all_results():
    """Get all processing results."""
    storage = current_app.config['DATA_STORAGE']
    
    if 'results' not in storage:
        return jsonify({
            'success': False,
            'error': 'No results available. Please run processing first.'
        }), 404
    
    return jsonify({
        'success': True,
        'data': storage['results']
    }), 200


@results_bp.route('/results/occupancy', methods=['GET'])
def get_occupancy_results():
    """Get occupancy report results."""
    storage = current_app.config['DATA_STORAGE']
    
    if 'results' not in storage:
        return jsonify({
            'success': False,
            'error': 'No results available. Please run processing first.'
        }), 404
    
    occupancy = storage['results'].get('occupancy')
    if not occupancy:
        return jsonify({
            'success': False,
            'error': 'Occupancy data not available'
        }), 404
    
    return jsonify({
        'success': True,
        'data': occupancy
    }), 200


@results_bp.route('/results/revenue', methods=['GET'])
def get_revenue_results():
    """Get revenue report results."""
    storage = current_app.config['DATA_STORAGE']
    
    if 'results' not in storage:
        return jsonify({
            'success': False,
            'error': 'No results available. Please run processing first.'
        }), 404
    
    revenue = storage['results'].get('revenue')
    if not revenue:
        return jsonify({
            'success': False,
            'error': 'Revenue data not available'
        }), 404
    
    return jsonify({
        'success': True,
        'data': revenue
    }), 200


@results_bp.route('/results/summary', methods=['GET'])
def get_summary():
    """Get processing summary."""
    storage = current_app.config['DATA_STORAGE']
    
    if 'results' not in storage:
        return jsonify({
            'success': False,
            'error': 'No results available. Please run processing first.'
        }), 404
    
    summary = storage['results'].get('summary')
    
    return jsonify({
        'success': True,
        'data': summary
    }), 200
