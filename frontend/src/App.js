import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import TabNavigation from './components/TabNavigation';
import UploadTab from './components/UploadTab';
import OccupancyTab from './components/OccupancyTab';
import RevenueTab from './components/RevenueTab';
import { getUploadStatus, getProcessingStatus, getAllResults } from './utils/api';
import { useLanguage } from './contexts/LanguageContext';

function App() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState('upload');
  const [uploadStatus, setUploadStatus] = useState({
    guests: null,
    reservations: null,
    invoices: null,
    ready_to_process: false
  });
  const [processingStatus, setProcessingStatus] = useState('not_started');
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch current status on mount
  const fetchStatus = useCallback(async () => {
    try {
      const [uploadRes, processRes] = await Promise.all([
        getUploadStatus().catch(() => ({ files: {}, ready_to_process: false })),
        getProcessingStatus().catch(() => ({ status: 'not_started' }))
      ]);
      
      setUploadStatus({
        guests: uploadRes.files?.guests,
        reservations: uploadRes.files?.reservations,
        invoices: uploadRes.files?.invoices,
        ready_to_process: uploadRes.ready_to_process
      });
      setProcessingStatus(processRes.status);

      // Fetch results if processing is completed
      if (processRes.status === 'completed') {
        const resultsRes = await getAllResults();
        if (resultsRes.success) {
          setResults(resultsRes.data);
        }
      }
    } catch (err) {
      console.error('Failed to fetch status:', err);
    }
  }, []);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  const handleUploadComplete = (fileType, fileInfo) => {
    setUploadStatus(prev => ({
      ...prev,
      [fileType]: fileInfo,
      ready_to_process: fileType === 'guests' || fileType === 'reservations' 
        ? (fileType === 'guests' ? (!!prev.reservations && !!fileInfo) : (!!prev.guests && !!fileInfo))
        : prev.ready_to_process
    }));
    setProcessingStatus('not_started');
    setResults(null);
    setError(null);
  };

  const handleFileDelete = (fileType) => {
    setUploadStatus(prev => ({
      ...prev,
      [fileType]: null,
      ready_to_process: fileType === 'guests' || fileType === 'reservations' ? false : prev.ready_to_process
    }));
    setProcessingStatus('not_started');
    setResults(null);
  };

  const handleClearAll = () => {
    setUploadStatus({
      guests: null,
      reservations: null,
      invoices: null,
      ready_to_process: false
    });
    setProcessingStatus('not_started');
    setResults(null);
    setError(null);
  };

  const handleProcessingComplete = (newResults) => {
    setProcessingStatus('completed');
    setResults(newResults);
    setError(null);
  };

  const handleProcessingError = (err) => {
    setProcessingStatus('failed');
    setError(err);
  };

  const tabs = [
    { id: 'upload', label: t('tabUpload'), icon: '📁' },
    { id: 'occupancy', label: t('tabOccupancy'), icon: '📊', disabled: !results },
    { id: 'revenue', label: t('tabRevenue'), icon: '💰', disabled: !results }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <TabNavigation 
          tabs={tabs} 
          activeTab={activeTab} 
          onTabChange={setActiveTab} 
        />
        
        <div className="mt-6 tab-content">
          {activeTab === 'upload' && (
            <UploadTab
              uploadStatus={uploadStatus}
              processingStatus={processingStatus}
              error={error}
              loading={loading}
              setLoading={setLoading}
              onUploadComplete={handleUploadComplete}
              onFileDelete={handleFileDelete}
              onClearAll={handleClearAll}
              onProcessingComplete={handleProcessingComplete}
              onProcessingError={handleProcessingError}
              results={results}
            />
          )}
          
          {activeTab === 'occupancy' && results && (
            <OccupancyTab data={results.occupancy} />
          )}
          
          {activeTab === 'revenue' && results && (
            <RevenueTab data={results.revenue} />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
