import { Login } from "./pages/Login.tsx";
import { AuthClient } from "./services/AuthClient.ts";
import "./App.css";

function App() {
  const authClient = new AuthClient();
  return <Login authClient={authClient} />;
}

export default App;
