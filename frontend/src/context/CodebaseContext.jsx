import React, { createContext, useState, useContext } from 'react';

/**
 * Context for managing codebase state across components
 */
const CodebaseContext = createContext();

/**
 * Provider component for Codebase context
 */
export function CodebaseProvider({ children }) {
  const [codebase, setCodebase] = useState({
    id: null,
    status: 'idle', // idle, uploading, processing, ready, error
    error: null,
    insights: null,
    name: '',
    uploadType: null, // 'file' or 'repo'
  });

  /**
   * Start the upload process for a codebase
   * @param {string} name - Name of the codebase
   * @param {string} uploadType - Type of upload ('file' or 'repo')
   */
  const startUpload = (name, uploadType) => {
    setCodebase({
      ...codebase,
      name,
      uploadType,
      status: 'uploading',
      error: null
    });
  };

  /**
   * Handle successful upload completion
   * @param {string} id - Codebase ID from the backend
   */
  const uploadComplete = (id) => {
    setCodebase({
      ...codebase,
      id,
      status: 'processing',
    });
  };

  /**
   * Handle upload error
   * @param {string} error - Error message
   */
  const uploadError = (error) => {
    setCodebase({
      ...codebase,
      status: 'error',
      error
    });
  };

  /**
   * Update codebase insights
   * @param {Object} insights - Insights data from the backend
   */
  const setInsights = (insights) => {
    setCodebase({
      ...codebase,
      insights,
      status: 'ready'
    });
  };

  /**
   * Reset codebase state
   */
  const resetCodebase = () => {
    setCodebase({
      id: null,
      status: 'idle',
      error: null,
      insights: null,
      name: '',
      uploadType: null,
    });
  };

  return (
    <CodebaseContext.Provider
      value={{
        codebase,
        startUpload,
        uploadComplete,
        uploadError,
        setInsights,
        resetCodebase
      }}
    >
      {children}
    </CodebaseContext.Provider>
  );
}

/**
 * Hook for using codebase context
 */
export function useCodebase() {
  const context = useContext(CodebaseContext);
  if (!context) {
    throw new Error('useCodebase must be used within a CodebaseProvider');
  }
  return context;
}