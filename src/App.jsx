import { useState } from "react";
import axios from "axios";

const API = "https://medvocal.onrender.com";

export default function App() {
  const [listening, setListening] = useState(false);
  const [spoken, setSpoken] = useState("");
  const [result, setResult] = useState(null);

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  const startListening = () => {
    const recog = new SpeechRecognition();
    recog.lang = "en-IN";
    recog.continuous = false;
    recog.interimResults = false;

    recog.onstart = () => setListening(true);
    recog.onend = () => setListening(false);

    recog.onresult = (event) => {
      const text = event.results[0][0].transcript;
      setSpoken(text);

      axios.post(`${API}/triage`, { text })
        .then(res => {
          const data = JSON.parse(res.data.result);
          setResult(data);
        })
        .catch(err => {
          console.error(err);
          alert("Backend not reachable");
        });
    };

    recog.start();
  };

  return (
    <div className="app">
      <h1>Med-Vocal Emergency Desk</h1>

      <button onClick={startListening} className="btn">
        {listening ? "Listening..." : "🎤 Speak Symptoms"}
      </button>

      {spoken && <p><b>You said:</b> {spoken}</p>}

      {result && (
        <div className={`card ${result.severity}`}>
          <h2>{result.severity} EMERGENCY</h2>
          <p><b>Clinical Reason:</b> {result.reason}</p>
          <ul>
            {result.action.split(".").map((x, i) => x && <li key={i}>{x}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
