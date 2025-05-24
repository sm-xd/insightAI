import React from 'react';
import { Link } from 'react-router-dom';

/**
 * Header component containing navigation and branding
 */
function Header() {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2">
          <svg 
            className="h-8 w-8 text-blue-600" 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" 
            />
          </svg>
          <span className="font-bold text-xl text-gray-900">InsightAI</span>
        </Link>
        
        <nav>
          <ul className="flex space-x-6">
            <li>
              <Link 
                to="/" 
                className="text-gray-600 hover:text-blue-600 transition-colors"
              >
                Home
              </Link>
            </li>
            <li>
              <Link 
                to="/upload" 
                className="text-gray-600 hover:text-blue-600 transition-colors"
              >
                Upload
              </Link>
            </li>
            <li>
              <a 
                href="https://github.com/yourusername/insightAI" 
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-600 hover:text-blue-600 transition-colors"
              >
                GitHub
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}

export default Header;