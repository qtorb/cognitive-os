import { useState } from 'react';
import { api } from '../utils/api';
import ProgressBar from './ProgressBar';

export default function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleTestLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/auth/test-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();

      // Save token to localStorage
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify({
        user_id: data.user_id,
        email: data.email,
        name: data.name,
        onboarded: data.onboarded
      }));

      onLoginSuccess(data);
    } catch (err) {
      console.error('Error during login:', err);
      setError('Error al iniciar sesión. Intenta de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <ProgressBar currentStep="login" />
      <div style={{
        maxWidth: '400px',
        margin: '40px auto',
        textAlign: 'center',
        padding: '20px',
        fontFamily: 'sans-serif'
      }}>
        <h1>Cognitive OS</h1>
        <p>Sistema cognitivo personal para decisiones</p>

      <form onSubmit={handleTestLogin} style={{ marginTop: '30px' }}>
        <div style={{ marginBottom: '16px', textAlign: 'left' }}>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
            Email (para testing):
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="tu@email.com"
            required
            style={{
              width: '100%',
              padding: '12px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontSize: '16px',
              boxSizing: 'border-box'
            }}
          />
        </div>

        {error && (
          <div style={{
            color: '#d32f2f',
            marginBottom: '16px',
            fontSize: '14px'
          }}>
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !email}
          style={{
            width: '100%',
            padding: '12px',
            backgroundColor: '#4285f4',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            fontSize: '16px',
            fontWeight: 'bold',
            cursor: 'pointer',
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>

        <p style={{ marginTop: '20px', fontSize: '12px', color: '#999' }}>
          📝 Modo de testing - usa cualquier email para acceder
        </p>
      </div>
    </div>
  );
}
