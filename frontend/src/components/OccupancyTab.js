import React, { useState } from 'react';
import BarChart from './charts/BarChart';
import PieChart from './charts/PieChart';
import PropertySelector from './charts/PropertySelector';
import DataTable from './charts/DataTable';
import { useLanguage } from '../contexts/LanguageContext';

function OccupancyTab({ data }) {
  const { t } = useLanguage();
  const [selectedProperty, setSelectedProperty] = useState(null);
  const generalStats = data?.general_stats || {};
  const propertyData = data?.by_property || {};
  const properties = Object.keys(propertyData);

  // Aggregate data for charts
  const propertyTotals = properties.map(prop => {
    const propData = propertyData[prop] || [];
    const totalRow = propData.find(row => row.nationality === 'TOTAL');
    return {
      property: prop,
      nights: totalRow?.total_nights || 0,
      guests: totalRow?.unique_guests || 0,
      personNights: totalRow?.person_nights || 0
    };
  }).filter(p => p.nights > 0);

  // Get nationality breakdown for selected property or all
  const getNationalityData = () => {
    if (selectedProperty) {
      const propData = propertyData[selectedProperty] || [];
      return propData.filter(row => row.nationality && row.nationality !== 'TOTAL' && row.nationality !== '');
    }
    
    // Aggregate across all properties
    const nationalityMap = {};
    properties.forEach(prop => {
      const propData = propertyData[prop] || [];
      propData.forEach(row => {
        if (row.nationality && row.nationality !== 'TOTAL' && row.nationality !== '') {
          if (!nationalityMap[row.nationality]) {
            nationalityMap[row.nationality] = { total_nights: 0, unique_guests: 0, person_nights: 0 };
          }
          nationalityMap[row.nationality].total_nights += row.total_nights || 0;
          nationalityMap[row.nationality].unique_guests += row.unique_guests || 0;
          nationalityMap[row.nationality].person_nights += row.person_nights || 0;
        }
      });
    });
    
    return Object.entries(nationalityMap).map(([nationality, stats]) => ({
      nationality,
      total_nights: stats.total_nights,
      unique_guests: stats.unique_guests,
      person_nights: stats.person_nights
    })).sort((a, b) => b.total_nights - a.total_nights);
  };

  const nationalityData = getNationalityData();

  return (
    <div className="space-y-6">
      {/* General Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center">
            <span className="text-3xl mr-4">👥</span>
            <div>
              <p className="text-3xl font-bold text-gray-900">{generalStats.total_guests || 0}</p>
              <p className="text-sm text-gray-500">{t('uniqueGuests')}</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center">
            <span className="text-3xl mr-4">🌙</span>
            <div>
              <p className="text-3xl font-bold text-gray-900">{generalStats.total_nights || 0}</p>
              <p className="text-sm text-gray-500">{t('totalNights')}</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center">
            <span className="text-3xl mr-4">📋</span>
            <div>
              <p className="text-3xl font-bold text-gray-900">{generalStats.total_reservations || 0}</p>
              <p className="text-sm text-gray-500">{t('totalReservations')}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Property Selector */}
      <PropertySelector
        properties={properties}
        selected={selectedProperty}
        onSelect={setSelectedProperty}
        label={t('selectProperty')}
      />

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bar Chart - Nights by Property */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">{t('nightsOverTime')}</h3>
          <BarChart
            data={propertyTotals}
            xKey="property"
            yKey="nights"
            color="#3b82f6"
            height={300}
          />
        </div>

        {/* Pie Chart - Nationality Distribution */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {t('guestDistribution')}
            {selectedProperty && <span className="text-sm font-normal text-gray-500 ml-2">({selectedProperty})</span>}
          </h3>
          <PieChart
            data={nationalityData.slice(0, 10)}
            valueKey="total_nights"
            labelKey="nationality"
            height={300}
          />
        </div>
      </div>

      {/* Bar Chart - Person Nights by Property */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{t('personNights')} by Property</h3>
        <BarChart
          data={propertyTotals}
          xKey="property"
          yKey="personNights"
          color="#10b981"
          height={300}
        />
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          {t('detailedData')}
          {selectedProperty && <span className="text-sm font-normal text-gray-500 ml-2">({selectedProperty})</span>}
        </h3>
        <DataTable
          data={nationalityData}
          columns={[
            { key: 'nationality', label: t('nationality') },
            { key: 'unique_guests', label: t('uniqueGuests'), type: 'number' },
            { key: 'total_nights', label: t('totalNights'), type: 'number' },
            { key: 'person_nights', label: t('personNights'), type: 'number' }
          ]}
        />
      </div>
    </div>
  );
}

export default OccupancyTab;
