import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const baseUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api`;
        
        // Fetch users and teams in parallel
        const [usersResponse, teamsResponse] = await Promise.all([
          fetch(`${baseUrl}/users/`),
          fetch(`${baseUrl}/teams/`)
        ]);
        
        if (!usersResponse.ok || !teamsResponse.ok) {
          throw new Error('Failed to fetch data');
        }
        
        const usersData = await usersResponse.json();
        const teamsData = await teamsResponse.json();
        
        // Handle both paginated (.results) and plain array responses
        setUsers(usersData.results || usersData);
        setTeams(teamsData.results || teamsData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="container mt-4">Loading users...</div>;
  if (error) return <div className="container mt-4 alert alert-danger">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">👤 Users</h2>
        <span className="badge bg-primary">{users.length} Total Users</span>
      </div>
      
      {users.length > 0 ? (
        <div className="card shadow-sm">
          <div className="card-body">
            <div className="table-responsive">
              <table className="table table-hover align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th>Username</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Team</th>
                    <th>Joined</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id}>
                      <td>
                        <strong className="text-primary">{user.username}</strong>
                      </td>
                      <td>{user.first_name} {user.last_name}</td>
                      <td>
                        <small className="text-muted">{user.email}</small>
                      </td>
                      <td>
                        {user.team_name ? (
                          <span className="badge bg-success">{user.team_name}</span>
                        ) : (
                          <span className="badge bg-secondary">No Team</span>
                        )}
                      </td>
                      <td>
                        <small>{new Date(user.date_joined).toLocaleDateString()}</small>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        <div className="alert alert-info text-center">No users found</div>
      )}
    </div>
  );
};

export default Users;
