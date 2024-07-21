from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Example configuration data
config = {
    "commands": [
        {"keyword": "open notepad", "action": "open_notepad"},
        {"keyword": "search google", "action": "search_google"}
    ],
    "voices": ["default", "male", "female"],
    "current_voice": "default"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config)

@app.route('/api/config', methods=['POST'])
def update_config():
    global config
    config = request.json
    return jsonify({"message": "Configuration updated"})

@app.route('/api/commands', methods=['POST'])
def add_command():
    command = request.json
    config['commands'].append(command)
    return jsonify({"message": "Command added"})

@app.route('/api/commands/<int:index>', methods=['DELETE'])
def delete_command(index):
    config['commands'].pop(index)
    return jsonify({"message": "Command deleted"})

if __name__ == '__main__':
    app.run(debug=True)


