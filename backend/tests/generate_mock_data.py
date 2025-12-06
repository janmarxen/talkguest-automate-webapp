#!/usr/bin/env python3
"""
Mock Data Generator for TalkGuest API Testing
==============================================
Generates realistic test data for hospitality ETL pipeline testing.
Adapted from original tests/generate_mock_data.py for backend tests.
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Faker is optional - use basic random data if not available
try:
    from faker import Faker
    fake_pt = Faker('pt_PT')
    fake_en = Faker('en_US')
    fake_fr = Faker('fr_FR')
    fake_de = Faker('de_DE')
    fake_es = Faker('es_ES')
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False

# Reservation column mappings for bilingual support
RESERVATION_COLUMNS = {
    'pt': {
        'reservation_id': 'Reserva',
        'guest': 'Hóspede',
        'property': 'Alojamento',
        'checkin': 'Checkin',
        'checkout': 'Checkout',
        'nights': 'Noites',
        'reservation_value': 'Valor Reserva',
        'channel': 'Canal',
        'channel_commission': 'Comissão Canal',
        'status': 'Status',
        'adults': 'Adultos',
        'children_no_tmt': 'Crianças não sujeitas TMT',
        'children_tmt': 'Crianças sujeitas TMT',
    },
    'en': {
        'reservation_id': 'Reservation',
        'guest': 'Guest',
        'property': 'Rental',
        'checkin': 'Checkin',
        'checkout': 'Checkout',
        'nights': 'Nights',
        'reservation_value': 'Reservation Value',
        'channel': 'Channel',
        'channel_commission': 'Channel Commission',
        'status': 'Status',
        'adults': 'Adults',
        'children_no_tmt': 'Children not subject to TMT',
        'children_tmt': 'Children subject to TMT',
    }
}


class MockDataGenerator:
    """Generate mock data for TalkGuest API testing."""
    
    def __init__(self, seed: int = 42, language: str = 'pt'):
        """
        Initialize with random seed for reproducible data.
        
        Args:
            seed: Random seed for reproducibility
            language: 'pt' for Portuguese or 'en' for English reservation columns
        """
        random.seed(seed)
        np.random.seed(seed)
        
        if FAKER_AVAILABLE:
            Faker.seed(seed)
        
        self.language = language
        self.res_cols = RESERVATION_COLUMNS[language]
        
        self.properties = [
            'Angra I', 'Angra II', 'Angra III',
            'Doze Ribeiras 0', 'Doze Ribeiras 1',
            'Casa 1', 'Casa 2', 'Casa 3', 'Casa 4', 'Casa 5',
            'Fuzeta 0', 'Fuzeta 1'
        ]
        
        self.channels = [
            'Booking.com', 'Airbnb', 'Direct', 'VRBO', 'Expedia',
            'Online Travel Agency', 'Phone Booking', 'Email'
        ]
        
        self.countries = {
            'Portugal': 0.35,
            'Spain': 0.15,
            'Germany': 0.12,
            'France': 0.10,
            'United Kingdom': 0.08,
            'Netherlands': 0.06,
            'Italy': 0.05,
            'United States': 0.04,
            'Brazil': 0.03,
            'Canada': 0.02
        }
        
        # Simple name generators
        self.first_names = ['John', 'Maria', 'Hans', 'Pierre', 'Giuseppe', 'Ana', 'Carlos', 'Sophie']
        self.last_names = ['Silva', 'Santos', 'Mueller', 'Dupont', 'Smith', 'Brown', 'Garcia']
    
    def _generate_name(self) -> str:
        """Generate a random name."""
        if FAKER_AVAILABLE:
            return random.choice([fake_pt, fake_en, fake_de, fake_fr, fake_es]).name()
        return f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
    
    def _generate_email(self, name: str) -> str:
        """Generate email from name."""
        if FAKER_AVAILABLE:
            return fake_en.email()
        clean_name = name.lower().replace(' ', '.').replace("'", "")
        return f"{clean_name}@email.com"
    
    def _generate_phone(self) -> str:
        """Generate phone number."""
        if FAKER_AVAILABLE:
            return fake_pt.phone_number()
        return f"+351 {random.randint(900000000, 999999999)}"
    
    def generate_guests_data(self, num_guests: int = 50) -> pd.DataFrame:
        """Generate guest data with realistic names and countries."""
        guests = []
        
        for _ in range(num_guests):
            country = np.random.choice(
                list(self.countries.keys()),
                p=list(self.countries.values())
            )
            
            name = self._generate_name()
            
            guest = {
                'Nome': name,
                'Pais': country,
                'Email': self._generate_email(name),
                'Telefone': self._generate_phone()
            }
            guests.append(guest)
        
        # Add test entries that should be filtered out
        test_entries = [
            {'Nome': 'Test User', 'Pais': 'Portugal', 'Email': 'test@test.com', 'Telefone': '123456789'},
            {'Nome': 'Eu Mesmo', 'Pais': 'Portugal', 'Email': 'eu@test.com', 'Telefone': '987654321'},
            {'Nome': 'John Test', 'Pais': 'United States', 'Email': 'john@test.com', 'Telefone': '555-1234'}
        ]
        guests.extend(test_entries)
        
        return pd.DataFrame(guests)
    
    def generate_reservations_data(self, guests_df: pd.DataFrame, num_reservations: int = 100) -> pd.DataFrame:
        """Generate reservation data linked to guests."""
        reservations = []
        cols = self.res_cols
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 31)
        
        for _ in range(num_reservations):
            guest_name = random.choice(guests_df['Nome'].tolist())
            
            # Generate dates
            days_offset = random.randint(0, 30)
            checkin = start_date + timedelta(days=days_offset)
            nights = random.randint(1, 7)
            checkout = checkin + timedelta(days=nights)
            
            property_name = random.choice(self.properties)
            channel = random.choice(self.channels)
            
            base_price = self._get_base_price(property_name)
            total_value = round(base_price * nights * random.uniform(0.8, 1.3), 2)
            commission = self._calculate_commission(channel, total_value)
            
            adults = random.choices([1, 2, 3, 4], weights=[0.2, 0.5, 0.2, 0.1])[0]
            children_no_tmt = random.choices([0, 1, 2], weights=[0.7, 0.2, 0.1])[0]
            children_tmt = random.choices([0, 1, 2], weights=[0.8, 0.15, 0.05])[0]
            
            reservation = {
                cols['reservation_id']: f"RES{random.randint(100000, 999999)}",
                cols['guest']: guest_name,
                cols['property']: property_name,
                cols['checkin']: checkin,
                cols['checkout']: checkout,
                cols['nights']: nights,
                cols['reservation_value']: total_value,
                cols['channel']: channel,
                cols['channel_commission']: commission,
                cols['status']: random.choices(['Confirmada', 'Check-in', 'Check-out', 'Cancelada'], weights=[0.7, 0.1, 0.15, 0.05])[0],
                cols['adults']: adults,
                cols['children_no_tmt']: children_no_tmt,
                cols['children_tmt']: children_tmt,
            }
            reservations.append(reservation)
        
        # Add zero-value reservations
        zero_value_reservations = [
            {
                cols['reservation_id']: 'RES000001',
                cols['guest']: 'Test User',
                cols['property']: 'Casa 1',
                cols['checkin']: datetime(2025, 1, 15),
                cols['checkout']: datetime(2025, 1, 17),
                cols['nights']: 2,
                cols['reservation_value']: 0,
                cols['channel']: 'Direct',
                cols['channel_commission']: 0,
                cols['status']: 'Cancelada',
                cols['adults']: 2,
                cols['children_no_tmt']: 0,
                cols['children_tmt']: 0,
            }
        ]
        reservations.extend(zero_value_reservations)
        
        # Add duplicate
        if reservations:
            reservations.append(reservations[0].copy())
        
        return pd.DataFrame(reservations)
    
    def generate_invoices_data(self, reservations_df: pd.DataFrame, num_invoices: int = 80) -> pd.DataFrame:
        """Generate invoice/billing data."""
        invoices = []
        cols = self.res_cols
        
        confirmed = reservations_df[
            reservations_df[cols['status']].isin(['Confirmada', 'Check-in', 'Check-out'])
        ]
        
        for _, reservation in confirmed.head(num_invoices).iterrows():
            invoice_type = random.choices(['Estadia', 'Limpeza', 'Taxa Turística'], weights=[0.85, 0.10, 0.05])[0]
            
            if invoice_type == 'Estadia':
                base_value = reservation[cols['reservation_value']]
            elif invoice_type == 'Limpeza':
                base_value = random.uniform(20, 80)
            else:
                base_value = int(reservation[cols['nights']]) * random.uniform(1, 3)
            
            if 'Fuzeta' in str(reservation[cols['property']]):
                iva_rate = 0.06
            else:
                iva_rate = 0.04
            
            iva_amount = base_value * iva_rate
            total_with_iva = base_value + iva_amount
            is_cancelled = random.choices([True, False], weights=[0.05, 0.95])[0]
            
            invoice = {
                'Documento': f"FT{random.randint(1000, 9999)}",
                'Alojamento': reservation[cols['property']],
                'Tipo Item': invoice_type,
                'Total Base Incidência': round(base_value, 2),
                'Total Do IVA': round(iva_amount, 2),
                'Total Documento': round(total_with_iva, 2),
                'Anulado': is_cancelled,
                'Data Documento': reservation[cols['checkin']] + timedelta(days=random.randint(0, 3))
            }
            invoices.append(invoice)
        
        return pd.DataFrame(invoices)
    
    def _get_base_price(self, property_name: str) -> float:
        """Get base price per night for a property."""
        price_mapping = {
            'Angra I': 80, 'Angra II': 85, 'Angra III': 90,
            'Doze Ribeiras 0': 70, 'Doze Ribeiras 1': 75,
            'Casa 1': 95, 'Casa 2': 100, 'Casa 3': 105, 'Casa 4': 110, 'Casa 5': 115,
            'Fuzeta 0': 120, 'Fuzeta 1': 125
        }
        return price_mapping.get(property_name, 90)
    
    def _calculate_commission(self, channel: str, total_value: float) -> float:
        """Calculate commission based on channel."""
        commission_rates = {
            'Booking.com': 0.15,
            'Airbnb': 0.12,
            'VRBO': 0.10,
            'Expedia': 0.18,
            'Online Travel Agency': 0.12,
            'Direct': 0.0,
            'Phone Booking': 0.0,
            'Email': 0.0
        }
        rate = commission_rates.get(channel, 0.10)
        return round(total_value * rate, 2)
    
    def generate_all_data(self) -> dict:
        """Generate all mock data as DataFrames."""
        guests_df = self.generate_guests_data()
        reservations_df = self.generate_reservations_data(guests_df)
        invoices_df = self.generate_invoices_data(reservations_df)
        
        return {
            'guests': guests_df,
            'reservations': reservations_df,
            'invoices': invoices_df
        }
