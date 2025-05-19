// script.js
document.getElementById("postForm").addEventListener("submit", async e => {
  e.preventDefault();

  const message  = document.getElementById("message").value.trim();
  const audience = document.getElementById("audience").value.trim();
  const tone     = document.getElementById("tone").value.trim();
  // select.value adja vissza a "true"/"false" stringet
  const emojis   = document.getElementById("emojis").value === "true";

  const payload = { message, audience, tone, emojis };

  try {
    const resp = await fetch("http://localhost:5000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();
    const container = document.getElementById("result");
    container.innerHTML = "";

    if (!resp.ok || data.error) {
      container.textContent = `Hiba: ${data.error || resp.statusText}`;
      return;
    }

    ["facebook","instagram","linkedin","x"].forEach(platform => {
      const h3 = document.createElement("h3");
      h3.textContent = platform.charAt(0).toUpperCase() + platform.slice(1);
      const p = document.createElement("p");
      p.textContent = data[platform] || "Nincs adat";
      container.append(h3, p);
    });

  } catch (err) {
    console.error("Kommunikációs hiba:", err);
    document.getElementById("result").textContent = "Nem sikerült kapcsolódni a szerverhez.";
  }
});
