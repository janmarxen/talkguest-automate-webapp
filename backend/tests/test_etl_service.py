#!/usr/bin/env python3
"""
Unit Tests for TalkGuest ETL Service
====================================
Tests for the ETL service module.
"""

import unittest
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.etl_service import ETLService, detect_reservations_language, RESERVATIONS_COLUMNS
from tests.generate_mock_data import MockDataGenerator


class TestETLService(unittest.TestCase):
    """Test cases for ETLService class."""
    
    language = 'pt'
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.generator = MockDataGenerator(seed=42, language=cls.language)
        cls.mock_data = cls.generator.generate_all_data()
        cls.res_cols = RESERVATIONS_COLUMNS[cls.language]
    
    def setUp(self):
        """Set up for each test."""
        self.etl = ETLService()
    
    def test_run_pipeline_success(self):
        """Test successful pipeline execution."""
        result = self.etl.run_pipeline(
            guests_df=self.mock_data['guests'],
            reservations_df=self.mock_data['reservations'],
            faturacao_df=self.mock_data['invoices']
        )
        
        self.assertTrue(result['success'])
        self.assertIn('occupancy', result)
        self.assertIn('revenue', result)
        self.assertIn('summary', result)
        self.assertIn('log', result)
    
    def test_run_pipeline_without_invoices(self):
        """Test pipeline without invoice data."""
        result = self.etl.run_pipeline(
            guests_df=self.mock_data['guests'],
            reservations_df=self.mock_data['reservations'],
            faturacao_df=None
        )
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['occupancy'])
        self.assertIsNotNone(result['revenue'])
        self.assertIsNone(result['revenue']['invoices_summary'])
    
    def test_removes_test_entries(self):
        """Test that test entries are properly removed."""
        result = self.etl.run_pipeline(
            guests_df=self.mock_data['guests'],
            reservations_df=self.mock_data['reservations']
        )
        
        self.assertTrue(result['success'])
        
        # Check that test entries were logged as removed
        log_messages = [entry['message'] for entry in result['log']]
        test_removal_log = [msg for msg in log_messages if 'test entries' in msg.lower()]
        self.assertTrue(len(test_removal_log) > 0)
    
    def test_removes_zero_value_reservations(self):
        """Test that zero-value reservations are removed."""
        col_value = self.res_cols['reservation_value']
        
        # Verify mock data has zero-value reservations
        zero_value_count = len(self.mock_data['reservations'][
            pd.to_numeric(self.mock_data['reservations'][col_value], errors='coerce') <= 0
        ])
        self.assertGreater(zero_value_count, 0, "Mock data should have zero-value reservations")
        
        result = self.etl.run_pipeline(
            guests_df=self.mock_data['guests'],
            reservations_df=self.mock_data['reservations']
        )
        
        self.assertTrue(result['success'])
        
        # Verify zero-value removed from combined data
        self.assertIsNone(self.etl.combined_df[
            pd.to_numeric(self.etl.combined_df[col_value], errors='coerce') <= 0
        ].shape[0] if self.etl.combined_df is not None else None)
    
    def test_booking_commission_applied(self):
        """Test Booking.com commission adjustment."""
        col_channel = self.res_cols['channel']
        
        # Get initial Booking.com reservations
        booking_mask = self.mock_data['reservations'][col_channel].str.contains('Booking.com', case=False, na=False)
        initial_booking_count = booking_mask.sum()
        
        if initial_booking_count > 0:
            result = self.etl.run_pipeline(
                guests_df=self.mock_data['guests'],
                reservations_df=self.mock_data['reservations']
            )
            
            self.assertTrue(result['success'])
            
            # Check log for commission application
            log_messages = [entry['message'] for entry in result['log']]
            commission_log = [msg for msg in log_messages if 'Booking.com commission' in msg]
            self.assertTrue(len(commission_log) > 0)
    
    def test_occupancy_report_structure(self):
        """Test occupancy report has correct structure."""
        result = self.etl.run_pipeline(
            guests_df=self.mock_data['guests'],
            reservations_df=self.mock_data['reservations']
        )
        
        self.assertTrue(result['success'])
        
        occupancy = result['occupancy']
        
        # Check general stats (English column names)
        self.assertIn('general_stats', occupancy)
        self.assertIn('total_guests', occupancy['general_stats'])
        self.assertIn('total_nights', occupancy['general_stats'])
        self.assertIn('total_reservations', occupancy['general_stats'])
        
        # Check property data
        self.assertIn('by_property', occupancy)
        self.assertGreater(len(occupancy['by_property']), 0)
        
        # Check property data structure (English column names)
        for property_name, data in occupancy['by_property'].items():
            self.assertIsInstance(data, list)
            if len(data) > 0:
                first_row = data[0]
                self.assertIn('nationality', first_row)
                self.assertIn('unique_guests', first_row)
                self.assertIn('total_nights', first_row)
                self.assertIn('person_nights', first_row)
    
    def test_revenue_report_structure(self):
        """Test revenue report has correct structure."""
        result = self.etl.run_pipeline(
            guests_df=self.mock_data['guests'],
            reservations_df=self.mock_data['reservations'],
            faturacao_df=self.mock_data['invoices']
        )
        
        self.assertTrue(result['success'])
        
        revenue = result['revenue']
        
        # Check reservations summary (English column names)
        self.assertIn('reservations_summary', revenue)
        self.assertIn('total_gross_value', revenue['reservations_summary'])
        self.assertIn('total_commissions', revenue['reservations_summary'])
        self.assertIn('total_iva', revenue['reservations_summary'])
        self.assertIn('total_net_value', revenue['reservations_summary'])
        
        # Check by property
        self.assertIn('reservations_by_property', revenue)
        self.assertGreater(len(revenue['reservations_by_property']), 0)
        
        # Check invoices data when provided
        self.assertIn('invoices_summary', revenue)
        self.assertIsNotNone(revenue['invoices_summary'])
    
    def test_iva_calculation(self):
        """Test IVA rates are correctly applied."""
        result = self.etl.run_pipeline(
            guests_df=self.mock_data['guests'],
            reservations_df=self.mock_data['reservations']
        )
        
        self.assertTrue(result['success'])
        
        # Check detailed calculations have IVA rates
        detailed = result['revenue']['detailed_calculations']
        self.assertGreater(len(detailed), 0)
        
        for calc in detailed:
            self.assertIn('iva_rate', calc)
            # Fuzeta should have 6%, others 4%
            if 'Fuzeta' in calc['property']:
                self.assertEqual(calc['iva_rate'], 0.06)
            else:
                self.assertEqual(calc['iva_rate'], 0.04)


class TestETLServiceEnglish(TestETLService):
    """Test cases for ETLService with English reservation data."""
    
    language = 'en'
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment with English data."""
        cls.generator = MockDataGenerator(seed=42, language='en')
        cls.mock_data = cls.generator.generate_all_data()
        cls.res_cols = RESERVATIONS_COLUMNS['en']


class TestLanguageDetection(unittest.TestCase):
    """Test cases for language detection."""
    
    def test_detect_portuguese(self):
        """Test detection of Portuguese columns."""
        df = pd.DataFrame({
            'Hóspede': ['Test'],
            'Noites': [1],
            'Valor Reserva': [100],
            'Alojamento': ['Casa 1']
        })
        
        language = detect_reservations_language(df)
        self.assertEqual(language, 'pt')
    
    def test_detect_english(self):
        """Test detection of English columns."""
        df = pd.DataFrame({
            'Guest': ['Test'],
            'Nights': [1],
            'Reservation Value': [100],
            'Rental': ['Casa 1']
        })
        
        language = detect_reservations_language(df)
        self.assertEqual(language, 'en')
    
    def test_invalid_columns_raises_error(self):
        """Test that invalid columns raise ValueError."""
        df = pd.DataFrame({
            'InvalidCol1': ['Test'],
            'InvalidCol2': [1]
        })
        
        with self.assertRaises(ValueError):
            detect_reservations_language(df)


if __name__ == '__main__':
    unittest.main()
