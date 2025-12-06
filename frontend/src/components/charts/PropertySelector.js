import React from 'react';

function PropertySelector({ properties, selected, onSelect, label }) {
  return (
    <div className="bg-white rounded-xl shadow p-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => onSelect(null)}
            className={`px-3 py-1 rounded-full text-sm transition-colors ${
              selected === null
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All Properties
          </button>
          {properties.map((prop) => (
            <button
              key={prop}
              onClick={() => onSelect(prop)}
              className={`px-3 py-1 rounded-full text-sm transition-colors ${
                selected === prop
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {prop.length > 20 ? prop.substring(0, 17) + '...' : prop}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default PropertySelector;
