import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useLanguage } from '../contexts/LanguageContext';

function FileDropzone({ fileType, label, required, onUpload, currentFile, onDelete, disabled }) {
  const { t } = useLanguage();
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
    setUploading(true);
    setError(null);
    setUploadProgress(0);

    try {
      await onUpload(fileType, file, (progress) => {
        setUploadProgress(progress);
      });
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Upload failed');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  }, [fileType, onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    maxFiles: 1,
    disabled: disabled || uploading
  });

  const handleDelete = (e) => {
    e.stopPropagation();
    onDelete(fileType);
  };

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </h3>
        {currentFile && (
          <button
            onClick={handleDelete}
            className="text-red-500 hover:text-red-700 text-sm"
            disabled={disabled}
          >
            {t('remove')}
          </button>
        )}
      </div>

      {currentFile ? (
        <div className="border-2 border-green-200 bg-green-50 rounded-lg p-4">
          <div className="flex items-center">
            <span className="text-green-500 text-2xl mr-3">✓</span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {currentFile.filename}
              </p>
              <p className="text-xs text-gray-500">
                {currentFile.row_count} {t('rows')} • {currentFile.columns?.length} {t('columns')}
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
            ${isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <input {...getInputProps()} />
          
          {uploading ? (
            <div>
              <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div
                  className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <p className="text-sm text-gray-500">{t('uploading')} {uploadProgress}%</p>
            </div>
          ) : (
            <>
              <span className="text-3xl mb-2 block">📄</span>
              <p className="text-sm text-gray-600">
                {isDragActive ? 'Drop the file here' : t('dragDrop')}
              </p>
              <p className="text-xs text-gray-400 mt-1">{t('orClickBrowse')}</p>
            </>
          )}
        </div>
      )}

      {error && (
        <div className="mt-2 text-sm text-red-600 bg-red-50 rounded p-2">
          {error}
        </div>
      )}
    </div>
  );
}

export default FileDropzone;
