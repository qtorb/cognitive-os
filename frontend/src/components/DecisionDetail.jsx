import { useState, useEffect } from 'react';
import { api } from '../utils/api';

export default function DecisionDetail({ token, decisionId, onBack }) {
  const [decision, setDecision] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisType, setAnalysisType] = useState('analyze');

  useEffect(() => {
    loadDecision();
  }, []);

  const loadDecision = async () => {
    try {
      const data = await api.getDecision(token, decisionId);
      setDecision(data);
    } catch (error) {
      console.error('Error loading decision:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalysis = async (type) => {
    setAnalyzing(true);
    setAnalysisType(type);

    try {
      let result;
      if (type === 'analyze') {
        result = await api.analyzeDecision(token, decisionId);
      } else if (type === 'counterargument') {
        result = await api.counterargument(token, decisionId);
      } else if (type === 'premortem') {
        result = await api.premortem(token, decisionId);
      }
      setAnalysis(result.analysis);
    } catch (error) {
      console.error('Error during analysis:', error);
      alert('Error al hacer análisis');
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return <div style={{ padding: '20px' }}>Cargando...</div>;
  }

  if (!decision) {
    return <div style={{ padding: '20px' }}>Decisión no encontrada</div>;
  }

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
      <button
        onClick={onBack}
        style={{ marginBottom: '20px', padding: '8px 16px', cursor: 'pointer' }}
      >
        ← Volver
      </button>

      <h1>{decision.title}</h1>

      <div style={{
        backgroundColor: '#f9f9f9',
        padding: '16px',
        borderRadius: '8px',
        marginBottom: '20px'
      }}>
        <p><strong>Contexto:</strong></p>
        <p>{decision.context}</p>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '16px' }}>
          <div>
            <p><strong>Área:</strong> {decision.area}</p>
            <p><strong>Tipo:</strong> {decision.decision_type}</p>
          </div>
          <div>
            <p><strong>Estado:</strong> {decision.status}</p>
            <p><strong>Convicción:</strong> {decision.conviction}/10</p>
          </div>
        </div>

        {decision.options && decision.options.length > 0 && (
          <div style={{ marginTop: '16px' }}>
            <p><strong>Opciones:</strong></p>
            <ul>
              {decision.options.map((opt, i) => (
                <li key={i}>{opt}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h2>Análisis con IA</h2>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          <button
            onClick={() => handleAnalysis('analyze')}
            disabled={analyzing}
            style={{
              padding: '10px 16px',
              backgroundColor: '#4285f4',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              opacity: analyzing ? 0.7 : 1
            }}
          >
            {analyzing && analysisType === 'analyze' ? '⏳ Analizando...' : '🔍 Analizar'}
          </button>

          <button
            onClick={() => handleAnalysis('counterargument')}
            disabled={analyzing}
            style={{
              padding: '10px 16px',
              backgroundColor: '#ea4335',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              opacity: analyzing ? 0.7 : 1
            }}
          >
            {analyzing && analysisType === 'counterargument' ? '⏳ Contraargumentando...' : '⚔️ Contraargumento'}
          </button>

          <button
            onClick={() => handleAnalysis('premortem')}
            disabled={analyzing}
            style={{
              padding: '10px 16px',
              backgroundColor: '#fbbc04',
              color: '#000',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              opacity: analyzing ? 0.7 : 1
            }}
          >
            {analyzing && analysisType === 'premortem' ? '⏳ Pre-mortem...' : '💀 Pre-mortem'}
          </button>
        </div>
      </div>

      {analysis && (
        <div style={{
          backgroundColor: '#f0f0f0',
          padding: '16px',
          borderRadius: '8px',
          whiteSpace: 'pre-wrap',
          lineHeight: '1.6'
        }}>
          {analysis}
        </div>
      )}

      <div style={{ marginTop: '20px', textAlign: 'center', color: '#999' }}>
        <p>Creada: {new Date(decision.created_at).toLocaleDateString('es-ES')}</p>
      </div>
    </div>
  );
}
