async function search() {
  const q = document.getElementById("search").value;
  const res = await fetch(`http://127.0.0.1:8000/search?q=${encodeURIComponent(q)}`);
  const data = await res.json();
  document.getElementById("results").innerHTML = data.results
    .map(d => `<div><h3>${d.title}</h3><p>${d.description}</p></div>`)
    .join("");
}

