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

# Column markers for file type detection
GUESTS_MARKERS = {'Nome', 'Pais'}  # Portuguese guests file columns
RESERVATIONS_MARKERS_PT = {'Reserva', 'Hóspede', 'Noites', 'Alojamento', 'Valor Reserva'}
RESERVATIONS_MARKERS_EN = {'Reservation', 'Guest', 'Nights', 'Rental', 'Reservation Value'}


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def detect_file_type(df):
    """
    Detect the actual file type based on column headers.
    
    Returns:
        tuple: (detected_type, confidence) where type is 'guests', 'reservations', or 'unknown'
    """
    columns = set(df.columns)
    
    guests_matches = len(columns & GUESTS_MARKERS)
    reservations_pt_matches = len(columns & RESERVATIONS_MARKERS_PT)
    reservations_en_matches = len(columns & RESERVATIONS_MARKERS_EN)
    reservations_matches = max(reservations_pt_matches, reservations_en_matches)
    
    # Guests file typically has Nome and Pais
    if guests_matches >= 2 and reservations_matches < 3:
        return 'guests', guests_matches
    
    # Reservations file has many specific columns
    if reservations_matches >= 3:
        return 'reservations', reservations_matches
    
    return 'unknown', 0


def validate_file_type(df, expected_type):
    """
    Validate that the uploaded file matches the expected type.
    
    Returns:
        tuple: (is_valid, error_message, error_code)
    """
    detected_type, confidence = detect_file_type(df)
    
    if detected_type == 'unknown':
        # Can't determine, allow it
        return True, None, None
    
    if detected_type != expected_type:
        # File appears to be swapped
        if expected_type == 'guests' and detected_type == 'reservations':
            return False, 'FILE_SWAP_GUESTS_HAS_RESERVATIONS', 'file_swap'
        elif expected_type == 'reservations' and detected_type == 'guests':
            return False, 'FILE_SWAP_RESERVATIONS_HAS_GUESTS', 'file_swap'
    
    return True, None, None


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
        
        # Validate file type matches expected type (guests vs reservations)
        if file_type in ['guests', 'reservations']:
            is_valid, error_code, error_type = validate_file_type(df, file_type)
            if not is_valid:
                return jsonify({
                    'success': False,
                    'error': error_code,
                    'error_type': error_type
                }), 400
        
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
        
        # Convert preview to JSON-safe format (replace NaN with None)
        preview_df = df.head(5).fillna('')  # Replace NaN with empty string for preview
        
        return jsonify({
            'success': True,
            'message': f'{file_type.capitalize()} file uploaded successfully',
            'filename': file.filename,
            'columns': df.columns.tolist(),
            'row_count': len(df),
            'preview': preview_df.to_dict(orient='records')
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
