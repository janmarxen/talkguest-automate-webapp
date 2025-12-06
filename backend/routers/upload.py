"""
Upload Router
=============
Handles file uploads for guests, reservations, and invoices data.
"""

from flask import Blueprint, request, jsonify, current_app
import pandas as pd
import io

upload_bp = Blueprint('upload', __name__)


ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/upload/<file_type>', methods=['POST'])
def upload_file(file_type):
    """
    Upload an Excel file for processing.
    
    Args:
        file_type: One of 'guests', 'reservations', or 'invoices'
    
    Returns:
        JSON with upload status and file info
    """
    valid_types = ['guests', 'reservations', 'invoices']
    
    if file_type not in valid_types:
        return jsonify({
            'success': False,
            'error': f'Invalid file type. Must be one of: {", ".join(valid_types)}'
        }), 400
    
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file provided'
        }), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Invalid file type. Only Excel files (.xlsx, .xls) are allowed'
        }), 400
    
    try:
        # Read file into memory
        file_content = file.read()
        
        # Try to parse as Excel to validate
        df = pd.read_excel(io.BytesIO(file_content))
        
        # Store in app storage
        storage = current_app.config['DATA_STORAGE']
        storage[file_type] = {
            'filename': file.filename,
            'data': file_content,
            'dataframe': df,
            'columns': df.columns.tolist(),
            'row_count': len(df)
        }
        
        # Clear any previous processing results when new file is uploaded
        if 'results' in storage:
            del storage['results']
        if 'errors' in storage:
            del storage['errors']
        
        return jsonify({
            'success': True,
            'message': f'{file_type.capitalize()} file uploaded successfully',
            'filename': file.filename,
            'columns': df.columns.tolist(),
            'row_count': len(df),
            'preview': df.head(5).to_dict(orient='records')
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to process file: {str(e)}'
        }), 400


@upload_bp.route('/upload/status', methods=['GET'])
def upload_status():
    """Get status of uploaded files."""
    storage = current_app.config['DATA_STORAGE']
    
    status = {
        'guests': None,
        'reservations': None,
        'invoices': None
    }
    
    for file_type in status.keys():
        if file_type in storage:
            status[file_type] = {
                'filename': storage[file_type]['filename'],
                'columns': storage[file_type]['columns'],
                'row_count': storage[file_type]['row_count']
            }
    
    # Check if ready to process (guests and reservations are required)
    ready_to_process = 'guests' in storage and 'reservations' in storage
    
    return jsonify({
        'success': True,
        'files': status,
        'ready_to_process': ready_to_process
    }), 200


@upload_bp.route('/upload/<file_type>', methods=['DELETE'])
def delete_file(file_type):
    """Delete an uploaded file."""
    valid_types = ['guests', 'reservations', 'invoices']
    
    if file_type not in valid_types:
        return jsonify({
            'success': False,
            'error': f'Invalid file type. Must be one of: {", ".join(valid_types)}'
        }), 400
    
    storage = current_app.config['DATA_STORAGE']
    
    if file_type in storage:
        del storage[file_type]
        
        # Clear results when a file is deleted
        if 'results' in storage:
            del storage['results']
        if 'errors' in storage:
            del storage['errors']
        
        return jsonify({
            'success': True,
            'message': f'{file_type.capitalize()} file deleted'
        }), 200
    
    return jsonify({
        'success': False,
        'error': f'No {file_type} file uploaded'
    }), 404


@upload_bp.route('/upload/clear', methods=['DELETE'])
def clear_all():
    """Clear all uploaded files and results."""
    storage = current_app.config['DATA_STORAGE']
    storage.clear()
    
    return jsonify({
        'success': True,
        'message': 'All data cleared'
    }), 200
