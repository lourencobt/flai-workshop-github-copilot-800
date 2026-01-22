import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            <img src="/octofitapp-logo.png" alt="OctoFit Logo" className="navbar-logo" />
            OctoFit Tracker
          </Link>
          <button 
            className="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarNav" 
            aria-controls="navbarNav" 
            aria-expanded="false" 
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link" to="/users">Users</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/teams">Teams</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/activities">Activities</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/workouts">Workouts</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={
          <div className="container mt-4">
            <div className="welcome-section">
              <h1 className="display-3 fw-bold">Welcome to OctoFit Tracker</h1>
              <p className="lead">Track your fitness activities, compete with teams, and achieve your goals!</p>
              <div className="mt-4">
                <div className="row text-center">
                  <div className="col-md-4 mb-3">
                    <div className="card border-0 shadow-sm h-100">
                      <div className="card-body">
                        <h3 className="text-primary">🏃‍♂️</h3>
                        <h5 className="card-title">Track Activities</h5>
                        <p className="card-text">Log your workouts and monitor your progress</p>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-4 mb-3">
                    <div className="card border-0 shadow-sm h-100">
                      <div className="card-body">
                        <h3 className="text-success">👥</h3>
                        <h5 className="card-title">Join Teams</h5>
                        <p className="card-text">Collaborate and compete with your teammates</p>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-4 mb-3">
                    <div className="card border-0 shadow-sm h-100">
                      <div className="card-body">
                        <h3 className="text-warning">🏆</h3>
                        <h5 className="card-title">Compete</h5>
                        <p className="card-text">Climb the leaderboard and earn achievements</p>
                      </div>
                    </div>
                  </div>
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
    </div>
  );
}

export default App;
