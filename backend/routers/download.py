"""
Download Router
===============
Provides endpoints for downloading processed data as Excel files.
"""

from flask import Blueprint, jsonify, current_app, send_file
import pandas as pd
import io

download_bp = Blueprint('download', __name__)


@download_bp.route('/download/occupancy', methods=['GET'])
def download_occupancy():
    """Download occupancy report as Excel file."""
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
    
    try:
        # Create Excel file in memory
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # General statistics sheet
            general_stats = pd.DataFrame([occupancy['general_stats']])
            general_stats.columns = ['Total Guests', 'Total Nights', 'Total Reservations']
            general_stats.to_excel(writer, sheet_name='General Statistics', index=False)
            
            # Property sheets
            for property_name, data in occupancy.get('by_property', {}).items():
                df = pd.DataFrame(data)
                # Rename columns to user-friendly English names
                df.columns = ['Nationality', 'Unique Guests', 'Total People', 'Total Nights', 'Person-Nights']
                
                # Sanitize sheet name
                sheet_name = property_name.replace('(', '').replace(')', '').replace(',', '')[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='occupancy_report.xlsx'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate Excel file: {str(e)}'
        }), 500


@download_bp.route('/download/revenue', methods=['GET'])
def download_revenue():
    """Download revenue report as Excel file."""
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
    
    try:
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Reservations summary
            res_summary = pd.DataFrame([revenue['reservations_summary']])
            res_summary.columns = ['Total Gross Value', 'Total Commissions', 'Total IVA', 'Total Net Value', 'Total Reservations']
            res_summary.to_excel(writer, sheet_name='Reservations Summary', index=False)
            
            # Reservations by property
            res_by_prop = pd.DataFrame(revenue['reservations_by_property'])
            res_by_prop.columns = ['Property', 'Gross Value', 'Commission', 'IVA Amount', 'Net Value', 'Reservation Count']
            res_by_prop.to_excel(writer, sheet_name='By Property (Reservations)', index=False)
            
            # Invoices data if available
            if revenue.get('invoices_summary'):
                inv_summary = pd.DataFrame([revenue['invoices_summary']])
                inv_summary.columns = ['Total Gross Value', 'Total IVA', 'Total Net Value', 'Total Invoices']
                inv_summary.to_excel(writer, sheet_name='Invoices Summary', index=False)
            
            if revenue.get('invoices_by_property'):
                inv_by_prop = pd.DataFrame(revenue['invoices_by_property'])
                inv_by_prop.columns = ['Property', 'Gross Value', 'Net Value', 'IVA Amount', 'Invoice Count']
                inv_by_prop.to_excel(writer, sheet_name='By Property (Invoices)', index=False)
            
            # Detailed calculations
            if revenue.get('detailed_calculations'):
                detailed = pd.DataFrame(revenue['detailed_calculations'])
                detailed.columns = ['Property', 'Gross Value', 'Commission', 'IVA Rate', 'IVA Amount', 'Net Value']
                detailed.to_excel(writer, sheet_name='Detailed Calculations', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='revenue_report.xlsx'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate Excel file: {str(e)}'
        }), 500


@download_bp.route('/download/all', methods=['GET'])
def download_all():
    """Download all reports as a single Excel file with multiple sheets."""
    storage = current_app.config['DATA_STORAGE']
    
    if 'results' not in storage:
        return jsonify({
            'success': False,
            'error': 'No results available. Please run processing first.'
        }), 404
    
    occupancy = storage['results'].get('occupancy')
    revenue = storage['results'].get('revenue')
    
    if not occupancy or not revenue:
        return jsonify({
            'success': False,
            'error': 'Complete results not available'
        }), 404
    
    try:
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Occupancy general stats
            general_stats = pd.DataFrame([occupancy['general_stats']])
            general_stats.columns = ['Total Guests', 'Total Nights', 'Total Reservations']
            general_stats.to_excel(writer, sheet_name='Occupancy Summary', index=False)
            
            # Revenue summary
            res_summary = pd.DataFrame([revenue['reservations_summary']])
            res_summary.columns = ['Total Gross Value', 'Total Commissions', 'Total IVA', 'Total Net Value', 'Total Reservations']
            res_summary.to_excel(writer, sheet_name='Revenue Summary', index=False)
            
            # Revenue by property
            res_by_prop = pd.DataFrame(revenue['reservations_by_property'])
            res_by_prop.columns = ['Property', 'Gross Value', 'Commission', 'IVA Amount', 'Net Value', 'Reservation Count']
            res_by_prop.to_excel(writer, sheet_name='Revenue by Property', index=False)
            
            # Occupancy by property (limited sheets)
            for i, (property_name, data) in enumerate(occupancy.get('by_property', {}).items()):
                if i >= 10:  # Limit to 10 property sheets
                    break
                df = pd.DataFrame(data)
                df.columns = ['Nationality', 'Unique Guests', 'Total People', 'Total Nights', 'Person-Nights']
                sheet_name = f"Occ {property_name}"[:31].replace('(', '').replace(')', '').replace(',', '')
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='talkguest_report.xlsx'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate Excel file: {str(e)}'
        }), 500
