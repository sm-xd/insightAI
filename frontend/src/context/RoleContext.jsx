import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

/**
 * Context for managing user role selection across components
 */
const RoleContext = createContext();

/**
 * Provider component for Role context
 */
export function RoleProvider({ children }) {
  const [roles, setRoles] = useState([
    {
      id: 'project_manager',
      name: 'Project Manager',
      description: 'Focus on high-level architecture, dependencies, and project structure.'
    },
    {
      id: 'frontend_developer',
      name: 'Frontend Developer',
      description: 'Focus on UI components, state management, and frontend architecture.'
    },
    {
      id: 'backend_developer',
      name: 'Backend Developer',
      description: 'Focus on API design, data models, and server architecture.'
    },
    {
      id: 'ai_ml_engineer',
      name: 'AI/ML Engineer',
      description: 'Focus on ML models, data pipelines, and AI architecture.'
    }
  ]);
  
  const [selectedRole, setSelectedRole] = useState('project_manager');
  const [loadingRoles, setLoadingRoles] = useState(false);
  const [error, setError] = useState(null);

  // Load available roles from the backend
  useEffect(() => {
    async function fetchRoles() {
      setLoadingRoles(true);
      setError(null);
      
      try {
        // This endpoint would return available roles from the backend
        const response = await axios.get('/api/roles');
        setRoles(response.data.roles);
      } catch (err) {
        console.error('Error fetching roles:', err);
        // If API call fails, we already have default roles from state
        setError('Failed to load roles from server, using default roles');
      } finally {
        setLoadingRoles(false);
      }
    }
    
    // Comment out the API call for now since the endpoint doesn't exist yet
    // fetchRoles();
  }, []);

  /**
   * Change the currently selected role
   * @param {string} roleId - ID of the selected role
   */
  const changeRole = (roleId) => {
    if (roles.some(role => role.id === roleId)) {
      setSelectedRole(roleId);
      return true;
    }
    return false;
  };

  /**
   * Get the currently selected role object
   * @returns {Object} Selected role object
   */
  const getCurrentRole = () => {
    return roles.find(role => role.id === selectedRole) || roles[0];
  };

  return (
    <RoleContext.Provider
      value={{
        roles,
        selectedRole,
        loadingRoles,
        error,
        changeRole,
        getCurrentRole
      }}
    >
      {children}
    </RoleContext.Provider>
  );
}

/**
 * Hook for using role context
 */
export function useRole() {
  const context = useContext(RoleContext);
  if (!context) {
    throw new Error('useRole must be used within a RoleProvider');
  }
  return context;
}