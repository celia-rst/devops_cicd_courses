import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000/api/tasks/";

// On reçoit les identifiants en props pour prouver à Django qu'on a le droit d'accéder
export const TodoList = ({ credentials }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [newTask, setNewTask] = useState("");

  // Configuration Axios pour envoyer l'authentification Basic à Django
  const axiosConfig = {
    auth: { username: credentials.email, password: credentials.password },
  };

  useEffect(() => {
    axios
      .get(API_URL, axiosConfig)
      .then((response) => {
        setTasks(response.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Impossible de charger les tâches.");
        setLoading(false);
      });
  }, []);

  const handleAddTask = () => {
    axios
      .post(API_URL, { title: newTask }, axiosConfig)
      .then((response) => {
        setTasks([...tasks, response.data]);
        setNewTask("");
      })
      .catch(() => alert("Erreur lors de l'ajout de la tâche"));
  };

  if (loading) return <p data-cy="loading-state">Chargement...</p>;
  if (error) return <p data-cy="error-state">{error}</p>;

  return (
    <div data-cy="app-view">
      <h1>Ma To-Do List</h1>
      <div>
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          aria-label="Nouvelle tâche"
          data-cy="new-task-input"
        />
        <button onClick={handleAddTask} data-cy="add-task-button">
          Ajouter
        </button>
      </div>
      <ul data-cy="task-list">
        {tasks.map((task) => (
          <li key={task.id} data-cy={`task-${task.title.replace(/\s+/g, "-")}`}>
            {task.title}
          </li>
        ))}
      </ul>
    </div>
  );
};