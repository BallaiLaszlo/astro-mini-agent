async function generate() {
  const message = document.getElementById("message").value.trim();
  const audience = document.getElementById("audience").value.trim();
  const tone = document.getElementById("tone").value.trim();
  const emojis = document.getElementById("emojis").value;

  const data = { message, audience, tone, emojis, regenerate: false };

  console.log("Generálás - küldöm a backendnek:", data);

  try {
    const response = await fetch('http://localhost:5000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    const resultDiv = document.getElementById("result");

    if (response.ok) {
      resultDiv.textContent = `Backend válasz: ${result.message}`;

      // Gomb szöveg és eseménykezelő csere
      const btn = document.getElementById("actionBtn");
      btn.textContent = "Újragenerálás";
      btn.removeEventListener("click", generateClickHandler);
      btn.addEventListener("click", regenerateClickHandler);
    } else {
      resultDiv.textContent = `Hiba: ${result.message || 'Ismeretlen hiba'}`;
    }
  } catch (error) {
    console.error('Hiba a kommunikáció során:', error);
    document.getElementById("result").textContent = "Nem sikerült kapcsolatot létesíteni a backenddel.";
  }
}

async function regenerate() {
  const message = document.getElementById("message").value.trim();
  const audience = document.getElementById("audience").value.trim();
  const tone = document.getElementById("tone").value.trim();
  const emojis = document.getElementById("emojis").value;

  const data = { message, audience, tone, emojis, regenerate: true };

  console.log("Újragenerálás - küldöm a backendnek:", data);

  try {
    const response = await fetch('http://localhost:5000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    const resultDiv = document.getElementById("result");

    if (response.ok) {
      resultDiv.textContent = `Backend válasz: ${result.message}`;
    } else {
      resultDiv.textContent = `Hiba: ${result.message || 'Ismeretlen hiba'}`;
    }
  } catch (error) {
    console.error('Hiba a kommunikáció során:', error);
    document.getElementById("result").textContent = "Nem sikerült kapcsolatot létesíteni a backenddel.";
  }
}

// Külön eseménykezelők, hogy könnyű legyen eltávolítani őket
const generateClickHandler = async (e) => {
  e.preventDefault();
  await generate();
};
const regenerateClickHandler = async (e) => {
  e.preventDefault();
  await regenerate();
};

// Esemény hozzárendelés az űrlap submit eseményére (az egy gomb miatt)
document.getElementById("postForm").addEventListener("submit", generateClickHandler);

// Így a gomb az űrlapon belül lesz, submitként működik, az első generálás elküldi az adatokat
