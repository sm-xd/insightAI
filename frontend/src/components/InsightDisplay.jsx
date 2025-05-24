import React from 'react';
import PropTypes from 'prop-types';
import { Visualization } from './visualizations';
import { useRole } from '../context/RoleContext';

/**
 * InsightDisplay component shows insights based on the selected role
 */
function InsightDisplay({ insights, visualizations, summary }) {
  const { selectedRole, roles } = useRole();
  
  const currentRole = roles.find(r => r.id === selectedRole) || {
    name: 'Default Role',
    description: 'No role selected'
  };
  
  if (!insights) {
    return (
      <div className="p-6 bg-gray-100 rounded-md">
        <p>No insights available. Select a role and analyze a codebase first.</p>
      </div>
    );
  }
  
  // Group the insights by their task_type
  const groupedInsights = Object.entries(insights).reduce((acc, [key, insight]) => {
    const type = insight.task_type || 'other';
    if (!acc[type]) {
      acc[type] = [];
    }
    acc[type].push({ id: key, ...insight });
    return acc;
  }, {});
  
  // Find visualizations for insights
  const getVisualizationsForInsight = (insightId) => {
    return visualizations.filter(viz => viz.task_id === insightId);
  };
  
  return (
    <div className="insight-display">
      <div className="mb-6">
        <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full">
          <span className="mr-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zm-4 7a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </span>
          <span className="font-medium">{currentRole.name} View</span>
        </div>
        
        <p className="mt-2 text-gray-600 italic">{currentRole.description}</p>
      </div>
      
      {/* Summary section */}
      <div className="mb-8 p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Summary</h2>
        <div className="prose max-w-none">
          <p>{summary}</p>
        </div>
      </div>
      
      {/* Insights by type */}
      {Object.entries(groupedInsights).map(([type, typeInsights]) => (
        <div key={type} className="mb-8">
          <h2 className="text-xl font-bold mb-4 capitalize">
            {type.replace(/_/g, ' ')} Insights
          </h2>
          
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {typeInsights.map(insight => (
              <div key={insight.id} className="p-6 bg-white rounded-lg shadow-md">
                <h3 className="text-lg font-semibold mb-3">
                  {insight.question}
                </h3>
                
                <div className="prose max-w-none mb-4">
                  <p>{insight.answer}</p>
                </div>
                
                {/* Render visualizations for this insight */}
                {getVisualizationsForInsight(insight.id).map((viz, idx) => (
                  <div key={idx} className="mt-4">
                    <Visualization 
                      type={viz.type}
                      data={viz.data}
                      config={viz.config}
                    />
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      ))}
      
      {/* If no insights for this role */}
      {Object.keys(groupedInsights).length === 0 && (
        <div className="p-6 bg-gray-100 rounded-md">
          <p>No specific insights available for the {currentRole.name} role.</p>
        </div>
      )}
    </div>
  );
}

InsightDisplay.propTypes = {
  insights: PropTypes.object,
  visualizations: PropTypes.array,
  summary: PropTypes.string
};

InsightDisplay.defaultProps = {
  insights: null,
  visualizations: [],
  summary: ''
};

export default InsightDisplay;