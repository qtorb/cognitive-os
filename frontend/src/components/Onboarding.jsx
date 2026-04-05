import { useState } from 'react';
import { api } from '../utils/api';
import ProgressBar from './ProgressBar';

export default function Onboarding({ token, onComplete }) {
  const [formData, setFormData] = useState({
    role: '',
    decision_areas: [],
    decision_types: [],
    horizon: '',
    known_bias: ''
  });

  const [areaInput, setAreaInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.completeOnboarding(token, formData);
      onComplete();
    } catch (error) {
      console.error('Error en onboarding:', error);
      alert('Error al completar onboarding');
    } finally {
      setLoading(false);
    }
  };

  const addArea = () => {
    if (areaInput && !formData.decision_areas.includes(areaInput)) {
      setFormData({
        ...formData,
        decision_areas: [...formData.decision_areas, areaInput]
      });
      setAreaInput('');
    }
  };

  const removeArea = (area) => {
    setFormData({
      ...formData,
      decision_areas: formData.decision_areas.filter(a => a !== area)
    });
  };

  const toggleType = (type) => {
    if (formData.decision_types.includes(type)) {
      setFormData({
        ...formData,
        decision_types: formData.decision_types.filter(t => t !== type)
      });
    } else {
      setFormData({
        ...formData,
        decision_types: [...formData.decision_types, type]
      });
    }
  };

  return (
    <div>
      <ProgressBar currentStep="onboarding" />
      <div style={{ maxWidth: '500px', margin: '40px auto', padding: '20px' }}>
        <h1>Completar Perfil</h1>
        <p>Cuéntanos sobre ti para personalizar Cognitive OS</p>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '20px' }}>
          <label>Tu rol:</label>
          <input
            type="text"
            value={formData.role}
            onChange={(e) => setFormData({ ...formData, role: e.target.value })}
            placeholder="Ej: Product Manager, Emprendedor"
            style={{ width: '100%', padding: '8px', marginTop: '8px', boxSizing: 'border-box' }}
            required
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Áreas de decisión (agrega varias):</label>
          <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
            <input
              type="text"
              value={areaInput}
              onChange={(e) => setAreaInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addArea())}
              placeholder="Ej: Estrategia de producto"
              style={{ flex: 1, padding: '8px' }}
            />
            <button type="button" onClick={addArea} style={{ padding: '8px 16px' }}>
              Agregar
            </button>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
            {formData.decision_areas.map(area => (
              <span key={area} style={{
                backgroundColor: '#e3f2fd',
                padding: '6px 12px',
                borderRadius: '20px',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}>
                {area}
                <button
                  type="button"
                  onClick={() => removeArea(area)}
                  style={{ background: 'none', border: 'none', cursor: 'pointer' }}
                >
                  ✕
                </button>
              </span>
            ))}
          </div>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Tipos de decisión importantes para ti:</label>
          <div style={{ marginTop: '8px' }}>
            {['operational', 'strategic', 'vital'].map(type => (
              <label key={type} style={{ display: 'block', marginBottom: '8px' }}>
                <input
                  type="checkbox"
                  checked={formData.decision_types.includes(type)}
                  onChange={() => toggleType(type)}
                />
                {' '}{type === 'operational' ? 'Operacional' : type === 'strategic' ? 'Estratégica' : 'Vital'}
              </label>
            ))}
          </div>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Horizonte temporal:</label>
          <select
            value={formData.horizon}
            onChange={(e) => setFormData({ ...formData, horizon: e.target.value })}
            style={{ width: '100%', padding: '8px', marginTop: '8px' }}
            required
          >
            <option value="">Selecciona...</option>
            <option value="daily">Diario</option>
            <option value="weekly">Semanal</option>
            <option value="monthly">Mensual</option>
            <option value="quarterly">Trimestral</option>
            <option value="yearly">Anual</option>
          </select>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label>Sesgo reconocido (opcional):</label>
          <textarea
            value={formData.known_bias}
            onChange={(e) => setFormData({ ...formData, known_bias: e.target.value })}
            placeholder="Ej: Tiiendo a sobreestimar capacidades del equipo"
            style={{ width: '100%', padding: '8px', marginTop: '8px', minHeight: '80px', boxSizing: 'border-box' }}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !formData.role || formData.decision_areas.length === 0}
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
          {loading ? 'Guardando...' : 'Completar Perfil'}
        </button>
      </form>
      </div>
    </div>
  );
}
