// Determine API base from global env (for simple static frontend) or default to localhost:8000
const API_BASE = (window.__env && window.__env.VITE_API_URL) || 'http://127.0.0.1:8000';

async function search() {
  const q = document.getElementById("search").value;
  const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(q)}`);
  const data = await res.json();
  document.getElementById("results").innerHTML = data.results
    .map(d => `<div><h3>${d.title}</h3><p>${d.description}</p></div>`)
    .join("");
}

