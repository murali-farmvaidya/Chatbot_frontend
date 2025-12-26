export async function speechToText(audioBlob) {
  const formData = new FormData();
  formData.append("file", audioBlob, "audio.webm");
  formData.append("language", "en");

  const res = await fetch("https://api.sarvam.ai/speech-to-text", {
    method: "POST",
    headers: {
      "api-subscription-key": import.meta.env.VITE_SARVAM_API_KEY
    },
    body: formData
  });

  const data = await res.json();
  console.log("📦 Sarvam raw response:", data);

  return data.text || data.transcript || "";
}
