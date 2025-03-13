from flask import Flask, render_template, request, redirect, url_for, jsonify
from game_manager import GameManager
import os

app = Flask(__name__)
os.makedirs('./data/games', exist_ok=True)
game_manager = GameManager('./data/games')

@app.route('/')
def index():
    games = game_manager.get_games()
    return render_template('index.html', games=games)


@app.route('/create_game', methods=['GET', 'POST'])
def create_game():
    if request.method == 'GET':
        return render_template('create_game.html')

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400
    game = game_manager.create_game(data)
    return jsonify({'status': 'success', 'message': 'Game created!', 'game': game})


@app.route('/delete_game/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    success = game_manager.delete_game(game_id)
    if not success:
        return jsonify({'status': 'error', 'message': 'Game not found'}), 404

    return jsonify({'status': 'success', 'message': f'Game {game_id} deleted'})


@app.route('/edit_game/<game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    game = game_manager.get_game_by_id(game_id)
    if not game:
        return jsonify({'status': 'error', 'message': 'Game not found'}), 404

    if request.method == 'GET':
        return render_template('edit_game.html', game=game)

    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

    game = game_manager.edit_game(game_id, data)
    if not game:
        return jsonify({'status': 'error', 'message': 'Game not found'}), 404

    return jsonify({'status': 'success', 'message': 'Game updated', 'game': game})


@app.route('/play_game/<game_id>')
def play_game(game_id):
    return f'Play game {game_id}'


@app.route('/continue_session/<session_id>')
def continue_session(session_id):
    return f'Continue session {session_id}'


@app.route('/delete_session/<session_id>', methods=['POST'])
def delete_session(session_id):
    global sessions
    sessions = [s for s in sessions if s['id'] != session_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)