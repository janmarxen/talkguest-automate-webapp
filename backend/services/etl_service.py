"""
ETL Service
===========
Core data processing service for hospitality data analysis.
Extracted from talkguest_etl.py and adapted for API use.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple


# =============================================================================
# COLUMN MAPPINGS FOR BILINGUAL SUPPORT
# =============================================================================

RESERVATIONS_COLUMNS = {
    'pt': {
        'reservation_id': 'Reserva',
        'status': 'Estado',
        'guest': 'Hóspede',
        'booked_at': 'Reservado em',
        'checkin': 'Checkin',
        'checkout': 'Checkout',
        'nights': 'Noites',
        'idiom': 'Idioma',
        'property': 'Alojamento',
        'bed': 'Cama',
        'expected_checkin_time': 'Hora Prevista Checkin',
        'expected_checkout_time': 'Hora Prevista Checkout',
        'adults': 'Adultos',
        'children_no_tmt': 'Crianças não sujeitas TMT',
        'children_tmt': 'Crianças sujeitas TMT',
        'channel': 'Canal',
        'channel_commission': 'Comissão Canal',
        'reservation_value': 'Valor Reserva',
        'cleaning_fee': 'Taxa de Limpeza',
        'canceled_at': 'Cancelado em',
    },
    'en': {
        'reservation_id': 'Reservation',
        'status': 'Status',
        'guest': 'Guest',
        'booked_at': 'Booked at',
        'checkin': 'Checkin',
        'checkout': 'Checkout',
        'nights': 'Nights',
        'idiom': 'Idiom',
        'property': 'Rental',
        'bed': 'Bed',
        'expected_checkin_time': 'Expected Checkin Time',
        'expected_checkout_time': 'Expected Checkout Time',
        'adults': 'Adults',
        'children_no_tmt': 'Children not subject to TMT',
        'children_tmt': 'Children subject to TMT',
        'channel': 'Channel',
        'channel_commission': 'Channel Commission',
        'reservation_value': 'Reservation Value',
        'cleaning_fee': 'Cleaning Fee',
        'canceled_at': 'Canceled At',
    }
}

GUESTS_COLUMNS = {
    'name': 'Nome',
    'country': 'Pais',
}

FATURACAO_COLUMNS = {
    'item_type': 'Tipo Item',
    'total_document': 'Total Documento',
    'base_amount': 'Total Base Incidência',
    'vat_amount': 'Total Do IVA',
    'cancelled': 'Anulado',
    'document_id': 'Documento',
    'property': 'Alojamento',
    'stay_value': 'Estadia',
}

# Default configuration
DEFAULT_CONFIG = {
    'iva_rates': {
        'azores': 0.04,
        'fuzeta': 0.06
    },
    'property_groups': {
        'angra_combined': ['Angra I', 'Angra II', 'Angra III'],
        'doze_ribeiras_combined': ['Doze Ribeiras 0', 'Doze Ribeiras 1'],
        'casas_separate': ['Casa 1', 'Casa 2', 'Casa 3', 'Casa 4', 'Casa 5'],
        'fuzeta_combined': ['Fuzeta 0', 'Fuzeta 1']
    }
}


def detect_reservations_language(df: pd.DataFrame) -> str:
    """
    Detect language of reservations DataFrame based on column headers.
    
    Args:
        df: pandas DataFrame with reservation data
        
    Returns:
        str: 'pt' or 'en'
        
    Raises:
        ValueError: If columns don't match either language schema
    """
    columns = set(df.columns)
    
    pt_markers = {'Hóspede', 'Noites', 'Valor Reserva', 'Alojamento'}
    en_markers = {'Guest', 'Nights', 'Reservation Value', 'Rental'}
    
    pt_matches = len(columns & pt_markers)
    en_matches = len(columns & en_markers)
    
    if pt_matches >= 3:
        return 'pt'
    elif en_matches >= 3:
        return 'en'
    else:
        raise ValueError(
            f"Unable to detect reservation file language. "
            f"Expected Portuguese columns {pt_markers} or English columns {en_markers}. "
            f"Found columns: {sorted(columns)}"
        )


class ColumnMapper:
    """Helper class to access column names based on detected language."""
    
    def __init__(self, language: str = 'pt'):
        self.language = language
        self._reservations = RESERVATIONS_COLUMNS[language]
        self._guests = GUESTS_COLUMNS
        self._faturacao = FATURACAO_COLUMNS
    
    def res(self, key: str) -> str:
        """Get reservation column name."""
        return self._reservations[key]
    
    def guest(self, key: str) -> str:
        """Get guest column name."""
        return self._guests[key]
    
    def fat(self, key: str) -> str:
        """Get faturacao column name."""
        return self._faturacao[key]


class ETLService:
    """ETL service for processing hospitality data."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize ETL service with configuration."""
        self.config = config or DEFAULT_CONFIG
        self.cols: Optional[ColumnMapper] = None
        self.guests_df: Optional[pd.DataFrame] = None
        self.reservations_df: Optional[pd.DataFrame] = None
        self.faturacao_df: Optional[pd.DataFrame] = None
        self.combined_df: Optional[pd.DataFrame] = None
        self.occupancy_data: Optional[Dict] = None
        self.revenue_data: Optional[Dict] = None
        self.processing_log: list = []
        self.errors: list = []
    
    def log(self, message: str, level: str = 'info'):
        """Add log message."""
        self.processing_log.append({'level': level, 'message': message})
        if level == 'error':
            self.errors.append(message)
    
    def run_pipeline(
        self,
        guests_df: pd.DataFrame,
        reservations_df: pd.DataFrame,
        faturacao_df: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Run the complete ETL pipeline.
        
        Args:
            guests_df: Guest data DataFrame
            reservations_df: Reservations data DataFrame
            faturacao_df: Optional invoices data DataFrame
            
        Returns:
            Dictionary with processing results
        """
        self.processing_log = []
        self.errors = []
        
        try:
            # Store input data
            self.guests_df = guests_df.copy()
            self.reservations_df = reservations_df.copy()
            self.faturacao_df = faturacao_df.copy() if faturacao_df is not None else None
            
            # Detect language and setup column mapper
            language = detect_reservations_language(self.reservations_df)
            self.cols = ColumnMapper(language)
            self.log(f"Detected reservation file language: {language.upper()}")
            
            # Process data
            self._process_data()
            
            # Generate reports
            self._generate_occupancy_report()
            self._generate_revenue_report()
            
            self.log("Pipeline completed successfully")
            
            return {
                'success': True,
                'occupancy': self.occupancy_data,
                'revenue': self.revenue_data,
                'log': self.processing_log,
                'summary': self._get_summary()
            }
            
        except Exception as e:
            self.log(f"Pipeline error: {str(e)}", level='error')
            return {
                'success': False,
                'errors': self.errors,
                'log': self.processing_log
            }
    
    def _process_data(self):
        """Clean and combine the data."""
        col_guest = self.cols.res('guest')
        col_channel = self.cols.res('channel')
        col_value = self.cols.res('reservation_value')
        col_commission = self.cols.res('channel_commission')
        col_property = self.cols.res('property')
        col_checkin = self.cols.res('checkin')
        col_checkout = self.cols.res('checkout')
        col_nights = self.cols.res('nights')
        col_adults = self.cols.res('adults')
        col_children_no_tmt = self.cols.res('children_no_tmt')
        col_children_tmt = self.cols.res('children_tmt')
        col_guest_name = self.cols.guest('name')
        
        # Clean up guest names
        self.guests_df[col_guest_name] = self.guests_df[col_guest_name].astype(str).str.strip()
        self.reservations_df[col_guest] = self.reservations_df[col_guest].astype(str).str.strip()
        
        # Apply Booking.com commission adjustment
        booking_mask = self.reservations_df[col_channel].str.contains('Booking.com', case=False, na=False)
        booking_count = booking_mask.sum()
        
        if booking_count > 0:
            valor_bruto = pd.to_numeric(self.reservations_df[col_value], errors='coerce').fillna(0)
            existing_commission = pd.to_numeric(self.reservations_df[col_commission], errors='coerce').fillna(0)
            additional_commission = valor_bruto * 0.014
            
            self.reservations_df.loc[booking_mask, col_commission] = (
                existing_commission[booking_mask] + additional_commission[booking_mask]
            ).round(2)
            
            total_additional = additional_commission[booking_mask].sum()
            self.log(f"Applied Booking.com commission: {booking_count} reservations, +€{total_additional:.2f}")
        
        # Remove test entries
        guests_before = len(self.guests_df)
        test_words = ['Eu', 'Test']
        pattern = r'\b(' + '|'.join(test_words) + r')\b'
        mask = self.guests_df[col_guest_name].str.contains(pattern, case=False, na=False, regex=True)
        self.guests_df = self.guests_df[~mask]
        guests_after = len(self.guests_df)
        self.log(f"Removed {guests_before - guests_after} test entries from guests")
        
        # Remove test and zero-value reservations
        reservations_before = len(self.reservations_df)
        reservation_mask = self.reservations_df[col_guest].str.contains(pattern, case=False, na=False, regex=True)
        self.reservations_df = self.reservations_df[
            (~reservation_mask) & 
            (pd.to_numeric(self.reservations_df[col_value], errors='coerce') > 0)
        ]
        reservations_after = len(self.reservations_df)
        self.log(f"Removed {reservations_before - reservations_after} invalid reservations")
        
        # Combine data
        self.combined_df = pd.merge(
            self.reservations_df,
            self.guests_df,
            left_on=col_guest,
            right_on=col_guest_name,
            how='left',
            suffixes=('_reservation', '_guest')
        )
        
        # Calculate total people
        self.combined_df['total_people'] = (
            pd.to_numeric(self.combined_df[col_adults], errors='coerce').fillna(0) +
            pd.to_numeric(self.combined_df[col_children_no_tmt], errors='coerce').fillna(0) +
            pd.to_numeric(self.combined_df[col_children_tmt], errors='coerce').fillna(0)
        ).astype(int)
        
        # Remove duplicates
        before_dedup = len(self.combined_df)
        duplicate_check_columns = [col_guest, col_checkin, col_checkout, col_property]
        self.combined_df = self.combined_df.drop_duplicates(subset=duplicate_check_columns, keep='first')
        after_dedup = len(self.combined_df)
        
        if before_dedup - after_dedup > 0:
            self.log(f"Removed {before_dedup - after_dedup} duplicates")
        
        # Process faturacao if available
        if self.faturacao_df is not None:
            col_item_type = self.cols.fat('item_type')
            stay_value = self.cols.fat('stay_value')
            self.faturacao_clean = self.faturacao_df[self.faturacao_df[col_item_type] == stay_value].copy()
            self.log(f"Filtered invoices to {len(self.faturacao_clean)} stay records")
        else:
            self.faturacao_clean = None
            self.log("No invoice data provided - using reservation values only")
        
        # If there are no records after cleaning, set combined_df to None
        if len(self.combined_df) == 0:
            self.log("No records found after cleaning - final dataset is empty")
            self.combined_df = None
        else:
            self.log(f"Final dataset: {len(self.combined_df)} unique records")
    
    def _group_property(self, property_name: str) -> str:
        """Group property according to business rules."""
        if pd.isna(property_name):
            return 'Unknown'
        
        property_name = str(property_name).strip()
        property_groups = self.config['property_groups']
        
        if property_name in property_groups.get('angra_combined', []):
            return 'Angra (I, II, III combined)'
        elif property_name in property_groups.get('doze_ribeiras_combined', []):
            return 'Doze Ribeiras (0, 1 combined)'
        elif property_name in property_groups.get('casas_separate', []):
            return property_name
        elif property_name in property_groups.get('fuzeta_combined', []):
            return 'Fuzeta (0, 1 combined)'
        else:
            return property_name
    
    def _generate_occupancy_report(self):
        """Generate occupancy report with English column names."""
        col_property = self.cols.res('property')
        col_guest = self.cols.res('guest')
        col_nights = self.cols.res('nights')
        col_country = self.cols.guest('country')
        
        # Apply property groupings
        self.combined_df['property_group'] = self.combined_df[col_property].apply(self._group_property)
        
        # Overall statistics (English column names)
        total_stats = {
            'total_guests': int(self.combined_df[col_guest].nunique()),
            'total_nights': int(self.combined_df[col_nights].sum()),
            'total_reservations': len(self.combined_df)
        }
        
        # Property breakdown with nationality
        property_tabs = {}
        unique_properties = self.combined_df['property_group'].unique()
        
        for property_name in sorted(unique_properties):
            if property_name == 'Unknown':
                continue
            
            property_data = self.combined_df[self.combined_df['property_group'] == property_name].copy()
            property_data['person_nights'] = property_data['total_people'] * property_data[col_nights]
            
            nationality_stats = property_data.groupby(col_country).agg({
                col_guest: 'nunique',
                'total_people': 'sum',
                col_nights: 'sum',
                'person_nights': 'sum'
            }).reset_index()
            
            # English column names
            nationality_stats.columns = ['nationality', 'unique_guests', 'total_people', 'total_nights', 'person_nights']
            nationality_stats = nationality_stats.sort_values('total_nights', ascending=False).reset_index(drop=True)
            
            # Add totals row
            totals = {
                'nationality': 'TOTAL',
                'unique_guests': int(property_data[col_guest].nunique()),
                'total_people': int(property_data['total_people'].sum()),
                'total_nights': int(property_data[col_nights].sum()),
                'person_nights': int(property_data['person_nights'].sum())
            }
            
            nationality_stats = pd.concat([
                nationality_stats,
                pd.DataFrame([{'nationality': '', 'unique_guests': '', 'total_people': '', 'total_nights': '', 'person_nights': ''}]),
                pd.DataFrame([totals])
            ], ignore_index=True)
            
            property_tabs[property_name] = nationality_stats.to_dict(orient='records')
        
        self.occupancy_data = {
            'general_stats': total_stats,
            'by_property': property_tabs
        }
        
        self.log("Occupancy report generated")
    
    def _generate_revenue_report(self):
        """Generate revenue report with English column names."""
        col_property = self.cols.res('property')
        col_value = self.cols.res('reservation_value')
        col_commission = self.cols.res('channel_commission')
        col_reservation_id = self.cols.res('reservation_id')
        
        revenue_df = self.combined_df.copy()
        revenue_df['individual_property'] = revenue_df[col_property].apply(lambda x: str(x).strip() if pd.notna(x) else 'Unknown')
        
        # IVA rate based on location
        def get_iva_rate(property_name):
            if pd.isna(property_name):
                return 0
            prop_lower = str(property_name).lower()
            if 'fuzeta' in prop_lower:
                return self.config['iva_rates'].get('fuzeta', 0.06)
            else:
                return self.config['iva_rates'].get('azores', 0.04)
        
        revenue_df['iva_rate'] = revenue_df[col_property].apply(get_iva_rate)
        revenue_df['gross_value'] = pd.to_numeric(revenue_df[col_value], errors='coerce').fillna(0)
        revenue_df['commission'] = pd.to_numeric(revenue_df[col_commission], errors='coerce').fillna(0)
        revenue_df['iva_amount'] = revenue_df['gross_value'] * revenue_df['iva_rate']
        revenue_df['net_value'] = revenue_df['gross_value'] - revenue_df['commission'] - revenue_df['iva_amount']
        
        # Group by property
        by_property = revenue_df.groupby('individual_property').agg({
            'gross_value': 'sum',
            'commission': 'sum',
            'iva_amount': 'sum',
            'net_value': 'sum',
            col_reservation_id: 'count'
        }).reset_index()
        
        by_property.columns = ['property', 'gross_value', 'commission', 'iva_amount', 'net_value', 'reservation_count']
        
        for col in ['gross_value', 'commission', 'iva_amount', 'net_value']:
            by_property[col] = by_property[col].round(2)
        
        # Overall summary
        reservations_summary = {
            'total_gross_value': round(revenue_df['gross_value'].sum(), 2),
            'total_commissions': round(revenue_df['commission'].sum(), 2),
            'total_iva': round(revenue_df['iva_amount'].sum(), 2),
            'total_net_value': round(revenue_df['net_value'].sum(), 2),
            'total_reservations': len(revenue_df)
        }
        
        # Faturacao data if available
        invoices_summary = None
        invoices_by_property = None
        
        if self.faturacao_clean is not None:
            col_fat_property = self.cols.fat('property')
            col_total_doc = self.cols.fat('total_document')
            col_base_amount = self.cols.fat('base_amount')
            col_vat_amount = self.cols.fat('vat_amount')
            col_cancelled = self.cols.fat('cancelled')
            col_document_id = self.cols.fat('document_id')
            
            faturacao_df = self.faturacao_clean.copy()
            
            faturacao_df['total_document_clean'] = pd.to_numeric(faturacao_df[col_total_doc], errors='coerce').fillna(0)
            faturacao_df['base_amount_clean'] = pd.to_numeric(faturacao_df[col_base_amount], errors='coerce').fillna(0)
            faturacao_df['vat_amount_clean'] = pd.to_numeric(faturacao_df[col_vat_amount], errors='coerce').fillna(0)
            
            faturacao_df['cancelled_bool'] = faturacao_df[col_cancelled].fillna(False)
            faturacao_df['multiplier'] = faturacao_df['cancelled_bool'].apply(lambda x: -1 if x else 1)
            
            faturacao_df['total_final'] = faturacao_df['total_document_clean'] * faturacao_df['multiplier']
            faturacao_df['base_final'] = faturacao_df['base_amount_clean'] * faturacao_df['multiplier']
            faturacao_df['vat_final'] = faturacao_df['vat_amount_clean'] * faturacao_df['multiplier']
            
            inv_by_prop = faturacao_df.groupby(col_fat_property).agg({
                'total_final': 'sum',
                'base_final': 'sum',
                'vat_final': 'sum',
                col_document_id: 'count'
            }).reset_index()
            
            inv_by_prop.columns = ['property', 'gross_value', 'net_value', 'iva_amount', 'invoice_count']
            
            for col in ['gross_value', 'net_value', 'iva_amount']:
                inv_by_prop[col] = inv_by_prop[col].round(2)
            
            invoices_by_property = inv_by_prop.to_dict(orient='records')
            
            invoices_summary = {
                'total_gross_value': round(faturacao_df['total_final'].sum(), 2),
                'total_iva': round(faturacao_df['vat_final'].sum(), 2),
                'total_net_value': round(faturacao_df['base_final'].sum(), 2),
                'total_invoices': len(faturacao_df)
            }
        
        # Detailed calculations for export
        detailed = revenue_df[['individual_property', 'gross_value', 'commission', 'iva_rate', 'iva_amount', 'net_value']].copy()
        detailed.columns = ['property', 'gross_value', 'commission', 'iva_rate', 'iva_amount', 'net_value']
        
        self.revenue_data = {
            'reservations_summary': reservations_summary,
            'reservations_by_property': by_property.to_dict(orient='records'),
            'invoices_summary': invoices_summary,
            'invoices_by_property': invoices_by_property,
            'detailed_calculations': detailed.to_dict(orient='records')
        }
        
        self.log("Revenue report generated")
    
    def _get_summary(self) -> Dict:
        """Get processing summary."""
        return {
            'guests_processed': len(self.guests_df) if self.guests_df is not None else 0,
            'reservations_processed': len(self.combined_df) if self.combined_df is not None else 0,
            'invoices_processed': len(self.faturacao_clean) if self.faturacao_clean is not None else 0,
            'properties_found': len(self.combined_df['property_group'].unique()) if self.combined_df is not None else 0
        }
