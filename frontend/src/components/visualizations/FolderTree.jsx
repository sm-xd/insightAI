import React, { useState } from 'react';
import PropTypes from 'prop-types';

/**
 * FolderTree component visualizes the folder structure of a codebase.
 * 
 * @param {Object} props - Component props
 * @param {Object} props.data - Folder tree data
 * @param {Object} props.config - Configuration options
 */
function FolderTree({ data, config }) {
  // In a real implementation, data would be properly structured
  // For this placeholder, we'll parse a simple string representation
  
  const [expandedNodes, setExpandedNodes] = useState({});
  
  // Parse mock data - in real implementation, data would be properly structured
  const parseMockData = () => {
    // This is a simplified placeholder
    // In a real implementation, the data would be a proper tree structure
    
    // Mock folder structure for placeholder
    return {
      name: 'insightAI',
      type: 'directory',
      children: [
        {
          name: 'frontend',
          type: 'directory',
          children: [
            { name: 'src', type: 'directory', children: [
              { name: 'components', type: 'directory', children: [] },
              { name: 'pages', type: 'directory', children: [] },
              { name: 'context', type: 'directory', children: [] },
              { name: 'App.jsx', type: 'file' },
              { name: 'index.js', type: 'file' }
            ]},
            { name: 'package.json', type: 'file' }
          ]
        },
        {
          name: 'backend',
          type: 'directory',
          children: [
            { name: 'main.py', type: 'file' },
            { name: 'config.py', type: 'file' },
            { name: 'utils.py', type: 'file' }
          ]
        },
        {
          name: 'rag',
          type: 'directory',
          children: [
            { name: 'pipeline.py', type: 'file' },
            { name: 'role_manager.py', type: 'file' },
            { name: 'templates', type: 'directory', children: [
              { name: 'project_manager.json', type: 'file' }
            ]}
          ]
        },
        {
          name: 'parsers',
          type: 'directory',
          children: [
            { name: 'base_parser.py', type: 'file' },
            { name: 'parser_registry.py', type: 'file' },
            { name: 'languages', type: 'directory', children: [] },
            { name: 'grammars', type: 'directory', children: [] }
          ]
        },
        {
          name: 'agents',
          type: 'directory', 
          children: []
        },
        {
          name: 'tests',
          type: 'directory',
          children: []
        },
        {
          name: 'README.md',
          type: 'file'
        }
      ]
    };
  };
  
  const mockTree = parseMockData();
  const maxDepth = config?.max_depth || 3;
  
  const toggleExpand = (path) => {
    setExpandedNodes({
      ...expandedNodes,
      [path]: !expandedNodes[path]
    });
  };
  
  const renderTreeNode = (node, path = '', depth = 0) => {
    const currentPath = `${path}/${node.name}`;
    const isExpanded = expandedNodes[currentPath] !== false;
    
    // Skip rendering if we're beyond max_depth (unless expanded)
    if (depth > maxDepth && !isExpanded) {
      return null;
    }
    
    return (
      <div key={currentPath} className="ml-4">
        <div className="flex items-center py-1">
          {node.type === 'directory' && node.children && node.children.length > 0 ? (
            <button 
              onClick={() => toggleExpand(currentPath)}
              className="mr-1 focus:outline-none"
            >
              {isExpanded ? (
                <span className="text-gray-500">▼</span>
              ) : (
                <span className="text-gray-500">►</span>
              )}
            </button>
          ) : (
            <span className="w-4 mr-1"></span>
          )}
          
          {node.type === 'directory' ? (
            <span className="text-blue-500">
              <i className="far fa-folder mr-1"></i> {node.name}/
            </span>
          ) : (
            <span className="text-gray-700">
              <i className="far fa-file mr-1"></i> {node.name}
            </span>
          )}
        </div>
        
        {node.type === 'directory' && isExpanded && node.children && (
          <div>
            {node.children.map(child => renderTreeNode(child, currentPath, depth + 1))}
          </div>
        )}
      </div>
    );
  };
  
  return (
    <div className="folder-tree border rounded-md p-4 bg-white">
      <h3 className="font-medium mb-2">Codebase Structure</h3>
      <div className="overflow-auto max-h-96 font-mono text-sm">
        {renderTreeNode(mockTree)}
      </div>
      <div className="mt-2 text-xs text-gray-500">
        {maxDepth < 10 && (
          <p>Showing {maxDepth} levels deep. Click folders to expand/collapse.</p>
        )}
      </div>
    </div>
  );
}

FolderTree.propTypes = {
  data: PropTypes.oneOfType([PropTypes.string, PropTypes.object]).isRequired,
  config: PropTypes.shape({
    max_depth: PropTypes.number
  })
};

FolderTree.defaultProps = {
  config: {
    max_depth: 3
  }
};

export default FolderTree;