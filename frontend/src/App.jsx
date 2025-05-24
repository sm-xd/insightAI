import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

// Component imports
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import ResultsPage from './pages/ResultsPage';

// Context providers
import { CodebaseProvider } from './context/CodebaseContext';
import { RoleProvider } from './context/RoleContext';

function App() {
  return (
    <Router>
      <CodebaseProvider>
        <RoleProvider>
          <div className="min-h-screen flex flex-col bg-gray-50">
            <Header />
            <main className="flex-grow container mx-auto px-4 py-8">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/upload" element={<UploadPage />} />
                <Route path="/results/:codebaseId" element={<ResultsPage />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </RoleProvider>
      </CodebaseProvider>
    </Router>
  );
}

export default App;