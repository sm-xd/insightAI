import React from 'react';

/**
 * Footer component with copyright and links
 */
function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">InsightAI</h3>
            <p className="text-gray-300">
              A role-aware AI teammate for codebase insights, helping teams quickly understand complex projects.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <a 
                  href="/upload" 
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  Upload Codebase
                </a>
              </li>
              <li>
                <a 
                  href="/" 
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  Home
                </a>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a 
                  href="https://github.com/yourusername/insightAI"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  GitHub Repository
                </a>
              </li>
              <li>
                <a 
                  href="#"
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  Documentation
                </a>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
          <p>&copy; {currentYear} InsightAI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;