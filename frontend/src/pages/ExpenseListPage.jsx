import { useState, useEffect } from 'react';
import { expenseAPI } from '../api';
import { EXPENSE_CATEGORIES } from '../constants';
import AddExpenseModal from '../components/AddExpenseModal';
import './ExpenseListPage.css';

function ExpenseListPage() {
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState({
    total_count: 0,
    total_amount: 0,
    average_amount: 0
  });
  const [monthlySummary, setMonthlySummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  
  // Filter states
  const [filters, setFilters] = useState({
    title: '',
    min_amount: '',
    max_amount: '',
    description: '',
    category: '',
    start_date: '',
    end_date: ''
  });
  
  // Fetch expenses when component mounts
  useEffect(() => {
    fetchExpenses();
    fetchMonthlySummary();
  }, []);

  // Auto-dismiss the success message after a short delay
  useEffect(() => {
    if (!successMessage) return;
    const timer = setTimeout(() => setSuccessMessage(''), 4000);
    return () => clearTimeout(timer);
  }, [successMessage]);

  const fetchExpenses = async (additionalFilters = {}) => {
    try {
      setLoading(true);
      const response = await expenseAPI.getExpenses({
        ...filters,
        ...additionalFilters
      });
      setExpenses(response.expenses);
      setSummary(response.summary);
    } catch (err) {
      setError(err.message || 'Failed to fetch expenses');
    } finally {
      setLoading(false);
    }
  };

  const fetchMonthlySummary = async () => {
    try {
      const response = await expenseAPI.getMonthlySummary();
      setMonthlySummary(response.monthly_summary);
    } catch (err) {
      console.error('Failed to fetch monthly summary:', err.message);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const applyFilters = () => {
    fetchExpenses();
  };

  const clearFilters = () => {
    setFilters({
      title: '',
      min_amount: '',
      max_amount: '',
      description: '',
      category: '',
      start_date: '',
      end_date: ''
    });
    fetchExpenses({
      title: '',
      min_amount: '',
      max_amount: '',
      description: '',
      category: '',
      start_date: '',
      end_date: ''
    });
  };

  const deleteExpense = async (id) => {
    try {
      await expenseAPI.deleteExpense(id);
      // Refresh the list after deletion
      fetchExpenses();
      fetchMonthlySummary(); // Also refresh monthly summary
    } catch (err) {
      setError(err.message || 'Failed to delete expense');
    }
  };

  // Called by AddExpenseModal after a successful creation:
  // refreshes the list, totals, and monthly summaries without a page reload.
  const handleExpenseCreated = (created) => {
    setShowAddModal(false);
    setSuccessMessage(`Expense "${created.title}" added successfully.`);
    // Clear any previous filters that could hide the new expense from view
    // (e.g. a category/date filter active when the expense was added)
    setFilters({
      title: '',
      min_amount: '',
      max_amount: '',
      description: '',
      category: '',
      start_date: '',
      end_date: ''
    });
    fetchExpenses({
      title: '',
      min_amount: '',
      max_amount: '',
      description: '',
      category: '',
      start_date: '',
      end_date: ''
    });
    fetchMonthlySummary();
  };

  if (loading) {
    return <div className="expense-list-page">Loading expenses...</div>;
  }

  return (
    <div className="expense-list-page">
      <div className="expenses-header">
        <h2>My Expenses</h2>
        <div className="header-actions">
          <button
            className="add-expense-button"
            onClick={() => setShowAddModal(true)}
          >
            + Add Expense
          </button>
          <div className="summary-stats">
            <div className="stat-item">
              <span className="stat-label">Total Count:</span>
              <span className="stat-value">{summary.total_count}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Total Amount:</span>
              <span className="stat-value">${summary.total_amount.toFixed(2)}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Average Amount:</span>
              <span className="stat-value">${summary.average_amount.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </div>

      {successMessage && <div className="success-message">{successMessage}</div>}

      {/* Filters Section */}
      <div className="filters-section">
        <h3>Filter Expenses</h3>
        <div className="filter-grid">
          <div className="filter-item">
            <label>Title:</label>
            <input 
              type="text" 
              name="title" 
              value={filters.title} 
              onChange={handleFilterChange}
              placeholder="Title"
            />
          </div>
          
          <div className="filter-item">
            <label>Min Amount:</label>
            <input 
              type="number" 
              name="min_amount" 
              value={filters.min_amount} 
              onChange={handleFilterChange}
              placeholder="Min amount"
              step="0.01"
            />
          </div>
          
          <div className="filter-item">
            <label>Max Amount:</label>
            <input 
              type="number" 
              name="max_amount" 
              value={filters.max_amount} 
              onChange={handleFilterChange}
              placeholder="Max amount"
              step="0.01"
            />
          </div>
          
          <div className="filter-item">
            <label>Description:</label>
            <input 
              type="text" 
              name="description" 
              value={filters.description} 
              onChange={handleFilterChange}
              placeholder="Description"
            />
          </div>
          
          <div className="filter-item">
            <label>Category:</label>
            <input 
              type="text" 
              name="category" 
              value={filters.category} 
              onChange={handleFilterChange}
              placeholder="Category"
            />
          </div>
          
          <div className="filter-item">
            <label>Start Date:</label>
            <input 
              type="date" 
              name="start_date" 
              value={filters.start_date} 
              onChange={handleFilterChange}
            />
          </div>
          
          <div className="filter-item">
            <label>End Date:</label>
            <input 
              type="date" 
              name="end_date" 
              value={filters.end_date} 
              onChange={handleFilterChange}
            />
          </div>
        </div>
        
        <div className="filter-buttons">
          <button onClick={applyFilters}>Apply Filters</button>
          <button onClick={clearFilters}>Clear Filters</button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {/* Monthly Summary Section */}
      <div className="monthly-summary-section">
        <h3>Monthly Summary</h3>
        {monthlySummary.length > 0 ? (
          <div className="monthly-summary-grid">
            {monthlySummary.map((monthData) => (
              <div key={`${monthData.year}-${monthData.month}`} className="monthly-summary-item">
                <div className="month-year">
                  {new Date(monthData.year, monthData.month - 1).toLocaleString('default', { month: 'long' })} {monthData.year}
                </div>
                <div className="summary-stats">
                  <div className="stat-item">
                    <span className="stat-label">Count:</span>
                    <span className="stat-value">{monthData.count}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Total:</span>
                    <span className="stat-value">${monthData.total_amount.toFixed(2)}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Avg:</span>
                    <span className="stat-value">${monthData.average_amount.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No monthly summary data available.</p>
        )}
      </div>

      {expenses.length === 0 ? (
        <div className="no-expenses">
          <p>No expenses found. Add your first expense!</p>
        </div>
      ) : (
        <div className="expenses-list">
          {expenses.map(expense => (
            <div key={expense.id} className="expense-item">
              <div className="expense-header">
                <div className="expense-title">{expense.title}</div>
                <button 
                  className="delete-button"
                  onClick={() => deleteExpense(expense.id)}
                >
                  Delete
                </button>
              </div>
              <div className="expense-details">
                <span className="expense-amount">${expense.amount.toFixed(2)}</span>
                {expense.category && (
                  <span className="expense-category">Category: {expense.category}</span>
                )}
                {expense.expense_date && (
                  <span className="expense-date">Date: {new Date(expense.expense_date).toLocaleDateString()}</span>
                )}
                {expense.description && (
                  <span className="expense-description">{expense.description}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Expense modal */}
      {showAddModal && (
        <AddExpenseModal
          onClose={() => setShowAddModal(false)}
          onCreated={handleExpenseCreated}
        />
      )}
    </div>
  );
}

export default ExpenseListPage;