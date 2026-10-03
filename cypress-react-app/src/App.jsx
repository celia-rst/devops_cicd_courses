import { useState } from "react";
import { Login } from "./Login";
import { TodoList } from "./TodoList";

function App() {
  const [credentials, setCredentials] = useState(null);

  if (!credentials) {
    return (
      <Login
        onLoginSuccess={(email, password) =>
          setCredentials({ email, password })
        }
      />
    );
  }

  return <TodoList credentials={credentials} />;
}

export default App;