import { useState, useEffect } from "react";
import Login from "./Login";
import Chat from "./Chat";
import Sidebar from "./Sidebar";
import Profile from "./Profile";

export default function App() {
  const [token, setToken] = useState(null);
  const [activeSession, setActiveSession] = useState(null);
  const [view, setView] = useState("chat"); // chat | profile
  const [refreshSessions, setRefreshSessions] = useState(0);

  useEffect(() => {
    const savedToken = localStorage.getItem("access_token");
    const lastSession = localStorage.getItem("active_session");

    if (savedToken) setToken(savedToken);
    if (lastSession) setActiveSession(lastSession);
  }, []);

  useEffect(() => {
    if (activeSession) {
      localStorage.setItem("active_session", activeSession);
    }
  }, [activeSession]);

  const handleLoginSuccess = (token) => {
    localStorage.setItem("access_token", token);
    setToken(token);
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setActiveSession(null);
  };

  if (!token) return <Login onLoginSuccess={handleLoginSuccess} />;

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      <Sidebar
        token={token}
        activeSession={activeSession}
        setActiveSession={setActiveSession}
        refreshSessions={refreshSessions}
        onNewChat={() => {
          localStorage.removeItem("active_session");
          setActiveSession("NEW");
          setView("chat");
        }}
        onProfile={() => setView("profile")}
        onLogout={handleLogout}
      />

      <div style={{ flex: 1, padding: 10 }}>
        {view === "profile" ? (
          <Profile setView={setView} />
        ) : (
          <Chat
            token={token}
            sessionId={activeSession}
            setActiveSession={setActiveSession}
            onMessageSent={() => setRefreshSessions(x => x + 1)}
          />
        )}
      </div>
    </div>
  );
}
