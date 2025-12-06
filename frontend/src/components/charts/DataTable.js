import React from 'react';

function DataTable({ data, columns }) {
  if (!data || data.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No data available
      </div>
    );
  }

  const formatValue = (value, type) => {
    if (value === null || value === undefined || value === '') return '-';
    
    switch (type) {
      case 'number':
        return typeof value === 'number' ? value.toLocaleString() : value;
      case 'currency':
        return typeof value === 'number' 
          ? `€${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
          : value;
      case 'percent':
        return typeof value === 'number' ? `${(value * 100).toFixed(1)}%` : value;
      default:
        return value;
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, rowIndex) => (
            <tr 
              key={rowIndex} 
              className={`${row.nationality === 'TOTAL' || row.property === 'TOTAL' ? 'bg-gray-100 font-semibold' : 'hover:bg-gray-50'}`}
            >
              {columns.map((col) => (
                <td
                  key={col.key}
                  className={`px-4 py-3 text-sm ${
                    col.type === 'number' || col.type === 'currency' || col.type === 'percent'
                      ? 'text-right'
                      : 'text-left'
                  } text-gray-900`}
                >
                  {formatValue(row[col.key], col.type)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;
