from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'alive': True})


@app.route('/api/wifi/configure', methods=['POST'])
def configure_wifi():
    return jsonify({})


app.run(port=5001)
