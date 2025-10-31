"""
server.py - Simple Flask server to expose the local CommandProcessor to the UI.
Serves files from the UI/ folder at root and exposes POST /api/command to accept a JSON {command: string}.
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from model import CommandProcessor
import os

app = Flask(__name__, static_folder='UI', static_url_path='')
CORS(app)

processor = CommandProcessor()

@app.route('/api/command', methods=['POST'])
def api_command():
    data = request.get_json() or {}
    cmd = data.get('command', '')
    if not cmd:
        return jsonify({'error': 'no command provided'}), 400
    try:
        response = processor.process(cmd)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve UI static files
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_ui(path):
    ui_dir = os.path.join(os.path.dirname(__file__), 'UI')
    if os.path.exists(os.path.join(ui_dir, path)):
        return send_from_directory(ui_dir, path)
    else:
        return send_from_directory(ui_dir, 'index.html')

if __name__ == '__main__':
    # Run on localhost:5000. Open http://localhost:5000 in your browser.
    app.run(host='0.0.0.0', port=5000, debug=True)
