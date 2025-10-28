import React, { useState } from 'react';
import './App.css';
import Gallery from './components/Gallery';
import Upload from './components/Upload';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [activeTab, setActiveTab] = useState('gallery');

  const handleImageAdded = () => {
    // Incrémenter le trigger pour forcer le rechargement de la galerie
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="App">
      <header style={{
        backgroundColor: '#007bff',
        color: 'white',
        padding: '20px',
        textAlign: 'center',
        marginBottom: '20px'
      }}>
        <h1>🖼️ Mini Gallery - React Frontend</h1>
        <p>Interface React consommant l'API Django</p>
      </header>

      <nav style={{
        display: 'flex',
        justifyContent: 'center',
        marginBottom: '20px',
        gap: '10px'
      }}>
        <button
          onClick={() => setActiveTab('gallery')}
          style={{
            padding: '10px 20px',
            backgroundColor: activeTab === 'gallery' ? '#007bff' : '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          🖼️ Galerie
        </button>
        <button
          onClick={() => setActiveTab('upload')}
          style={{
            padding: '10px 20px',
            backgroundColor: activeTab === 'upload' ? '#007bff' : '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          📤 Upload
        </button>
      </nav>

      <main>
        {activeTab === 'gallery' && <Gallery refreshTrigger={refreshTrigger} />}
        {activeTab === 'upload' && <Upload onImageAdded={handleImageAdded} />}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '20px',
        backgroundColor: '#f8f9fa',
        marginTop: '40px',
        color: '#666'
      }}>
        <p>Mini Gallery - Frontend React + Backend Django</p>
        <p>API: <code>http://127.0.0.1:8000/api/images/</code></p>
      </footer>
    </div>
  );
}

export default App;

