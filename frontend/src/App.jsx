import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ExpenseListPage from './pages/ExpenseListPage';
import Header from './components/Header';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is authenticated on app load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <div className="app">
        <Header isAuthenticated={isAuthenticated} onLogout={handleLogout} />
        <main className="main-content">
          <Routes>
            <Route 
              path="/login" 
              element={!isAuthenticated ? <LoginPage onLogin={handleLogin} /> : <Navigate to="/expenses" />} 
            />
            <Route 
              path="/register" 
              element={!isAuthenticated ? <RegisterPage onRegister={handleLogin} /> : <Navigate to="/expenses" />} 
            />
            <Route 
              path="/expenses" 
              element={isAuthenticated ? <ExpenseListPage /> : <Navigate to="/login" />} 
            />
            <Route path="/" element={<Navigate to="/expenses" />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;