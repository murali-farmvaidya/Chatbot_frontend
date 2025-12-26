import { useEffect, useState, useRef } from "react";
import { speechToText } from "./stt";

export default function Chat({ token, sessionId, setActiveSession, onMessageSent }) {
  const [messages, setMessages] = useState([]);
  const [msg, setMsg] = useState("");
  const [sending, setSending] = useState(false);
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  // 🔹 Load history when session changes
  useEffect(() => {
    if (sessionId && sessionId !== "NEW") {
      fetch(`${import.meta.env.VITE_BACKEND_URL}/messages/${sessionId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(r => {
          if (!r.ok) return [];
          return r.json();
        })
        .then(data => {
          if (Array.isArray(data)) {
            setMessages(data);
          } else {
            setMessages([]);
          }
        })
        .catch(() => setMessages([]));
    } else if (sessionId === "NEW") {
      // New chat
      setMessages([]);
    }
  }, [sessionId, token]);

  async function send() {
    if (!msg.trim() || sending) return;

    setSending(true);

    try {
      let activeSid = sessionId;

      if (!activeSid || activeSid === "NEW") {
        const s = await fetch(`${import.meta.env.VITE_BACKEND_URL}/sessions/`, {
          method: "POST",
          headers: { Authorization: `Bearer ${token}` }
        }).then(r => r.json());

        activeSid = s.session_id;
        setActiveSession(activeSid);
      }

      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          session_id: activeSid,
          message: msg
        })
      }).then(r => r.json());

      await fetch(`${import.meta.env.VITE_BACKEND_URL}/messages/${activeSid}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(r => r.json())
        .then(setMessages);

      onMessageSent();

      setMsg("");
    } finally {
      setSending(false);
    }
  }

  async function startRecording() {
    console.log("🎤 Start recording");

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    chunksRef.current = [];
    mediaRecorderRef.current = mediaRecorder;

    mediaRecorder.ondataavailable = e => {
      console.log("🎧 Audio chunk size:", e.data.size);
      if (e.data.size > 0) chunksRef.current.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      console.log("🛑 Recording stopped");

      const audioBlob = new Blob(chunksRef.current, { type: "audio/webm" });
      console.log("📦 Audio blob size:", audioBlob.size);

      if (audioBlob.size === 0) {
        console.warn("❌ Empty audio blob");
        return;
      }

      try {
        console.log("📤 Sending audio to Sarvam...");
        const text = await speechToText(audioBlob);
        console.log("📝 STT text:", text);

        if (text) {
          setMsg(text);   // 👈 THIS IS THE IMPORTANT LINE
        } else {
          console.warn("⚠️ No text returned from STT");
        }
      } catch (e) {
        console.error("❌ STT failed:", e);
      }
    };

    mediaRecorder.start();
    setRecording(true);
  }

  function stopRecording() {
    console.log("⏹ Stop recording");
    mediaRecorderRef.current.stop();
    setRecording(false);
  }

  return (
    <>
      <div style={{ height: "80vh", overflowY: "auto", border: "1px solid #ccc" }}>
        {messages.map((m, i) => (
          <p key={i}>
            <b>{m.role}:</b> {m.content}
          </p>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={msg}
          onChange={e => setMsg(e.target.value)}
          placeholder="Type or speak your question"
          style={{ flex: 1 }}
        />

        <button
          onClick={recording ? stopRecording : startRecording}
          style={{
            background: recording ? "red" : "#4CAF50",
            color: "white"
          }}
        >
          🎤
        </button>

        <button onClick={send} disabled={sending}>
          {sending ? "Sending..." : "Send"}
        </button>
      </div>

      {recording && <p style={{ color: "red" }}>🎙 Listening...</p>}

      {!recording && msg && (
        <p style={{ color: "green" }}>📝 Voice converted to text</p>
      )}
    </>
  );
}
