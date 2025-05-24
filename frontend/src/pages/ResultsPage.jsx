import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { useCodebase } from '../context/CodebaseContext';
import { useRole } from '../context/RoleContext';

// Import visualization components (to be created in a real implementation)
const VisualizationPlaceholder = ({ type, data, config }) => (
  <div className="border rounded-md p-4 bg-gray-50">
    <h3 className="font-medium text-gray-700 mb-2">
      {type} Visualization
    </h3>
    <p className="text-sm text-gray-500">
      This is a placeholder for a {type} visualization. In a real implementation, 
      this would be a proper chart or diagram based on the data.
    </p>
    <div className="mt-2 p-2 bg-gray-100 rounded text-xs overflow-auto max-h-32">
      <pre>{JSON.stringify({ data: data.substring(0, 100) + '...', config }, null, 2)}</pre>
    </div>
  </div>
);

/**
 * Results page displaying codebase insights
 */
function ResultsPage() {
  const { codebaseId } = useParams();
  const { codebase, setInsights } = useCodebase();
  const { selectedRole, getCurrentRole, changeRole } = useRole();
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const role = getCurrentRole();
  
  // Fetch insights based on codebase ID and role
  useEffect(() => {
    async function fetchInsights() {
      setLoading(true);
      setError('');
      
      try {
        const response = await axios.post(`/api/insights`, {
          codebase_id: codebaseId,
          role: selectedRole
        });
        
        setInsights(response.data);
      } catch (err) {
        console.error('Error fetching insights:', err);
        setError(err.response?.data?.detail || 'Failed to load insights');
      } finally {
        setLoading(false);
      }
    }
    
    if (codebaseId) {
      // In a real implementation, we would call fetchInsights()
      // For now, we'll use mock data after a short delay
      setTimeout(() => {
        setInsights({
          insights: {
            project_structure: {
              question: 'What is the overall structure of this project?',
              answer: 'This project has a typical structure with frontend (React), backend (FastAPI), and support modules. The main components are organized into logical directories including /frontend for the UI, /backend for API services, /rag for retrieval-augmented generation pipeline, /parsers for code analysis, and /agents for AI coordination logic.',
              task_type: 'structure'
            },
            dependencies: {
              question: 'What are the main dependencies?',
              answer: 'Key dependencies include: LangChain for RAG pipelines, FAISS for vector storage, Tree-sitter for code parsing, React with Tailwind for frontend, FastAPI for backend services, and various Python utilities.',
              task_type: 'dependencies'
            },
            tech_stack: {
              question: 'What technologies are used?',
              answer: 'The project uses Python (FastAPI, LangChain) for backend services, JavaScript/React for frontend, Tree-sitter for code parsing, and integrates with vector databases for efficient retrieval.',
              task_type: 'technology'
            }
          },
          visualizations: [
            {
              type: 'folder_tree',
              data: 'Visualization data for project structure...',
              config: { max_depth: 3 },
              task_id: 'project_structure'
            },
            {
              type: 'dependency_graph',
              data: 'Visualization data for dependencies...',
              config: { show_versions: true },
              task_id: 'dependencies'
            }
          ],
          summary: 'This is a well-structured modern application that uses a RAG (Retrieval-Augmented Generation) architecture to provide code insights. It has clear separation of concerns between frontend, backend, and AI components. The codebase is organized for extensibility and maintainability.'
        });
        setLoading(false);
      }, 1500);
    }
  }, [codebaseId, selectedRole, setInsights]);
  
  // Handle role change
  const handleRoleChange = (e) => {
    const newRole = e.target.value;
    changeRole(newRole);
  };
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Analyzing codebase with {role.name} perspective...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <h2 className="font-bold mb-2">Error</h2>
        <p>{error}</p>
      </div>
    );
  }
  
  if (!codebase.insights) {
    return (
      <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
        <h2 className="font-bold mb-2">No Data</h2>
        <p>No insights available for this codebase. Please try again or contact support.</p>
      </div>
    );
  }
  
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Codebase Insights</h1>
        
        <div className="flex items-center">
          <label htmlFor="role-select" className="mr-2 text-sm font-medium">
            View as:
          </label>
          <select
            id="role-select"
            value={selectedRole}
            onChange={handleRoleChange}
            className="form-select py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            {/* Role options would come from roleContext */}
            <option value="project_manager">Project Manager</option>
            <option value="frontend_developer">Frontend Developer</option>
            <option value="backend_developer">Backend Developer</option>
            <option value="ai_ml_engineer">AI/ML Engineer</option>
          </select>
        </div>
      </div>
      
      {/* Summary card */}
      <div className="card mb-8">
        <h2 className="text-xl font-bold mb-2">Executive Summary</h2>
        <p className="text-gray-700">{codebase.insights.summary}</p>
      </div>
      
      {/* Insights grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {Object.entries(codebase.insights.insights).map(([key, insight]) => (
          <div key={key} className="card">
            <h3 className="text-lg font-semibold mb-2">{insight.question}</h3>
            <p className="text-gray-700">{insight.answer}</p>
            
            {/* Render visualization if available */}
            {codebase.insights.visualizations.some(v => v.task_id === key) && (
              <div className="mt-4">
                {codebase.insights.visualizations
                  .filter(v => v.task_id === key)
                  .map((viz, idx) => (
                    <VisualizationPlaceholder 
                      key={idx}
                      type={viz.type}
                      data={viz.data}
                      config={viz.config}
                    />
                  ))}
              </div>
            )}
          </div>
        ))}
      </div>
      
      {/* Action buttons */}
      <div className="flex justify-end space-x-4">
        <button 
          className="btn-secondary"
          onClick={() => window.print()}
        >
          Export Insights
        </button>
        <button 
          className="btn-primary"
          onClick={() => {/* This would open a modal or new page for detailed exploration */}}
        >
          Explore In Depth
        </button>
      </div>
    </div>
  );
}

export default ResultsPage;