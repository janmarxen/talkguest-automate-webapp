import React from 'react';

function Header() {
  return (
    <header className="bg-primary-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <span className="text-2xl mr-3">🏨</span>
            <div>
              <h1 className="text-xl font-bold">TalkGuest Analytics</h1>
              <p className="text-primary-200 text-xs">Hospitality Data Processing</p>
            </div>
          </div>
          <div className="text-sm text-primary-200">
            v1.0.0
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
