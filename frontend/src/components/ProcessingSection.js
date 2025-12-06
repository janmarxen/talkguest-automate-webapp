import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

function ProcessingSection({ canProcess, loading, processingStatus, onProcess }) {
  const { t } = useLanguage();

  return (
    <div className="bg-white rounded-xl shadow p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        ⚙️ {t('processData')}
      </h2>

      <div className="flex items-center justify-between">
        <div>
          {!canProcess && (
            <p className="text-sm text-gray-500">
              {t('uploadRequired')}
            </p>
          )}
          {canProcess && processingStatus === 'not_started' && (
            <p className="text-sm text-gray-600">
              {t('readyToProcess')}
            </p>
          )}
          {processingStatus === 'completed' && (
            <div className="flex items-center text-green-600">
              <span className="mr-2">✓</span>
              <span className="text-sm font-medium">{t('processingCompleted')}</span>
            </div>
          )}
          {processingStatus === 'failed' && (
            <div className="flex items-center text-red-600">
              <span className="mr-2">✗</span>
              <span className="text-sm font-medium">{t('processingFailed')}</span>
            </div>
          )}
        </div>

        <button
          onClick={onProcess}
          disabled={!canProcess || loading}
          className={`
            px-6 py-3 rounded-lg font-medium transition-all
            ${canProcess && !loading
              ? 'bg-primary-600 text-white hover:bg-primary-700 shadow-md hover:shadow-lg'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }
          `}
        >
          {loading ? (
            <div className="flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {t('processing')}
            </div>
          ) : (
            `${t('processData')}`
          )}
        </button>
      </div>
    </div>
  );
}

export default ProcessingSection;
