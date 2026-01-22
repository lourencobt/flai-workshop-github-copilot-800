import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
        console.log('Users - Fetching from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Users - Fetched data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const usersData = data.results || data;
        console.log('Users - Processed data:', usersData);
        
        setUsers(usersData);
        setLoading(false);
      } catch (err) {
        console.error('Users - Error fetching data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <div className="container mt-4">Loading users...</div>;
  if (error) return <div className="container mt-4 alert alert-danger">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">👤 Users</h2>
        <span className="badge bg-primary">{users.length} Total Users</span>
      </div>
      <div className="row">
        {users.length > 0 ? (
          users.map((user) => (
            <div key={user.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body">
                  <h5 className="card-title text-primary fw-bold">{user.username}</h5>
                  <ul className="list-group list-group-flush mt-3">
                    <li className="list-group-item border-0 px-0">
                      <strong>📧 Email:</strong> <span className="text-muted">{user.email}</span>
                    </li>
                    <li className="list-group-item border-0 px-0">
                      <strong>👥 Team:</strong> <span className="text-muted">{user.team_name || 'No team'}</span>
                    </li>
                    <li className="list-group-item border-0 px-0">
                      <strong>🎯 Fitness Goal:</strong> <span className="text-muted">{user.fitness_goal || 'Not set'}</span>
                    </li>
                    <li className="list-group-item border-0 px-0">
                      <strong>📅 Joined:</strong> <span className="text-muted">{new Date(user.date_joined).toLocaleDateString()}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center">No users found</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Users;
