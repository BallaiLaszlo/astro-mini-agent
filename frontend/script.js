document.getElementById("postForm").addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = document.getElementById("message").value.trim();
  const audience = document.getElementById("audience").value.trim();
  const tone = document.getElementById("tone").value.trim();
  const emojis = document.getElementById("emojis").value;

  console.log("Küldöm a backendnek:", { message, audience, tone, emojis });

  try {
    const response = await fetch('http://localhost:5000/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, audience, tone, emojis }),
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
});
