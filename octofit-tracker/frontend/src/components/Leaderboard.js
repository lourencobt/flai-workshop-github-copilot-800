import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
        console.log('Leaderboard - Fetching from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Leaderboard - Fetched data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard - Processed data:', leaderboardData);
        
        setLeaderboard(leaderboardData);
        setLoading(false);
      } catch (err) {
        console.error('Leaderboard - Error fetching data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) return <div className="container mt-4">Loading leaderboard...</div>;
  if (error) return <div className="container mt-4 alert alert-danger">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">🏆 Leaderboard</h2>
        <span className="badge bg-warning text-dark">{leaderboard.length} Competitors</span>
      </div>
      <div className="table-responsive">
        <table className="table table-hover align-middle">
          <thead className="table-warning">
            <tr>
              <th scope="col" className="text-center">🥇 Rank</th>
              <th scope="col">👤 User</th>
              <th scope="col">👥 Team</th>
              <th scope="col" className="text-center">⭐ Total Points</th>
              <th scope="col" className="text-center">📊 Activities</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length > 0 ? (
              leaderboard.map((entry, index) => (
                <tr key={entry.id} className={index < 3 ? 'table-active' : ''}>
                  <td className="text-center">
                    {index === 0 && <span className="badge bg-warning text-dark fs-6">🥇 1</span>}
                    {index === 1 && <span className="badge bg-secondary text-white fs-6">🥈 2</span>}
                    {index === 2 && <span className="badge bg-danger text-white fs-6">🥉 3</span>}
                    {index > 2 && <span className="badge bg-light text-dark border">{index + 1}</span>}
                  </td>
                  <td className="fw-bold">{entry.username || entry.user?.username || 'Unknown'}</td>
                  <td><span className="badge bg-info text-dark">{entry.user?.team_name || 'No Team'}</span></td>
                  <td className="text-center fw-bold text-warning">{entry.total_points}</td>
                  <td className="text-center">{entry.total_activities}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center text-muted py-4">No leaderboard data found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;
