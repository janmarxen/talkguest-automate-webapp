#!/usr/bin/env python3
"""
Unit Tests for TalkGuest API Endpoints
======================================
Tests for the Flask API routers.
"""

import unittest
import json
import io
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from tests.generate_mock_data import MockDataGenerator


class TestAPIBase(unittest.TestCase):
    """Base test class for API tests."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.generator = MockDataGenerator(seed=42)
        cls.mock_data = cls.generator.generate_all_data()
    
    def setUp(self):
        """Set up for each test."""
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        
        # Clear storage before each test
        with self.app.app_context():
            self.app.config['DATA_STORAGE'].clear()
    
    def _create_excel_file(self, df):
        """Create an in-memory Excel file from DataFrame."""
        output = io.BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        return output


class TestHealthEndpoint(TestAPIBase):
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test health endpoint returns correct response."""
        response = self.client.get('/api/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'talkguest-api')


class TestUploadEndpoints(TestAPIBase):
    """Test file upload endpoints."""
    
    def test_upload_guests_file(self):
        """Test uploading guests file."""
        excel_file = self._create_excel_file(self.mock_data['guests'])
        
        response = self.client.post(
            '/api/upload/guests',
            data={'file': (excel_file, 'guests.xlsx')},
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('columns', data)
        self.assertIn('row_count', data)
    
    def test_upload_reservations_file(self):
        """Test uploading reservations file."""
        excel_file = self._create_excel_file(self.mock_data['reservations'])
        
        response = self.client.post(
            '/api/upload/reservations',
            data={'file': (excel_file, 'reservations.xlsx')},
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_upload_invalid_file_type(self):
        """Test uploading invalid file type."""
        response = self.client.post(
            '/api/upload/guests',
            data={'file': (io.BytesIO(b'test'), 'test.txt')},
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_upload_status(self):
        """Test upload status endpoint."""
        # Upload guests file
        excel_file = self._create_excel_file(self.mock_data['guests'])
        self.client.post(
            '/api/upload/guests',
            data={'file': (excel_file, 'guests.xlsx')},
            content_type='multipart/form-data'
        )
        
        response = self.client.get('/api/upload/status')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['files']['guests'])
        self.assertIsNone(data['files']['reservations'])
        self.assertFalse(data['ready_to_process'])
    
    def test_ready_to_process_when_files_uploaded(self):
        """Test ready_to_process is true when required files are uploaded."""
        # Upload guests
        guests_file = self._create_excel_file(self.mock_data['guests'])
        self.client.post(
            '/api/upload/guests',
            data={'file': (guests_file, 'guests.xlsx')},
            content_type='multipart/form-data'
        )
        
        # Upload reservations
        res_file = self._create_excel_file(self.mock_data['reservations'])
        self.client.post(
            '/api/upload/reservations',
            data={'file': (res_file, 'reservations.xlsx')},
            content_type='multipart/form-data'
        )
        
        response = self.client.get('/api/upload/status')
        data = json.loads(response.data)
        
        self.assertTrue(data['ready_to_process'])
    
    def test_delete_file(self):
        """Test deleting uploaded file."""
        # Upload file first
        excel_file = self._create_excel_file(self.mock_data['guests'])
        self.client.post(
            '/api/upload/guests',
            data={'file': (excel_file, 'guests.xlsx')},
            content_type='multipart/form-data'
        )
        
        # Delete file
        response = self.client.delete('/api/upload/guests')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Verify deleted
        status_response = self.client.get('/api/upload/status')
        status_data = json.loads(status_response.data)
        self.assertIsNone(status_data['files']['guests'])
    
    def test_clear_all(self):
        """Test clearing all uploaded files."""
        # Upload files
        guests_file = self._create_excel_file(self.mock_data['guests'])
        self.client.post(
            '/api/upload/guests',
            data={'file': (guests_file, 'guests.xlsx')},
            content_type='multipart/form-data'
        )
        
        # Clear all
        response = self.client.delete('/api/upload/clear')
        
        self.assertEqual(response.status_code, 200)
        
        # Verify cleared
        status_response = self.client.get('/api/upload/status')
        status_data = json.loads(status_response.data)
        self.assertIsNone(status_data['files']['guests'])


class TestProcessEndpoints(TestAPIBase):
    """Test processing endpoints."""
    
    def _upload_required_files(self):
        """Helper to upload required files."""
        guests_file = self._create_excel_file(self.mock_data['guests'])
        self.client.post(
            '/api/upload/guests',
            data={'file': (guests_file, 'guests.xlsx')},
            content_type='multipart/form-data'
        )
        
        res_file = self._create_excel_file(self.mock_data['reservations'])
        self.client.post(
            '/api/upload/reservations',
            data={'file': (res_file, 'reservations.xlsx')},
            content_type='multipart/form-data'
        )
    
    def test_process_without_files(self):
        """Test processing without uploaded files."""
        response = self.client.post('/api/process')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_process_with_files(self):
        """Test successful processing."""
        self._upload_required_files()
        
        response = self.client.post('/api/process')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('summary', data)
        self.assertIn('log', data)
    
    def test_process_with_invoices(self):
        """Test processing with invoice data."""
        self._upload_required_files()
        
        # Add invoices
        inv_file = self._create_excel_file(self.mock_data['invoices'])
        self.client.post(
            '/api/upload/invoices',
            data={'file': (inv_file, 'invoices.xlsx')},
            content_type='multipart/form-data'
        )
        
        response = self.client.post('/api/process')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_process_status(self):
        """Test processing status endpoint."""
        self._upload_required_files()
        
        # Before processing
        response = self.client.get('/api/process/status')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'not_started')
        
        # After processing
        self.client.post('/api/process')
        response = self.client.get('/api/process/status')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'completed')


class TestResultsEndpoints(TestAPIBase):
    """Test results endpoints."""
    
    def _upload_and_process(self):
        """Helper to upload files and process."""
        guests_file = self._create_excel_file(self.mock_data['guests'])
        self.client.post(
            '/api/upload/guests',
            data={'file': (guests_file, 'guests.xlsx')},
            content_type='multipart/form-data'
        )
        
        res_file = self._create_excel_file(self.mock_data['reservations'])
        self.client.post(
            '/api/upload/reservations',
            data={'file': (res_file, 'reservations.xlsx')},
            content_type='multipart/form-data'
        )
        
        inv_file = self._create_excel_file(self.mock_data['invoices'])
        self.client.post(
            '/api/upload/invoices',
            data={'file': (inv_file, 'invoices.xlsx')},
            content_type='multipart/form-data'
        )
        
        self.client.post('/api/process')
    
    def test_results_without_processing(self):
        """Test getting results before processing."""
        response = self.client.get('/api/results')
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_all_results(self):
        """Test getting all results."""
        self._upload_and_process()
        
        response = self.client.get('/api/results')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('occupancy', data['data'])
        self.assertIn('revenue', data['data'])
    
    def test_get_occupancy_results(self):
        """Test getting occupancy results."""
        self._upload_and_process()
        
        response = self.client.get('/api/results/occupancy')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('general_stats', data['data'])
        self.assertIn('by_property', data['data'])
    
    def test_get_revenue_results(self):
        """Test getting revenue results."""
        self._upload_and_process()
        
        response = self.client.get('/api/results/revenue')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('reservations_summary', data['data'])
        self.assertIn('reservations_by_property', data['data'])


class TestDownloadEndpoints(TestAPIBase):
    """Test download endpoints."""
    
    def _upload_and_process(self):
        """Helper to upload files and process."""
        guests_file = self._create_excel_file(self.mock_data['guests'])
        self.client.post(
            '/api/upload/guests',
            data={'file': (guests_file, 'guests.xlsx')},
            content_type='multipart/form-data'
        )
        
        res_file = self._create_excel_file(self.mock_data['reservations'])
        self.client.post(
            '/api/upload/reservations',
            data={'file': (res_file, 'reservations.xlsx')},
            content_type='multipart/form-data'
        )
        
        self.client.post('/api/process')
    
    def test_download_occupancy(self):
        """Test downloading occupancy report."""
        self._upload_and_process()
        
        response = self.client.get('/api/download/occupancy')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content_type,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    def test_download_revenue(self):
        """Test downloading revenue report."""
        self._upload_and_process()
        
        response = self.client.get('/api/download/revenue')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content_type,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    def test_download_all(self):
        """Test downloading all reports."""
        self._upload_and_process()
        
        response = self.client.get('/api/download/all')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content_type,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    def test_download_without_processing(self):
        """Test download before processing."""
        response = self.client.get('/api/download/occupancy')
        
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
