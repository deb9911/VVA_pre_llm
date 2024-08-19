from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
app.config.from_object('config.Config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

config = {
    "commands": [
        {"keyword": "google search", "action": "google_search"},
        {"keyword": "wake up", "action": "wake_up_cmd"},
        {"keyword": "wikipedia search", "action": "wikipedia_search"},
        {"keyword": "tell time", "action": "tell_time"},
        {"keyword": "get today", "action": "get_today"},
        {"keyword": "introduce yourself", "action": "name_intro"},
        {"keyword": "play music", "action": "play_music"},
        {"keyword": "make note", "action": "make_note"},
        {"keyword": "open window", "action": "open_window"},
        {"keyword": "stop assistant", "action": "end_assistant"},
        {"keyword": "shut down", "action": "system_down"},
        {"keyword": "lock system", "action": "sys_lock"},
        {"keyword": "clean trash", "action": "cln_trsh"},
        {"keyword": "clear console", "action": "cmd_clr"},
        {"keyword": "mute sound", "action": "mute_system_sound"},
        {"keyword": "unmute sound", "action": "unmute_system_sound"}
    ],
    "voices": ["default", "male", "female"],
    "current_voice": "default"
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/device_management')
def device_management():
    return render_template('device_management.html')


@app.route('/add_command_view')
def add_command_view():
    return render_template('add_command.html')


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
