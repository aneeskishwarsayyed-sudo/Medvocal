import { useState } from "react";
import axios from "axios";

const API = "https://medvocal-1--api-7vtpvxhi.web.app";

export default function App() {
  const [listening,setListening] = useState(false);
  const [spoken,setSpoken] = useState("");
  const [result,setResult] = useState(null);

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  const start = () => {
    const r = new SR();
    r.lang="en-IN";
    r.onstart=()=>setListening(true);
    r.onend=()=>setListening(false);
    r.onresult = e => {
      const text = e.results[0][0].transcript;
      setSpoken(text);
      axios.post(API+"/triage",{text}).then(res=>{
        setResult(JSON.parse(res.data.result));
      });
    };
    r.start();
  };

  return (
    <div className="app">
      <h1>Med-Vocal Emergency Desk</h1>
      <button onClick={start}>{listening?"Listening...":"🎤 Speak Symptoms"}</button>
      {spoken && <p>You said: {spoken}</p>}
      {result && (
        <div className={result.severity}>
          <h2>{result.severity} EMERGENCY</h2>
          <p>{result.reason}</p>
          <ul>{result.action.split(".").map((x,i)=><li key={i}>{x}</li>)}</ul>
        </div>
      )}
    </div>
  );
}
