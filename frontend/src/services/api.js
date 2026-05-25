const API_BASE = 'http://localhost:5000/api';

export const searchPatterns = async (text, patterns) => {
  const response = await fetch(`${API_BASE}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, patterns })
  });
  if (!response.ok) {
    throw new Error('Failed to search patterns');
  }
  return response.json();
};

export const validateField = async (pattern, value) => {
  const response = await fetch(`${API_BASE}/validate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pattern, value })
  });
  if (!response.ok) {
    throw new Error('Failed to validate field');
  }
  return response.json();
};

export const validateForm = async (fields) => {
  const response = await fetch(`${API_BASE}/validate-form`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fields })
  });
  if (!response.ok) {
    throw new Error('Failed to validate form');
  }
  return response.json();
};

export const getPatterns = async () => {
  const response = await fetch(`${API_BASE}/patterns`);
  if (!response.ok) {
    throw new Error('Failed to fetch patterns');
  }
  return response.json();
};

export const healthCheck = async () => {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error('API is not available');
  }
  return response.json();
};