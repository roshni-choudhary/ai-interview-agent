const API_BASE = '/api';

const getHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

const handleResponse = async (response) => {
  if (response.status === 401) {
    localStorage.removeItem('token');
    window.location.href = '/login';
    throw new Error('Unauthorized session. Please login again.');
  }
  
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'An unexpected request error occurred.');
  }
  return data;
};

export const authApi = {
  register: async (username, email, password) => {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password })
    });
    return handleResponse(res);
  },
  
  login: async (username, password) => {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await handleResponse(res);
    if (data.access_token) {
      localStorage.setItem('token', data.access_token);
    }
    return data;
  },

  getMe: async () => {
    const res = await fetch(`${API_BASE}/auth/me`, {
      method: 'GET',
      headers: getHeaders()
    });
    return handleResponse(res);
  }
};

export const interviewApi = {
  start: async (topics, difficulty) => {
    const res = await fetch(`${API_BASE}/interview/start`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ topics, difficulty })
    });
    return handleResponse(res);
  },

  getSession: async (sessionId) => {
    const res = await fetch(`${API_BASE}/interview/${sessionId}`, {
      method: 'GET',
      headers: getHeaders()
    });
    return handleResponse(res);
  },

  sendMessage: async (sessionId, content, messageType = 'chat') => {
    const res = await fetch(`${API_BASE}/interview/${sessionId}/message`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ content, message_type: messageType })
    });
    return handleResponse(res);
  },

  submitCode: async (sessionId, code, language) => {
    const res = await fetch(`${API_BASE}/interview/${sessionId}/submit`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ code, language })
    });
    return handleResponse(res);
  },

  requestHint: async (sessionId) => {
    const res = await fetch(`${API_BASE}/interview/${sessionId}/hint`, {
      method: 'POST',
      headers: getHeaders()
    });
    return handleResponse(res);
  },

  endSession: async (sessionId) => {
    const res = await fetch(`${API_BASE}/interview/${sessionId}/end`, {
      method: 'POST',
      headers: getHeaders()
    });
    return handleResponse(res);
  }
};

export const progressApi = {
  getProgress: async () => {
    const res = await fetch(`${API_BASE}/progress`, {
      method: 'GET',
      headers: getHeaders()
    });
    return handleResponse(res);
  },

  getDashboard: async () => {
    const res = await fetch(`${API_BASE}/progress/dashboard`, {
      method: 'GET',
      headers: getHeaders()
    });
    return handleResponse(res);
  }
};
