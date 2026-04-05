import { useState } from 'react';
import { api } from '../utils/api';

export default function CreateDecision({ token, user, onBack, onCreated }) {
  const [formData, setFormData] = useState({
    title: '',
    context: '',
    area: user.decision_areas?.[0] || '',
    decision_type: 'operational',
    options: [],
    hypotheses: [],
    signals: [],
    conviction: 5
  });

  const [optionInput, setOptionInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.createDecision(token, formData);
      onCreated();
    } catch (error) {
      console.error('Error creating decision:', error);
      alert('Error al crear decisión');
    } finally {
      setLoading(false);
    }
  };

  const addOption = () => {
    if (optionInput && !formData.options.includes(optionInput)) {
      setFormData({
        ...formData,
        options: [...formData.options, optionInput]
      });
      setOptionInput('');
    }
  };

  const removeOption = (option) => {
    setFormData({
      ...formData,
      options: formData.options.filter(o => o !== option)
    });
  };

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', padding: '20px' }}>
      <h1>Nueva Decisión</h1>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '20px' }}>
          <label>Título:</label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            placeholder="Ej: Expandir a nuevo mercado"
            style={{ width: '100%', padding: '8px', marginTop: '8px', boxSizing: 'border-box' }}
            required
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Contexto:</label>
          <textarea
            value={formData.context}
            onChange={(e) => setFormData({ ...formData, context: e.target.value })}
            placeholder="Describe la situación y por qué necesitas tomar esta decisión"
            style={{ width: '100%', padding: '8px', marginTop: '8px', minHeight: '100px', boxSizing: 'border-box' }}
            required
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Área:</label>
          <select
            value={formData.area}
            onChange={(e) => setFormData({ ...formData, area: e.target.value })}
            style={{ width: '100%', padding: '8px', marginTop: '8px' }}
          >
            {user.decision_areas?.map(area => (
              <option key={area} value={area}>{area}</option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Tipo de decisión:</label>
          <select
            value={formData.decision_type}
            onChange={(e) => setFormData({ ...formData, decision_type: e.target.value })}
            style={{ width: '100%', padding: '8px', marginTop: '8px' }}
          >
            <option value="operational">Operacional</option>
            <option value="strategic">Estratégica</option>
            <option value="vital">Vital</option>
          </select>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Opciones consideradas:</label>
          <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
            <input
              type="text"
              value={optionInput}
              onChange={(e) => setOptionInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addOption())}
              placeholder="Ej: Opción A"
              style={{ flex: 1, padding: '8px' }}
            />
            <button type="button" onClick={addOption} style={{ padding: '8px 16px' }}>
              Agregar
            </button>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
            {formData.options.map(option => (
              <span key={option} style={{
                backgroundColor: '#e3f2fd',
                padding: '6px 12px',
                borderRadius: '20px',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}>
                {option}
                <button
                  type="button"
                  onClick={() => removeOption(option)}
                  style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                >
                  ✕
                </button>
              </span>
            ))}
          </div>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Convicción (1-10):</label>
          <input
            type="range"
            min="1"
            max="10"
            value={formData.conviction}
            onChange={(e) => setFormData({ ...formData, conviction: parseInt(e.target.value) })}
            style={{ width: '100%', marginTop: '8px' }}
          />
          <p style={{ margin: '8px 0 0 0', textAlign: 'center' }}>{formData.conviction}/10</p>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            type="submit"
            disabled={loading || !formData.title || !formData.context}
            style={{
              flex: 1,
              padding: '12px',
              backgroundColor: '#4285f4',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              opacity: loading ? 0.7 : 1
            }}
          >
            {loading ? 'Creando...' : 'Crear Decisión'}
          </button>
          <button
            type="button"
            onClick={onBack}
            style={{
              flex: 1,
              padding: '12px',
              backgroundColor: '#f0f0f0',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}
