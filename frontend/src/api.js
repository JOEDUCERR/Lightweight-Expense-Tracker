// API client for communicating with the Expense Tracker backend
// Using relative paths so Vite proxy works correctly
const API_BASE_URL = '/api';

// Helper function to make API requests
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // Add default headers
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // If we have a token, add it to the Authorization header
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(formatApiError(response.status, errorData));
    }

    return await response.json();
  } catch (error) {
    // Network failure (fetch rejects with a TypeError when the server
    // is unreachable, the connection drops, or CORS blocks the request)
    if (error instanceof TypeError && !error.message.startsWith('HTTP')) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw new Error('Network error: could not reach the server. Please try again.');
    }
    throw error;
  }
}

// Convert a FastAPI error response into a readable message.
// Handles: validation error arrays, plain string details, and entirely
// unexpected response bodies.
function formatApiError(status, errorData) {
  const prefix = `HTTP error ${status}`;

  // No parseable JSON body (or empty) -> generic readable message
  if (!errorData) {
    return `${prefix}`;
  }

  const detail = errorData.detail;

  // FastAPI validation errors: detail is an array of error objects
  if (Array.isArray(detail)) {
    const messages = detail
      .map(item => {
        const field = item.loc && item.loc.length > 1 ? item.loc[item.loc.length - 1] : null;
        const fieldLabel = field
          ? field.charAt(0).toUpperCase() + field.slice(1)
          : null;
        return fieldLabel ? `${fieldLabel}: ${item.msg}` : item.msg || prefix;
      });
    return messages.join('\n') || prefix;
  }

  // Plain string detail (e.g. "Username already registered")
  if (typeof detail === 'string' && detail.length > 0) {
    return detail;
  }

  // Unexpected shapes (objects/numbers etc.)
  if (detail != null && typeof detail !== 'object') {
    return String(detail);
  }
  if (errorData.message && typeof errorData.message === 'string') {
    return errorData.message;
  }

  return prefix;
}

// Auth endpoints
export const authAPI = {
  // Register a new user
  async register(userData) {
    return apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  // Login an existing user
  // The backend login endpoint expects a JSON body: { username, password }
  // (see backend/app/routers/auth.py -> LoginRequest)
  async login(credentials) {
    return apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({
        username: credentials.username,
        password: credentials.password,
      }),
    });
  },
};

// Expense endpoints
export const expenseAPI = {
  // Get all expenses for the current user
  async getExpenses(params = {}) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      // Skip empty values entirely: empty strings for numeric/date filters
      // (e.g. "min_amount=") fail backend validation with a 422
      if (value !== null && value !== undefined && value !== '') {
        searchParams.append(key, value);
      }
    });
    
    const queryString = searchParams.toString();
    // Collection endpoints are registered as "/api/expenses/" (with trailing
    // slash). Calling "/api/expenses" would trigger FastAPI's 307 redirect,
    // whose absolute Location header is cross-origin through the Vite proxy,
    // causing fetch() to strip the Authorization header.
    const endpoint = queryString ? `/expenses/?${queryString}` : '/expenses/';
    
    return apiRequest(endpoint);
  },

  // Get monthly summary
  async getMonthlySummary(params = {}) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      // Skip empty values: empty numeric/date params fail backend validation
      if (value !== null && value !== undefined && value !== '') {
        searchParams.append(key, value);
      }
    });
    
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/expenses/monthly-summary?${queryString}` : '/expenses/monthly-summary';
    
    return apiRequest(endpoint);
  },

  // Get a specific expense by ID
  async getExpense(id) {
    return apiRequest(`/expenses/${id}`);
  },

  // Create a new expense
  // Note the trailing slash: the backend route is "/api/expenses/"
  async createExpense(expenseData) {
    return apiRequest('/expenses/', {
      method: 'POST',
      body: JSON.stringify(expenseData),
    });
  },

  // Update an existing expense
  async updateExpense(id, expenseData) {
    return apiRequest(`/expenses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(expenseData),
    });
  },

  // Delete an expense
  async deleteExpense(id) {
    return apiRequest(`/expenses/${id}`, {
      method: 'DELETE',
    });
  },
};