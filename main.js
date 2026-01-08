import './style.css';

let form = document.querySelector('form');
let promptInput = document.querySelector('input[name="prompt"]');
let output = document.querySelector('.output');

form.onsubmit = async (e) => {
  e.preventDefault();
  output.textContent = "Analyzing symptoms...";

  try {
    const res = await fetch("https://medvocal.onrender.com/api/triage", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: promptInput.value })
    });

    const data = await res.json();
    output.textContent = data.result;
  } catch (err) {
    output.textContent = "Server error. Please try again.";
  }
};
