import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import JobDescriptionEntry from './components/JobDescriptionEntry';

function App() {
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    // Force component remount on page reload
    const handleBeforeUnload = () => {
      setReloadKey(prev => prev + 1);
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  return (
    <div className="App">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10b981',
              secondary: '#fff',
            },
          },
          error: {
            duration: 4000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />
      <JobDescriptionEntry key={reloadKey} />
    </div>
  );
}

export default App; 