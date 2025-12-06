import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import logo from '../img/luzzme_logo.avif';

function Header() {
  const { language, toggleLanguage, t } = useLanguage();

  return (
    <header className="bg-primary-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <img 
              src={logo} 
              alt="Luzzme Logo" 
              className="h-10 w-auto mr-3 rounded-lg bg-white p-1"
            />
            <div>
              <h1 className="text-xl font-bold">{t('appTitle')}</h1>
              <p className="text-primary-200 text-xs">{t('appSubtitle')}</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-2 px-3 py-1.5 bg-primary-700 hover:bg-primary-600 rounded-lg text-sm transition-colors"
              title={t('language')}
            >
              <span className="text-lg">{language === 'en' ? '🇬🇧' : '🇵🇹'}</span>
              <span>{language === 'en' ? 'EN' : 'PT'}</span>
            </button>
            <div className="text-sm text-primary-200">
              v1.0.0
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
