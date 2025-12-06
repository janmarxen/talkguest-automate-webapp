import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

function TabNavigation({ tabs, activeTab, onTabChange }) {
  const { t } = useLanguage();

  return (
    <div className="border-b border-gray-200">
      <nav className="-mb-px flex space-x-8">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => !tab.disabled && onTabChange(tab.id)}
            disabled={tab.disabled}
            className={`
              flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors
              ${activeTab === tab.id
                ? 'border-primary-500 text-primary-600'
                : tab.disabled
                  ? 'border-transparent text-gray-300 cursor-not-allowed'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 cursor-pointer'
              }
            `}
          >
            <span className="mr-2">{tab.icon}</span>
            {tab.label}
            {tab.disabled && (
              <span className="ml-2 text-xs text-gray-400">({t('processDataFirst')})</span>
            )}
          </button>
        ))}
      </nav>
    </div>
  );
}

export default TabNavigation;
