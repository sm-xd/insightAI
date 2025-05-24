import React from 'react';
import { Link } from 'react-router-dom';
import { useRole } from '../context/RoleContext';

/**
 * Home page component with information about the project and role selection
 */
function HomePage() {
  const { roles, selectedRole, changeRole } = useRole();
  
  return (
    <div className="space-y-12">
      {/* Hero section */}
      <section className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          InsightAI: Role-Aware AI Teammate for Codebase Insights
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Quickly understand complex codebases with personalized insights tailored to your team role.
          Upload your code and get instant, actionable information.
        </p>
        <div className="mt-8">
          <Link 
            to="/upload" 
            className="btn-primary text-lg py-3 px-8"
          >
            Get Started
          </Link>
        </div>
      </section>
      
      {/* Features section */}
      <section className="card">
        <h2 className="text-2xl font-bold mb-6">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="bg-blue-100 rounded-full p-4 w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">1. Upload or Clone</h3>
            <p className="text-gray-600">Upload your codebase as a ZIP file or provide a GitHub repository URL.</p>
          </div>
          
          <div className="text-center">
            <div className="bg-blue-100 rounded-full p-4 w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">2. Select Your Role</h3>
            <p className="text-gray-600">Choose your team role to get insights tailored to your specific needs.</p>
          </div>
          
          <div className="text-center">
            <div className="bg-blue-100 rounded-full p-4 w-16 h-16 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">3. Get Insights</h3>
            <p className="text-gray-600">Receive detailed analysis, visualizations, and actionable insights about the codebase.</p>
          </div>
        </div>
      </section>
      
      {/* Role selection section */}
      <section className="card">
        <h2 className="text-2xl font-bold mb-6">Choose Your Role</h2>
        <p className="text-gray-600 mb-6">
          InsightAI tailors its analysis based on your team role. Select your role to see what insights you'll receive.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {roles.map(role => (
            <div 
              key={role.id}
              onClick={() => changeRole(role.id)}
              className={`
                p-4 rounded-lg border-2 cursor-pointer transition-all
                ${selectedRole === role.id 
                  ? 'border-blue-500 bg-blue-50' 
                  : 'border-gray-200 hover:border-blue-300'}
              `}
            >
              <h3 className="font-semibold text-lg mb-2">{role.name}</h3>
              <p className="text-sm text-gray-600">{role.description}</p>
            </div>
          ))}
        </div>
        
        <div className="mt-8 text-center">
          <Link 
            to="/upload" 
            className="btn-primary"
          >
            Continue with {roles.find(r => r.id === selectedRole)?.name}
          </Link>
        </div>
      </section>
      
      {/* Tech used section */}
      <section>
        <h2 className="text-2xl font-bold mb-6">Powered By</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <h3 className="font-semibold">Tree-sitter</h3>
            <p className="text-sm text-gray-600">For accurate code parsing</p>
          </div>
          <div>
            <h3 className="font-semibold">LangChain</h3>
            <p className="text-sm text-gray-600">For RAG pipelines</p>
          </div>
          <div>
            <h3 className="font-semibold">FAISS</h3>
            <p className="text-sm text-gray-600">For efficient vector search</p>
          </div>
          <div>
            <h3 className="font-semibold">React + Tailwind</h3>
            <p className="text-sm text-gray-600">For the user interface</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;