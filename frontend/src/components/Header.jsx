import './Header.css';

function Header({ isAuthenticated, onLogout }) {
  return (
    <header className="header">
      <div className="header-content">
        <h1>Expense Tracker</h1>
        {isAuthenticated && (
          <nav className="nav">
            <button onClick={onLogout} className="logout-button">Logout</button>
          </nav>
        )}
      </div>
    </header>
  );
}

export default Header;