import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
        console.log('Teams - Fetching from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Teams - Fetched data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams - Processed data:', teamsData);
        
        setTeams(teamsData);
        setLoading(false);
      } catch (err) {
        console.error('Teams - Error fetching data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) return <div className="container mt-4">Loading teams...</div>;
  if (error) return <div className="container mt-4 alert alert-danger">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">👥 Teams</h2>
        <span className="badge bg-success">{teams.length} Total Teams</span>
      </div>
      <div className="row">
        {teams.length > 0 ? (
          teams.map((team) => (
            <div key={team.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body">
                  <h5 className="card-title text-success fw-bold">{team.name}</h5>
                  <p className="card-text text-muted">{team.description}</p>
                  <ul className="list-group list-group-flush mt-3">
                    <li className="list-group-item border-0 px-0">
                      <strong>👤 Members:</strong> <span className="badge bg-primary rounded-pill">{team.member_count || 0}</span>
                    </li>
                    <li className="list-group-item border-0 px-0">
                      <strong>⭐ Total Points:</strong> <span className="badge bg-warning text-dark rounded-pill">{team.total_points || 0}</span>
                    </li>
                    <li className="list-group-item border-0 px-0">
                      <strong>📅 Created:</strong> <span className="text-muted">{new Date(team.created_at).toLocaleDateString()}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center">No teams found</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Teams;
