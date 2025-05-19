import os
import json
import logging
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from cohere import ClientV2
from dotenv import load_dotenv

# Betöltjük a .env-et a projekt gyökérkönyvtárból
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY nincs beállítva a .env fájlban")

# Flask app és CORS
app = Flask(__name__)
CORS(app)

# Logolás beállítása
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(BASE_DIR, 'app.log'), encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Cohere kliens inicializálása
client = ClientV2(api_key=COHERE_API_KEY)

def strip_emojis(text: str) -> str:
    """
    Eltávolítja az összes Unicode emoji karaktert a szövegből.

    Paraméterek:
        text (str): A bemeneti szöveg, amelyből el kell távolítani az emojikat.

    Visszatér:
        str: A megtisztított szöveg emojik nélkül.
    """
    pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE)
    return pattern.sub(r'', text)

# AI generáló függvény
def generate_ai_message(message, audience, tone, use_emojis):
    """
    Meghívja a Cohere AI-t, hogy egy marketing kampányüzenetből több közösségi média posztot generáljon
    különböző platformokra (Facebook, Instagram, LinkedIn, X), magyar nyelven.

    Paraméterek:
        message (str): A marketing kampányüzenet.
        audience (str): A célközönség megnevezése.
        tone (str): A kívánt hangnem (pl. barátságos, szakmai, stb.).
        use_emojis (bool): Emojik használatának engedélyezése vagy tiltása.

    Visszatér:
        dict: A generált posztokat tartalmazó szótár, vagy hibaüzenet egy hiba esetén.
            Példa:
            {
                "facebook": "szöveg",
                "instagram": "szöveg",
                "linkedin": "szöveg",
                "x": "szöveg"
            }
            vagy hiba esetén:
            {
                "error": "Hibás formátumú AI válasz",
                "raw_response": "...",
                "debug_prompt": "..."
            }
    """
    logging.info("Elkezdem meghívni a Cohere API-t...")
    prompt = f"""
    Kérlek generálj közösségi média posztokat magyar nyelven KIZÁRÓLAG JSON formátumban!
    Kimeneti struktúra:
    {{
    "facebook": "szöveg",
    "instagram": "szöveg",
    "linkedin": "szöveg",
    "x": "szöveg"
    }}

    Bemeneti paraméterek:
    - Kampányüzenet: {message}
    - Célközönség: {audience}
    - Hangnem: {tone}
    - Emojik használata: {'igen' if use_emojis else 'nem'}

    FIGYELEM! Csak tiszta JSON válasz megengedett, semmilyen egyéb szöveg nem lehet a válaszban!
    """
    try:
        response = client.chat(
            model="command-xlarge-nightly",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7
        )
    except Exception as e:
        logging.error(f"Cohere API hiba: {str(e)}", exc_info=True)  # ⬅️ Részletesebb log
        return {"error": "AI szolgáltatás elérhetetlen."}

    raw = response.message.content[0].text
    logging.info(f"AI raw válasz: {raw[:80]}...")

    # JSON kibontása kapcsos zárójelek között
    json_str = raw.strip()
    if not json_str.startswith('{'):
        json_str = '{' + json_str.split('{', 1)[-1]
    if not json_str.endswith('}'):
        json_str = json_str.rsplit('}', 1)[0] + '}'
    json_str = json_str.replace('\n', ' ')
    try:
        result = json.loads(json_str)
        # Extra validáció a kulcsokra
        required_keys = {"facebook", "instagram", "linkedin", "x"}
        if not all(k in result for k in required_keys):
            raise ValueError("Hiányzó kulcsok")
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"JSON hiba: {e}\nRaw válasz: {json_str}")
        return {
            "error": "Hibás formátumú AI válasz",
            "raw_response": json_str,
            "debug_prompt": prompt  
        }

    # Emojik eltávolítása, ha kell
    if not use_emojis:
        for k, v in result.items():
            if isinstance(v, str):
                result[k] = strip_emojis(v)

    return result

@app.route('/generate', methods=['POST', 'OPTIONS'])
def generate():
    """
    HTTP POST végpont, amely JSON-ben kapja a bemenetet:
        {
            "message": "kampányüzenet",
            "audience": "célközönség",
            "tone": "hangnem",
            "emojis": true/false
        }

    Meghívja a `generate_ai_message()` függvényt, majd visszaadja az eredményt JSON válaszként.

    Ha az OPTIONS metódus érkezik (pl. CORS preflight kérés), akkor 200 OK választ ad vissza.

    Visszatér:
        Response: JSON válasz, amely tartalmazza a generált posztokat vagy hibaüzenetet.
    """

    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')
    audience = data.get('audience', '')
    tone = data.get('tone', '')
    emojis = data.get('emojis', False)

    logging.info(f"Generálás: message={message}, audience={audience}, tone={tone}, emojis={emojis}")
    result = generate_ai_message(message, audience, tone, emojis)

    resp = jsonify(result)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)