import React from 'react';

function ErrorDisplay({ errors }) {
  if (!errors || errors.length === 0) return null;

  return (
    <div className="bg-red-50 border border-red-200 rounded-xl p-4 fade-in">
      <div className="flex items-start">
        <span className="text-red-500 text-xl mr-3">⚠️</span>
        <div>
          <h3 className="text-red-800 font-medium">Processing Error</h3>
          <ul className="mt-2 text-sm text-red-700 list-disc list-inside">
            {errors.map((error, index) => (
              <li key={index}>{error}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ErrorDisplay;
