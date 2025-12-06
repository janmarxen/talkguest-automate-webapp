import React from 'react';
import FileDropzone from './FileDropzone';
import ProcessingSection from './ProcessingSection';
import ErrorDisplay from './ErrorDisplay';
import ResultsSummary from './ResultsSummary';
import { uploadFile, deleteFile, clearAllFiles, runProcessing } from '../utils/api';

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
  const handleUpload = async (fileType, file, onProgress) => {
    const result = await uploadFile(fileType, file, onProgress);
    if (result.success) {
      onUploadComplete(fileType, {
        filename: result.filename,
        columns: result.columns,
        row_count: result.row_count
      });
    }
    return result;
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
            📁 Upload Data Files
          </h2>
          {hasAnyFiles && (
            <button
              onClick={handleClearAll}
              className="text-sm text-red-600 hover:text-red-800"
              disabled={loading}
            >
              Clear All
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <FileDropzone
            fileType="guests"
            label="Guests List"
            required={true}
            onUpload={handleUpload}
            currentFile={uploadStatus.guests}
            onDelete={handleDelete}
            disabled={loading}
          />
          <FileDropzone
            fileType="reservations"
            label="Reservations"
            required={true}
            onUpload={handleUpload}
            currentFile={uploadStatus.reservations}
            onDelete={handleDelete}
            disabled={loading}
          />
          <FileDropzone
            fileType="invoices"
            label="Invoices (Optional)"
            required={false}
            onUpload={handleUpload}
            currentFile={uploadStatus.invoices}
            onDelete={handleDelete}
            disabled={loading}
          />
        </div>

        <p className="text-xs text-gray-500 mt-4">
          * Required files. Accepts Excel files (.xlsx, .xls)
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
