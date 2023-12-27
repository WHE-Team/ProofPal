from flask import Flask, jsonify
import psutil
import threading

app = Flask(__name__)

# Flag to track the game status (Initially, the game is locked)
game_locked = True

def unlock_game_content():
    # Update the game status to unlocked
    global game_locked
    game_locked = False
    return "Game content unlocked for all users"

def lock_game_content():
    exit_fortnite()
    global game_locked
    game_locked = True
    return 'Game content locked for all users'


def run_game():
    # Check if the game is unlocked
    if not game_locked:
        return "Running the game for all users"
    else:
        return "Game is locked. Complete the task to unlock."

def exit_fortnite():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'FortniteClient-Win64-Shipping.exe':
            print("Terminating Fortnite...")
            psutil.Process(process.info['pid']).terminate()
            print("Fortnite terminated.")
            return

def check_and_exit_fortnite():
    while True:
        if game_locked:
            exit_fortnite()

@app.route('/unlock', methods=['GET', 'POST'])
def unlock():
    return jsonify({'message': unlock_game_content()})

@app.route('/lock', methods=['GET', 'POST'])
def lock():
    exit_fortnite()
    return jsonify({'message': lock_game_content()})

@app.route('/run', methods=['GET', 'POST'])
def run():
    return jsonify({'message': run_game()})

@app.route('/exit_fortnite', methods=['POST', 'GET'])
def exit_fortnite_endpoint():
    exit_fortnite()
    return jsonify({'message': 'Exiting Fortnite'})

if __name__ == '__main__':
    # Start the Flask application in the main thread
    app.run(debug=True, use_reloader=False)

    # Start the thread to check and exit Fortnite
    fn = threading.Thread(target=check_and_exit_fortnite)
    fn.daemon = True
    fn.start()
