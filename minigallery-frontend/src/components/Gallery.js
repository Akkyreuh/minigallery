import React, { useState, useEffect } from 'react';

const Gallery = ({ refreshTrigger }) => {
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchImages = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/images/');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setImages(data.results || []);
      setError(null);
    } catch (err) {
      setError(`Erreur lors du chargement des images: ${err.message}`);
      console.error('Error fetching images:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchImages();
  }, [refreshTrigger]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '20px' }}>
        <div>🔄 Chargement des images...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '20px', color: 'red' }}>
        <div>❌ {error}</div>
        <button 
          onClick={fetchImages}
          style={{
            marginTop: '10px',
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Réessayer
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <h2>🖼️ Galerie d'images</h2>
      
      {images.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          <div>📷 Aucune image dans la galerie</div>
          <div style={{ fontSize: '14px', marginTop: '10px' }}>
            Utilisez le formulaire d'upload pour ajouter des images
          </div>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
          gap: '20px',
          marginTop: '20px'
        }}>
          {images.map((image) => (
            <div
              key={image.id}
              style={{
                border: '1px solid #ddd',
                borderRadius: '8px',
                padding: '15px',
                backgroundColor: 'white',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                transition: 'transform 0.2s ease'
              }}
              onMouseEnter={(e) => e.target.style.transform = 'translateY(-2px)'}
              onMouseLeave={(e) => e.target.style.transform = 'translateY(0)'}
            >
              <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>
                {image.title}
              </h3>
              
              {image.image_url ? (
                <img
                  src={image.image_url}
                  alt={image.title}
                  style={{
                    width: '100%',
                    height: '200px',
                    objectFit: 'cover',
                    borderRadius: '5px',
                    marginBottom: '10px'
                  }}
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'block';
                  }}
                />
              ) : null}
              
              <div style={{ display: 'none', textAlign: 'center', padding: '40px', color: '#666' }}>
                Image non disponible
              </div>
              
              <div style={{ fontSize: '12px', color: '#666', marginBottom: '5px' }}>
                📅 {new Date(image.created_at).toLocaleDateString('fr-FR', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </div>
              
              <div style={{ fontSize: '12px', color: '#007bff' }}>
                🔗 Source: {image.source}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Gallery;

