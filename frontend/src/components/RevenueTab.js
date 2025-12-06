import React, { useState } from 'react';
import BarChart from './charts/BarChart';
import PieChart from './charts/PieChart';
import TimeSeriesChart from './charts/TimeSeriesChart';
import DataTable from './charts/DataTable';
import { downloadRevenue } from '../utils/api';

function RevenueTab({ data }) {
  const [showInvoices, setShowInvoices] = useState(false);
  
  const reservationsSummary = data?.reservations_summary || {};
  const reservationsByProperty = data?.reservations_by_property || [];
  const invoicesSummary = data?.invoices_summary;
  const invoicesByProperty = data?.invoices_by_property || [];
  const detailedCalculations = data?.detailed_calculations || [];

  const hasInvoiceData = invoicesSummary !== null;

  // Prepare property data for charts
  const propertyChartData = reservationsByProperty.map(p => ({
    property: p.property,
    gross: p.gross_value,
    net: p.net_value,
    commission: p.commission,
    iva: p.iva_amount,
    count: p.reservation_count
  }));

  // Calculate IVA breakdown by rate
  const ivaBreakdown = detailedCalculations.reduce((acc, calc) => {
    const rate = calc.iva_rate === 0.04 ? 'Azores (4%)' : calc.iva_rate === 0.06 ? 'Mainland (6%)' : 'Other';
    if (!acc[rate]) {
      acc[rate] = { value: 0, count: 0 };
    }
    acc[rate].value += calc.iva_amount || 0;
    acc[rate].count += 1;
    return acc;
  }, {});

  const ivaChartData = Object.entries(ivaBreakdown).map(([label, stats]) => ({
    label,
    value: stats.value,
    count: stats.count
  }));

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center">
            <span className="text-3xl mr-4">💰</span>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                €{(reservationsSummary.total_gross_value || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-gray-500">Gross Revenue</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center">
            <span className="text-3xl mr-4">📉</span>
            <div>
              <p className="text-2xl font-bold text-red-600">
                €{(reservationsSummary.total_commissions || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-gray-500">Commissions</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center">
            <span className="text-3xl mr-4">🏛️</span>
            <div>
              <p className="text-2xl font-bold text-orange-600">
                €{(reservationsSummary.total_iva || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-gray-500">IVA/VAT</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow p-6">
          <div className="flex items-center">
            <span className="text-3xl mr-4">✨</span>
            <div>
              <p className="text-2xl font-bold text-green-600">
                €{(reservationsSummary.total_net_value || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-gray-500">Net Revenue</p>
            </div>
          </div>
        </div>
      </div>

      {/* Toggle for Invoice comparison */}
      {hasInvoiceData && (
        <div className="bg-blue-50 rounded-xl p-4 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-medium text-blue-800">Invoice Data Available</h3>
            <p className="text-xs text-blue-600">Compare reservation data with invoice records</p>
          </div>
          <button
            onClick={() => setShowInvoices(!showInvoices)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              showInvoices 
                ? 'bg-blue-600 text-white' 
                : 'bg-white text-blue-600 border border-blue-300'
            }`}
          >
            {showInvoices ? 'Showing Invoice Data' : 'Show Invoice Comparison'}
          </button>
        </div>
      )}

      {/* Invoice Summary (if showing) */}
      {showInvoices && invoicesSummary && (
        <div className="bg-purple-50 rounded-xl p-6 fade-in">
          <h3 className="text-lg font-semibold text-purple-800 mb-4">Invoice Summary</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <p className="text-xl font-bold text-purple-900">
                €{(invoicesSummary.total_gross_value || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-purple-600">Invoice Gross</p>
            </div>
            <div>
              <p className="text-xl font-bold text-purple-900">
                €{(invoicesSummary.total_iva || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-purple-600">Invoice IVA</p>
            </div>
            <div>
              <p className="text-xl font-bold text-purple-900">
                €{(invoicesSummary.total_net_value || 0).toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-purple-600">Invoice Net</p>
            </div>
            <div>
              <p className="text-xl font-bold text-purple-900">{invoicesSummary.total_invoices || 0}</p>
              <p className="text-sm text-purple-600">Total Invoices</p>
            </div>
          </div>
        </div>
      )}

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bar Chart - Revenue by Property */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue by Property</h3>
          <BarChart
            data={propertyChartData}
            xKey="property"
            yKey="gross"
            color="#10b981"
            height={300}
            formatValue={(v) => `€${v.toLocaleString()}`}
          />
        </div>

        {/* Pie Chart - Revenue Breakdown */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue Breakdown</h3>
          <PieChart
            data={[
              { label: 'Net Revenue', value: reservationsSummary.total_net_value || 0 },
              { label: 'Commissions', value: reservationsSummary.total_commissions || 0 },
              { label: 'IVA/VAT', value: reservationsSummary.total_iva || 0 }
            ]}
            valueKey="value"
            labelKey="label"
            height={300}
            colors={['#10b981', '#ef4444', '#f59e0b']}
          />
        </div>
      </div>

      {/* Commission vs Net by Property */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Net Revenue vs Commissions by Property</h3>
        <TimeSeriesChart
          data={propertyChartData}
          xKey="property"
          lines={[
            { key: 'net', color: '#10b981', label: 'Net Revenue' },
            { key: 'commission', color: '#ef4444', label: 'Commission' }
          ]}
          height={300}
        />
      </div>

      {/* IVA Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">IVA/VAT by Region</h3>
          <PieChart
            data={ivaChartData}
            valueKey="value"
            labelKey="label"
            height={250}
            colors={['#3b82f6', '#8b5cf6', '#06b6d4']}
          />
        </div>

        {/* Download Section */}
        <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-xl shadow p-6 flex flex-col justify-center">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Export Reports</h3>
          <p className="text-sm text-gray-600 mb-4">
            Download detailed Excel reports with full calculations and breakdowns.
          </p>
          <button
            onClick={downloadRevenue}
            className="w-full px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            📥 Download Revenue Report
          </button>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white rounded-xl shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue by Property Details</h3>
        <DataTable
          data={reservationsByProperty}
          columns={[
            { key: 'property', label: 'Property' },
            { key: 'gross_value', label: 'Gross (€)', type: 'currency' },
            { key: 'commission', label: 'Commission (€)', type: 'currency' },
            { key: 'iva_amount', label: 'IVA (€)', type: 'currency' },
            { key: 'net_value', label: 'Net (€)', type: 'currency' },
            { key: 'reservation_count', label: 'Reservations', type: 'number' }
          ]}
        />
      </div>
    </div>
  );
}

export default RevenueTab;
