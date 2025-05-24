import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useCodebase } from '../context/CodebaseContext';
import { useRole } from '../context/RoleContext';

/**
 * Upload page for submitting codebases
 */
function UploadPage() {
  const navigate = useNavigate();
  const { startUpload, uploadComplete, uploadError } = useCodebase();
  const { selectedRole, getCurrentRole } = useRole();
  
  const [uploadType, setUploadType] = useState('file');
  const [file, setFile] = useState(null);
  const [repoUrl, setRepoUrl] = useState('');
  const [branch, setBranch] = useState('main');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const role = getCurrentRole();
  
  /**
   * Handle file selection
   */
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError('');
  };
  
  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      let response;
      
      if (uploadType === 'file') {
        // Validate file upload
        if (!file) {
          setError('Please select a file to upload');
          setIsLoading(false);
          return;
        }
        
        // Create form data for file upload
        const formData = new FormData();
        formData.append('file', file);
        
        // Update context state
        startUpload(file.name, 'file');
        
        // Call API to upload file
        response = await axios.post('/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
      } else {
        // Validate repository URL
        if (!repoUrl) {
          setError('Please enter a repository URL');
          setIsLoading(false);
          return;
        }
        
        // Update context state
        startUpload(repoUrl, 'repo');
        
        // Call API to clone repository
        response = await axios.post('/api/clone', {
          repo_url: repoUrl,
          branch: branch || 'main'
        });
      }
      
      // Handle successful upload
      uploadComplete(response.data.codebase_id);
      
      // Navigate to results page
      navigate(`/results/${response.data.codebase_id}`);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.response?.data?.detail || 'An error occurred during upload');
      uploadError(err.response?.data?.detail || 'An error occurred during upload');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Upload Your Codebase</h1>
      
      <div className="card mb-6">
        <div className="flex justify-center mb-6">
          <div className="inline-flex rounded-md shadow-sm" role="group">
            <button
              type="button"
              onClick={() => setUploadType('file')}
              className={`px-4 py-2 text-sm font-medium rounded-l-lg ${
                uploadType === 'file'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Upload Zip File
            </button>
            <button
              type="button"
              onClick={() => setUploadType('repo')}
              className={`px-4 py-2 text-sm font-medium rounded-r-lg ${
                uploadType === 'repo'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Clone Repository
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          {uploadType === 'file' ? (
            <div className="mb-4">
              <label htmlFor="file" className="block text-sm font-medium text-gray-700 mb-2">
                Select ZIP file containing your codebase
              </label>
              <input
                type="file"
                id="file"
                accept=".zip,.tar.gz,.tgz"
                onChange={handleFileChange}
                className="w-full p-2 border border-gray-300 rounded-md"
              />
              <p className="mt-2 text-sm text-gray-500">
                Accepted formats: .zip, .tar.gz, .tgz
              </p>
            </div>
          ) : (
            <>
              <div className="mb-4">
                <label htmlFor="repoUrl" className="block text-sm font-medium text-gray-700 mb-2">
                  GitHub Repository URL
                </label>
                <input
                  type="text"
                  id="repoUrl"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  placeholder="https://github.com/username/repository"
                  className="w-full p-2 border border-gray-300 rounded-md"
                />
              </div>
              
              <div className="mb-4">
                <label htmlFor="branch" className="block text-sm font-medium text-gray-700 mb-2">
                  Branch (optional)
                </label>
                <input
                  type="text"
                  id="branch"
                  value={branch}
                  onChange={(e) => setBranch(e.target.value)}
                  placeholder="main"
                  className="w-full p-2 border border-gray-300 rounded-md"
                />
              </div>
            </>
          )}
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Selected Role
            </label>
            <div className="p-3 bg-gray-50 rounded-md">
              <div className="font-medium">{role.name}</div>
              <div className="text-sm text-gray-500">{role.description}</div>
            </div>
          </div>
          
          {error && (
            <div className="p-3 mb-4 text-red-700 bg-red-100 rounded-md">
              {error}
            </div>
          )}
          
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isLoading}
              className={`btn-primary ${isLoading ? 'opacity-75 cursor-not-allowed' : ''}`}
            >
              {isLoading ? 'Processing...' : 'Analyze Codebase'}
            </button>
          </div>
        </form>
      </div>
      
      <div className="card bg-blue-50">
        <h2 className="text-xl font-semibold mb-4">What happens after upload?</h2>
        <p className="text-gray-700">
          Once your codebase is uploaded, InsightAI will:
        </p>
        <ol className="list-decimal list-inside mt-2 space-y-1 text-gray-700">
          <li>Parse your code using Tree-sitter to understand its structure</li>
          <li>Index the content in a vector database for efficient retrieval</li>
          <li>Generate role-specific insights tailored to your selected role ({role.name})</li>
          <li>Create visualizations to help you understand the codebase better</li>
        </ol>
        <p className="mt-4 text-gray-700">
          This process may take a few minutes depending on the size of your codebase.
        </p>
      </div>
    </div>
  );
}

export default UploadPage;