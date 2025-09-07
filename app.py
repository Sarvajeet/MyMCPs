from flask import Flask, render_template, request, jsonify
from mcp_client import MCPClient
import asyncio
import json

app = Flask(__name__)
client = MCPClient()

@app.route('/')
def index():
    with open('config.json') as f:
        config = json.load(f)
    return render_template('index.html', servers=config['servers'])

@app.route('/connect', methods=['POST'])
async def connect():
    data = request.get_json()
    server_url = data.get('server_url')
    if not server_url:
        return jsonify({'error': 'No server URL provided'}), 400

    response = await client.connect_to_server(server_url)
    return jsonify({'message': response})


@app.route('/chat', methods=['POST'])
async def chat():
    data = request.get_json()
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    response = await client.process_query(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
