import React from 'react';
import FileDropzone from './FileDropzone';
import ProcessingSection from './ProcessingSection';
import ErrorDisplay from './ErrorDisplay';
import ResultsSummary from './ResultsSummary';
import { uploadFile, deleteFile, clearAllFiles, runProcessing } from '../utils/api';
import { useLanguage } from '../contexts/LanguageContext';

function UploadTab({
  uploadStatus,
  processingStatus,
  error,
  loading,
  setLoading,
  onUploadComplete,
  onFileDelete,
  onClearAll,
  onProcessingComplete,
  onProcessingError,
  results
}) {
  const { t } = useLanguage();
  
  const handleUpload = async (fileType, file, onProgress) => {
    console.log(`[UploadTab] Starting upload for ${fileType}:`, file.name);
    
    try {
      const result = await uploadFile(fileType, file, onProgress);
      console.log(`[UploadTab] Raw result:`, result);
      console.log(`[UploadTab] Type of result:`, typeof result);
      
      // Robust parsing - handle string, object, or nested scenarios
      let data = result;
      
      // If it's a string, try to parse it (possibly multiple times if double-stringified)
      while (typeof data === 'string') {
        try {
          data = JSON.parse(data);
          console.log(`[UploadTab] Parsed to:`, data);
        } catch (e) {
          console.error(`[UploadTab] Cannot parse string:`, data.substring(0, 100));
          break; // Stop if we can't parse
        }
      }
      
      // Now check for success
      if (data && typeof data === 'object' && (data.success || data.filename)) {
        console.log(`[UploadTab] Success! Calling onUploadComplete`);
        onUploadComplete(fileType, {
          filename: data.filename,
          columns: data.columns || [],
          row_count: data.row_count || 0
        });
        console.log(`[UploadTab] onUploadComplete called`);
      } else if (data && typeof data === 'object' && data.error) {
        console.error(`[UploadTab] Server returned error:`, data.error);
        throw new Error(data.error);
      } else {
        console.error(`[UploadTab] Unexpected response format:`, data);
        throw new Error('Unexpected response format from server');
      }
    } catch (err) {
      console.error(`[UploadTab] Upload exception:`, err);
      throw err;
    }
  };

  const handleDelete = async (fileType) => {
    try {
      await deleteFile(fileType);
      onFileDelete(fileType);
    } catch (err) {
      console.error('Failed to delete file:', err);
    }
  };

  const handleClearAll = async () => {
    try {
      await clearAllFiles();
      onClearAll();
    } catch (err) {
      console.error('Failed to clear files:', err);
    }
  };

  const handleProcess = async () => {
    setLoading(true);
    try {
      const result = await runProcessing();
      if (result.success) {
        // Fetch full results
        const { getAllResults } = await import('../utils/api');
        const fullResults = await getAllResults();
        if (fullResults.success) {
          onProcessingComplete(fullResults.data);
        }
      } else {
        onProcessingError(result.errors || ['Processing failed']);
      }
    } catch (err) {
      onProcessingError([err.response?.data?.error || err.message || 'Processing failed']);
    } finally {
      setLoading(false);
    }
  };

  const hasAnyFiles = uploadStatus.guests || uploadStatus.reservations || uploadStatus.invoices;
  const canProcess = uploadStatus.guests && uploadStatus.reservations;

  return (
    <div className="space-y-6">
      {/* Error Display */}
      {error && (
        <ErrorDisplay errors={Array.isArray(error) ? error : [error]} />
      )}

      {/* File Upload Section */}
      <div className="bg-gray-50 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            📁 {t('uploadTitle')}
          </h2>
          {hasAnyFiles && (
            <button
              onClick={handleClearAll}
              className="text-sm text-red-600 hover:text-red-800"
              disabled={loading}
            >
              {t('clearAll')}
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <FileDropzone
            fileType="guests"
            label={t('guestsList')}
            required={true}
            onUpload={handleUpload}
            currentFile={uploadStatus.guests}
            onDelete={handleDelete}
            disabled={loading}
          />
          <FileDropzone
            fileType="reservations"
            label={t('reservations')}
            required={true}
            onUpload={handleUpload}
            currentFile={uploadStatus.reservations}
            onDelete={handleDelete}
            disabled={loading}
          />
          <FileDropzone
            fileType="invoices"
            label={t('invoicesOptional')}
            required={false}
            onUpload={handleUpload}
            currentFile={uploadStatus.invoices}
            onDelete={handleDelete}
            disabled={loading}
          />
        </div>

        <p className="text-xs text-gray-500 mt-4">
          {t('requiredFiles')}
        </p>
      </div>

      {/* Processing Section */}
      <ProcessingSection
        canProcess={canProcess}
        loading={loading}
        processingStatus={processingStatus}
        onProcess={handleProcess}
      />

      {/* Results Summary */}
      {results && (
        <ResultsSummary data={results} />
      )}
    </div>
  );
}

export default UploadTab;
