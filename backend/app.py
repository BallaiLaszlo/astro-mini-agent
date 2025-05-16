from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

# Logger beállítása fájlba és konzolra
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    app.logger.info("Generálás indítva ezekkel az adatokkal:")
    app.logger.info(f"Kampányüzenet: {data.get('message')}")
    app.logger.info(f"Célközönség: {data.get('audience')}")
    app.logger.info(f"Hangnem: {data.get('tone')}")
    app.logger.info(f"Használjon emojikat: {data.get('emojis')}")
    return jsonify({"status": "success", "message": "Adatok fogadva"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
