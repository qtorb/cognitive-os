import { useState, useEffect } from 'react';
import Login from './components/Login';
import Onboarding from './components/Onboarding';
import Dashboard from './components/Dashboard';

function App() {
  const [token, setToken] = useState(null);
  const [user, setUser] = useState(null);
  const [page, setPage] = useState('login'); // login, onboarding, dashboard

  useEffect(() => {
    // Check if token exists in localStorage
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (savedToken && savedUser) {
      setToken(savedToken);
      const parsedUser = JSON.parse(savedUser);
      setUser(parsedUser);

      // Determine which page to show
      if (parsedUser.onboarded) {
        setPage('dashboard');
      } else {
        setPage('onboarding');
      }
    } else {
      setPage('login');
    }
  }, []);

  const handleLoginSuccess = (loginData) => {
    setToken(loginData.token);
    setUser({
      user_id: loginData.user_id,
      email: loginData.email,
      name: loginData.name,
      onboarded: loginData.onboarded
    });

    if (loginData.onboarded) {
      setPage('dashboard');
    } else {
      setPage('onboarding');
    }
  };

  const handleOnboardingComplete = () => {
    // Update user as onboarded
    const updatedUser = { ...user, onboarded: true };
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
    setPage('dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    setPage('login');
  };

  return (
    <div className="app">
      {page === 'login' && (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}

      {page === 'onboarding' && token && (
        <Onboarding token={token} onComplete={handleOnboardingComplete} />
      )}

      {page === 'dashboard' && token && user && (
        <Dashboard token={token} user={user} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;
