import React, { useState } from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  const location = useLocation();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const menuItems = [
    { path: '/', icon: '🏠', label: 'Home' },
    { path: '/users', icon: '👤', label: 'Users' },
    { path: '/teams', icon: '👥', label: 'Teams' },
    { path: '/activities', icon: '🏃', label: 'Activities' },
    { path: '/leaderboard', icon: '🏆', label: 'Leaderboard' },
    { path: '/workouts', icon: '💪', label: 'Workouts' }
  ];

  return (
    <div className="App">
      <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-header">
          <img src="/octofitapp-logo.png" alt="OctoFit" className="sidebar-logo" />
          {!isCollapsed && <span className="sidebar-title">OctoFit</span>}
        </div>
        
        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <Link 
              key={item.path}
              to={item.path} 
              className={`sidebar-item ${location.pathname === item.path ? 'active' : ''}`}
              title={item.label}
            >
              <span className="sidebar-icon">{item.icon}</span>
              {!isCollapsed && <span className="sidebar-label">{item.label}</span>}
            </Link>
          ))}
        </nav>

        <button 
          className="sidebar-toggle"
          onClick={() => setIsCollapsed(!isCollapsed)}
          aria-label="Toggle sidebar"
        >
          {isCollapsed ? '»' : '«'}
        </button>
      </aside>

      <main className="main-content">
        <Routes>
          <Route path="/" element={
            <div className="content-wrapper">
              <div className="welcome-section">
                <h1 className="display-title">Welcome to OctoFit Tracker</h1>
                <p className="subtitle">Track your fitness activities, compete with teams, and achieve your goals!</p>
                <div className="feature-grid">
                  <div className="feature-card">
                    <div className="feature-icon">🏃‍♂️</div>
                    <h3 className="feature-title">Track Activities</h3>
                    <p className="feature-text">Log your workouts and monitor your progress</p>
                  </div>
                  <div className="feature-card">
                    <div className="feature-icon">👥</div>
                    <h3 className="feature-title">Join Teams</h3>
                    <p className="feature-text">Collaborate and compete with your teammates</p>
                  </div>
                  <div className="feature-card">
                    <div className="feature-icon">🏆</div>
                    <h3 className="feature-title">Compete</h3>
                    <p className="feature-text">Climb the leaderboard and earn achievements</p>
                  </div>
                </div>
              </div>
            </div>
          } />
          <Route path="/users" element={<Users />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
