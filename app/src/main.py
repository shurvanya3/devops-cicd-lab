import socket
import os
from flask import Flask, jsonify

app = Flask(__name__)

VERSION = "1.0.0"
SERVICE_NAME = "devops-cicd-lab-app"

@app.route('/')
def index():
    return jsonify({
        "service": SERVICE_NAME,
        "version": VERSION,
        "hostname": socket.gethostname()
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/greeting')
def greeting():
    is_feat_en = os.getenv("FEATURE_NEW_GREETING", "false").lower() == "true"

    if is_feat_en:
        return jsonify({"message": "You are seeing the brand new awesome greeting feature!"})
    return jsonify({"message": "Hello, World! (This is the old stable greeting)"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
