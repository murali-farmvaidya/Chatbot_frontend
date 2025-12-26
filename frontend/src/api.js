const API = import.meta.env.VITE_BACKEND_URL;

export function login(email, password) {
  return fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  }).then(res => res.json());
}

export const googleLogin = (token) =>
  fetch(`${API}/auth/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token })
  }).then(r => r.json());

export const newSession = (token) =>
  fetch(`${API}/sessions/`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  }).then(r => r.json());

export const sendMsg = (sessionId, message, token) =>
  fetch(`${API}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ session_id: sessionId, message })
  }).then(r => r.json());
