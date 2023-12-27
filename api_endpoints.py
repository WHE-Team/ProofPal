from flask import Flask, jsonify, render_template
import psutil
import threading
import ctypes

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
    show_popup_message("To play games, complete your work!")
    return jsonify({'message': 'Game content locked for all users'})

def show_popup_message(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Message", 1)

def run_game():
    # Check if the game is unlocked
    if not game_locked:
        return "Running the game for all users"
    else:
        return "Game is locked. Complete the task to unlock."

def exit_fortnite():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'FortniteClient-Win64-Shipping.exe':
            print("Terminating...")
            psutil.Process(process.info['pid']).terminate()
            print("Terminated.")
            show_popup_message("To play games, complete your work!")
            return

def check_and_exit_fortnite():
    if game_locked:
        exit_fortnite()

@app.route('/unlock', methods=['GET', 'POST'])
def unlock():
    return jsonify({'message': unlock_game_content()})

@app.route('/lock', methods=['GET', 'POST'])
def lock():
    exit_fortnite()
    return lock_game_content()

@app.route('/exit', methods=['POST', 'GET'])
def exit_fortnite_endpoint():
    exit_fortnite()
    return jsonify({'message': 'Exiting Fortnite'})

if __name__ == '__main__':
    # Start the Flask application in the main thread
    app.run(debug=True, use_reloader=False)

    # Start the thread to check and exit Fortnite
    threading.Thread(target=check_and_exit_fortnite).start()
