import React, { useState } from 'react';

const Upload = ({ onImageAdded }) => {
  const [formData, setFormData] = useState({
    title: '',
    image_file: null
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const handleInputChange = (e) => {
    const { name, value, files } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'image_file' ? files[0] : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title.trim()) {
      setMessage('Veuillez saisir un titre');
      setMessageType('error');
      return;
    }
    
    if (!formData.image_file) {
      setMessage('Veuillez sélectionner un fichier image');
      setMessageType('error');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      // Créer FormData pour l'upload
      const uploadData = new FormData();
      uploadData.append('title', formData.title);
      uploadData.append('image_file', formData.image_file);

      const response = await fetch('http://127.0.0.1:8000/upload/', {
        method: 'POST',
        body: uploadData,
        // Ne pas définir Content-Type, laissez le navigateur le faire automatiquement
      });

      if (response.ok) {
        setMessage('✅ Image uploadée avec succès !');
        setMessageType('success');
        
        // Réinitialiser le formulaire
        setFormData({
          title: '',
          image_file: null
        });
        
        // Réinitialiser l'input file
        const fileInput = document.getElementById('image_file');
        if (fileInput) fileInput.value = '';
        
        // Notifier le composant parent pour rafraîchir la galerie
        if (onImageAdded) {
          onImageAdded();
        }
      } else {
        const errorText = await response.text();
        setMessage(`❌ Erreur lors de l'upload: ${response.status}`);
        setMessageType('error');
        console.error('Upload error:', errorText);
      }
    } catch (error) {
      setMessage(`❌ Erreur de connexion: ${error.message}`);
      setMessageType('error');
      console.error('Network error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '500px', margin: '0 auto' }}>
      <h2>📤 Upload d'image</h2>
      
      <div style={{
        backgroundColor: '#e7f3ff',
        padding: '15px',
        borderRadius: '5px',
        marginBottom: '20px',
        borderLeft: '4px solid #007bff'
      }}>
        <strong>ℹ️ Information :</strong> Votre image sera automatiquement uploadée sur ImgBB et ajoutée à la galerie.
      </div>

      {message && (
        <div style={{
          padding: '10px',
          marginBottom: '20px',
          borderRadius: '5px',
          backgroundColor: messageType === 'success' ? '#d4edda' : '#f8d7da',
          color: messageType === 'success' ? '#155724' : '#721c24',
          border: `1px solid ${messageType === 'success' ? '#c3e6cb' : '#f5c6cb'}`
        }}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
      }}>
        <div style={{ marginBottom: '20px' }}>
          <label 
            htmlFor="title" 
            style={{ 
              display: 'block', 
              marginBottom: '5px', 
              fontWeight: 'bold',
              color: '#333'
            }}
          >
            Titre de l'image *
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            placeholder="Entrez le titre de l'image"
            required
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '5px',
              fontSize: '16px',
              boxSizing: 'border-box'
            }}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label 
            htmlFor="image_file" 
            style={{ 
              display: 'block', 
              marginBottom: '5px', 
              fontWeight: 'bold',
              color: '#333'
            }}
          >
            Fichier image *
          </label>
          <input
            type="file"
            id="image_file"
            name="image_file"
            accept="image/*"
            onChange={handleInputChange}
            required
            style={{
              width: '100%',
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '5px',
              fontSize: '16px',
              boxSizing: 'border-box'
            }}
          />
        </div>

        <div style={{ textAlign: 'center' }}>
          <button
            type="submit"
            disabled={loading}
            style={{
              backgroundColor: loading ? '#6c757d' : '#007bff',
              color: 'white',
              padding: '12px 30px',
              border: 'none',
              borderRadius: '5px',
              fontSize: '16px',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'background-color 0.3s'
            }}
          >
            {loading ? '🔄 Upload en cours...' : '📤 Uploader l\'image'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Upload;

