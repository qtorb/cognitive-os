// API client para Cognitive OS Backend
const API_BASE = 'http://localhost:8000';

export const api = {
  // Auth
  getLoginUrl: async () => {
    const response = await fetch(`${API_BASE}/auth/login-url`);
    return response.json();
  },

  processCallback: async (code) => {
    const response = await fetch(`${API_BASE}/auth/callback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    return response.json();
  },

  getCurrentUser: async (token) => {
    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
  },

  // Onboarding
  completeOnboarding: async (token, data) => {
    const response = await fetch(`${API_BASE}/onboarding`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data)
    });
    return response.json();
  },

  // Decisions
  createDecision: async (token, decision) => {
    const response = await fetch(`${API_BASE}/decisions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(decision)
    });
    return response.json();
  },

  getDecisions: async (token) => {
    const response = await fetch(`${API_BASE}/decisions`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
  },

  getDecision: async (token, decisionId) => {
    const response = await fetch(`${API_BASE}/decisions/${decisionId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
  },

  // AI Analysis
  analyzeDecision: async (token, decisionId) => {
    const response = await fetch(`${API_BASE}/decisions/${decisionId}/analyze`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
  },

  counterargument: async (token, decisionId) => {
    const response = await fetch(`${API_BASE}/decisions/${decisionId}/counterargument`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
  },

  premortem: async (token, decisionId) => {
    const response = await fetch(`${API_BASE}/decisions/${decisionId}/premortem`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
  }
};
