import { useEffect, useState } from "react";

export default function Sidebar({
  token,
  activeSession,
  setActiveSession,
    refreshSessions,
  onNewChat,
  onProfile,
  onLogout
}) {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_URL}/sessions/`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(r => r.json())
      .then(setSessions);
    }, [token, refreshSessions]);

  async function deleteSession(id) {
    await fetch(`${import.meta.env.VITE_BACKEND_URL}/sessions/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    });
    setSessions(s => s.filter(x => x.id !== id));
  }

  return (
    <div style={{ width: 250, borderRight: "1px solid #ccc", padding: 10 }}>
      <button onClick={onNewChat}>➕ New Chat</button>
      <button onClick={onProfile}>👤 Profile</button>
      <button onClick={onLogout}>🚪 Logout</button>

      <hr />

      {sessions.map(s => (
        <div key={s.id}>
          <button
            onClick={() => setActiveSession(s.id)}
            style={{
              fontWeight: s.id === activeSession ? "bold" : "normal"
            }}
          >
            {s.title || "Chat"}
          </button>
          <button onClick={() => deleteSession(s.id)}>❌</button>
        </div>
      ))}
    </div>
  );
}
