import { useState, useEffect } from 'react';
import { api } from '../utils/api';
import ProgressBar from './ProgressBar';
import CreateDecision from './CreateDecision';
import DecisionDetail from './DecisionDetail';

export default function Dashboard({ token, user, onLogout }) {
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [selectedDecision, setSelectedDecision] = useState(null);

  useEffect(() => {
    loadDecisions();
  }, []);

  const loadDecisions = async () => {
    try {
      const data = await api.getDecisions(token);
      setDecisions(data.decisions || []);
    } catch (error) {
      console.error('Error loading decisions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateDecision = async () => {
    loadDecisions();
    setShowCreate(false);
  };

  if (selectedDecision) {
    return (
      <DecisionDetail
        token={token}
        decisionId={selectedDecision.id}
        onBack={() => setSelectedDecision(null)}
        onRefresh={loadDecisions}
      />
    );
  }

  if (showCreate) {
    return (
      <CreateDecision
        token={token}
        user={user}
        onBack={() => setShowCreate(false)}
        onCreated={handleCreateDecision}
      />
    );
  }

  return (
    <div>
      <ProgressBar currentStep="dashboard" />
      <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h1>Cognitive OS</h1>
        <div>
          <span style={{ marginRight: '20px' }}>👤 {user.name || user.email}</span>
          <button onClick={onLogout} style={{ padding: '8px 16px', cursor: 'pointer' }}>
            Salir
          </button>
        </div>
      </div>

      <div style={{
        backgroundColor: '#f5f5f5',
        padding: '15px',
        borderRadius: '4px',
        marginBottom: '20px'
      }}>
        <p><strong>Rol:</strong> {user.role || 'No completado'}</p>
        <p><strong>Áreas:</strong> {user.decision_areas?.join(', ') || 'No completado'}</p>
      </div>

      <button
        onClick={() => setShowCreate(true)}
        style={{
          padding: '12px 24px',
          backgroundColor: '#4285f4',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          fontSize: '16px',
          fontWeight: 'bold',
          cursor: 'pointer',
          marginBottom: '20px'
        }}
      >
        + Nueva Decisión
      </button>

      {loading ? (
        <p>Cargando decisiones...</p>
      ) : decisions.length === 0 ? (
        <p>No tienes decisiones registradas. ¡Crea la primera!</p>
      ) : (
        <div>
          <h2>Tus Decisiones ({decisions.length})</h2>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '16px'
          }}>
            {decisions.map(decision => (
              <div
                key={decision.id}
                onClick={() => setSelectedDecision(decision)}
                style={{
                  border: '1px solid #ddd',
                  padding: '16px',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  backgroundColor: '#fff'
                }}
                onMouseOver={(e) => e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)'}
                onMouseOut={(e) => e.currentTarget.style.boxShadow = 'none'}
              >
                <h3 style={{ margin: '0 0 8px 0' }}>{decision.title}</h3>
                <p style={{ margin: '0 0 8px 0', color: '#666', fontSize: '14px' }}>
                  📍 {decision.area}
                </p>
                <p style={{ margin: '0 0 8px 0', color: '#666', fontSize: '14px' }}>
                  Status: <strong>{decision.status}</strong>
                </p>
                <p style={{ margin: '0', color: '#999', fontSize: '12px' }}>
                  {new Date(decision.created_at).toLocaleDateString('es-ES')}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
      </div>
    </div>
  );
}
