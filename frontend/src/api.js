const API = import.meta.env.VITE_BACKEND_URL;

export function login(email, password) {
  return fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  }).then(async res => {
    if (!res.ok) {
      throw new Error("Login failed");
    }
    return res.json();
  });
}

export const googleLogin = (token) =>
  fetch(`${API}/auth/google`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token })
  }).then(async r => {
    if (!r.ok) {
      throw new Error("Google login failed");
    }
    return r.json();
  });

export const newSession = (token) =>
  fetch(`${API}/sessions/`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  }).then(async r => {
    if (r.status === 401) {
      localStorage.removeItem("access_token");
      throw new Error("Unauthorized");
    }
    if (!r.ok) {
      throw new Error("Failed to create session");
    }
    return r.json();
  });

export const sendMsg = (sessionId, message, token) =>
  fetch(`${API}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ session_id: sessionId, message })
  }).then(async r => {
    if (r.status === 401) {
      localStorage.removeItem("access_token");
      throw new Error("Unauthorized");
    }
    if (!r.ok) {
      throw new Error("Failed to send message");
    }
    return r.json();
  });

