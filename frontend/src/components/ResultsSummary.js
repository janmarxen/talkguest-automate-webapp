import React from 'react';
import { downloadOccupancy, downloadRevenue, downloadAll } from '../utils/api';
import { useLanguage } from '../contexts/LanguageContext';

function ResultsSummary({ data }) {
  const { t } = useLanguage();
  const occupancy = data?.occupancy?.general_stats || {};
  const revenue = data?.revenue?.reservations_summary || {};

  return (
    <div className="bg-white rounded-xl shadow p-6 fade-in">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">
          📊 {t('resultsSummary')}
        </h2>
        <div className="flex gap-2">
          <button
            onClick={downloadOccupancy}
            className="px-4 py-2 text-sm bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
          >
            📥 {t('occupancyReport')}
          </button>
          <button
            onClick={downloadRevenue}
            className="px-4 py-2 text-sm bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
          >
            📥 {t('revenueReport')}
          </button>
          <button
            onClick={downloadAll}
            className="px-4 py-2 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            📥 {t('downloadAll')}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Occupancy Summary */}
        <div className="bg-blue-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-blue-800 mb-3">{t('occupancyOverview')}</h3>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <p className="text-2xl font-bold text-blue-900">{occupancy.total_guests || 0}</p>
              <p className="text-xs text-blue-600">{t('totalGuests')}</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-blue-900">{occupancy.total_nights || 0}</p>
              <p className="text-xs text-blue-600">{t('totalNights')}</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-blue-900">{occupancy.total_reservations || 0}</p>
              <p className="text-xs text-blue-600">{t('totalReservations')}</p>
            </div>
          </div>
        </div>

        {/* Revenue Summary */}
        <div className="bg-green-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-green-800 mb-3">{t('revenueOverview')}</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-2xl font-bold text-green-900">
                €{(revenue.total_gross_value || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-xs text-green-600">{t('grossRevenue')}</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-green-900">
                €{(revenue.total_net_value || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-xs text-green-600">{t('netRevenue')}</p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4 mt-3 pt-3 border-t border-green-200">
            <div>
              <p className="text-sm font-medium text-green-900">
                €{(revenue.total_commissions || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-xs text-green-600">{t('totalCommissions')}</p>
            </div>
            <div>
              <p className="text-sm font-medium text-green-900">
                €{(revenue.total_iva || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-xs text-green-600">{t('totalIVA')}</p>
            </div>
          </div>
        </div>
      </div>

      <p className="text-xs text-gray-500 mt-4 text-center">
        {t('navigateToTabs')}
      </p>
    </div>
  );
}

export default ResultsSummary;
