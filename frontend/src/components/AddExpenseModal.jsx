import { useState } from 'react';
import { expenseAPI } from '../api';
import { EXPENSE_CATEGORIES } from '../constants';
import './AddExpenseModal.css';

// Returns YYYY-MM-DD for "today" in the local timezone
function todayISO() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

const EMPTY_FORM = {
  title: '',
  amount: '',
  category: '',
  expense_date: null, // filled with today's date on open
  description: '',
};

function AddExpenseModal({ onClose, onCreated }) {
  const [form, setForm] = useState({ ...EMPTY_FORM, expense_date: todayISO() });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Client-side amount validation: numeric, non-zero, non-negative
    const amount = Number(form.amount);
    if (form.amount === '' || Number.isNaN(amount)) {
      setError('Please enter a valid amount.');
      return;
    }
    if (amount <= 0) {
      setError('Amount must be greater than 0.');
      return;
    }

    setIsSubmitting(true);
    try {
      const created = await expenseAPI.createExpense({
        title: form.title,
        amount: amount,
        category: form.category || null,
        expense_date: form.expense_date || null,
        description: form.description || null,
      });
      onCreated(created);
    } catch (err) {
      setError(err.message || 'Failed to add expense');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Add Expense</h3>
          <button
            type="button"
            className="modal-close"
            onClick={onClose}
            aria-label="Close"
          >
            ×
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="add-expense-form">
          <div className="form-group">
            <label htmlFor="expense-title">Title:</label>
            <input
              type="text"
              id="expense-title"
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="e.g. Grocery shopping"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="expense-amount">Amount:</label>
            <input
              type="number"
              id="expense-amount"
              name="amount"
              value={form.amount}
              onChange={handleChange}
              placeholder="0.00"
              step="0.01"
              min="0.01"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="expense-category">Category:</label>
            <select
              id="expense-category"
              name="category"
              value={form.category}
              onChange={handleChange}
            >
              <option value="">None</option>
              {EXPENSE_CATEGORIES.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="expense-date">Date:</label>
            <input
              type="date"
              id="expense-date"
              name="expense_date"
              value={form.expense_date}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="expense-description">Description (optional):</label>
            <textarea
              id="expense-description"
              name="description"
              value={form.description}
              onChange={handleChange}
              placeholder="Additional details"
              rows="3"
            />
          </div>

          <div className="modal-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="primary-button"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Saving...' : 'Add Expense'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddExpenseModal;
