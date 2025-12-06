"""
Process Router
==============
Handles ETL processing trigger and status.
"""

from flask import Blueprint, request, jsonify, current_app
from services.etl_service import ETLService

process_bp = Blueprint('process', __name__)


@process_bp.route('/process', methods=['POST'])
def run_processing():
    """
    Run the ETL pipeline on uploaded files.
    
    Requires: guests and reservations files to be uploaded.
    Optional: invoices file.
    
    Request body can contain optional config overrides:
    {
        "iva_rates": {"azores": 0.04, "fuzeta": 0.06},
        "property_groups": {...}
    }
    """
    storage = current_app.config['DATA_STORAGE']
    
    # Check required files
    if 'guests' not in storage:
        return jsonify({
            'success': False,
            'error': 'Guests file is required. Please upload guests data first.'
        }), 400
    
    if 'reservations' not in storage:
        return jsonify({
            'success': False,
            'error': 'Reservations file is required. Please upload reservations data first.'
        }), 400
    
    # Get optional config overrides from request
    config = None
    if request.is_json and request.json:
        config = request.json.get('config')
    
    try:
        # Initialize ETL service
        etl = ETLService(config=config)
        
        # Get dataframes from storage
        guests_df = storage['guests']['dataframe']
        reservations_df = storage['reservations']['dataframe']
        invoices_df = storage['invoices']['dataframe'] if 'invoices' in storage else None
        
        # Run pipeline
        result = etl.run_pipeline(guests_df, reservations_df, invoices_df)
        
        if result['success']:
            # Store results
            storage['results'] = {
                'occupancy': result['occupancy'],
                'revenue': result['revenue'],
                'summary': result['summary']
            }
            storage['processing_log'] = result['log']
            
            return jsonify({
                'success': True,
                'message': 'Processing completed successfully',
                'summary': result['summary'],
                'log': result['log']
            }), 200
        else:
            # Store errors
            storage['errors'] = result['errors']
            storage['processing_log'] = result['log']
            
            return jsonify({
                'success': False,
                'errors': result['errors'],
                'log': result['log']
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Processing failed: {str(e)}'
        }), 500


@process_bp.route('/process/status', methods=['GET'])
def processing_status():
    """Get the current processing status."""
    storage = current_app.config['DATA_STORAGE']
    
    has_results = 'results' in storage
    has_errors = 'errors' in storage
    
    status = 'not_started'
    if has_results:
        status = 'completed'
    elif has_errors:
        status = 'failed'
    
    response = {
        'status': status,
        'has_results': has_results,
        'log': storage.get('processing_log', [])
    }
    
    if has_results:
        response['summary'] = storage['results'].get('summary', {})
    
    if has_errors:
        response['errors'] = storage.get('errors', [])
    
    return jsonify(response), 200
