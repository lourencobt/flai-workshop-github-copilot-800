import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
        console.log('Workouts - Fetching from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Workouts - Fetched data:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts - Processed data:', workoutsData);
        
        setWorkouts(workoutsData);
        setLoading(false);
      } catch (err) {
        console.error('Workouts - Error fetching data:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) return <div className="container mt-4">Loading workouts...</div>;
  if (error) return <div className="container mt-4 alert alert-danger">Error: {error}</div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">💪 Recommended Workouts</h2>
        <span className="badge bg-danger">{workouts.length} Workouts Available</span>
      </div>
      <div className="row">
        {workouts.length > 0 ? (
          workouts.map((workout) => (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100 border-0 shadow-sm">
                <div className="card-body">
                  <h5 className="card-title text-danger fw-bold">{workout.name}</h5>
                  <p className="card-text text-muted">{workout.description}</p>
                  <ul className="list-group list-group-flush mt-3">
                    <li className="list-group-item border-0 px-0">
                      <strong>🏋️ Type:</strong> <span className="badge bg-primary">{workout.workout_type}</span>
                    </li>
                    <li className="list-group-item border-0 px-0">
                      <strong>⏱️ Duration:</strong> <span className="text-muted">{workout.duration} minutes</span>
                    </li>
                    <li className="list-group-item border-0 px-0">
                      <strong>📊 Difficulty:</strong> <span className={`badge ${
                        workout.difficulty_level === 'beginner' ? 'bg-success' :
                        workout.difficulty_level === 'intermediate' ? 'bg-warning text-dark' :
                        'bg-danger'
                      }`}>{workout.difficulty_level}</span>
                    </li>
                    <li className="list-group-item border-0 px-0">
                      <strong>🔥 Calories:</strong> <span className="text-danger fw-bold">{workout.calories_target}</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center">No workouts found</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Workouts;
