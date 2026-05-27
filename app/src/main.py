import socket
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
