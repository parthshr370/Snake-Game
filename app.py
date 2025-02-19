from flask import Flask, request, jsonify, render_template
import sqlite3
import threading
import time
from game_logic import GameEnvironment

app = Flask(__name__)
game_env = GameEnvironment()

def init_db():
    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    player_input = data.get("playerInput", "")
    if ":" not in player_input:
        return jsonify({"error": "Invalid format"}), 400

    name_part, skills_part = player_input.split(":")
    player_name = name_part.strip()
    skills = [skill.strip() for skill in skills_part.split(",")]

    conn = sqlite3.connect('players.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO players (name, skills) VALUES (?, ?)", (player_name, ','.join(skills)))
    player_id = cursor.lastrowid
    conn.commit()
    conn.close()

    game_env.init_game(player_id, player_name, skills)
    return jsonify({"status": "Game started"}), 200

@app.route('/game_state', methods=['GET'])
def game_state():
    return jsonify(game_env.get_state()), 200

def run_game_loop():
    while True:
        time.sleep(0.2)
        game_env.update()

if __name__ == '__main__':
    init_db()
    threading.Thread(target=run_game_loop, daemon=True).start()
    app.run(debug=True)
