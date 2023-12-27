import ctypes
import time
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
    exit_slack()
    global game_locked
    game_locked = True
    show_yes_no_popup("Have you completed your work?", "Slack")
    return jsonify({'message': 'Slack content locked for all users'})

def show_yes_no_popup(message, title):
    result = ctypes.windll.user32.MessageBoxW(0, message, title, 1 | 0x40)  # MB_YESNO flag

    if result == 1:  # User clicked "Yes"
        # do thingy here
        print("Yes")
    else:
        # Terminate the Slack application or perform other actions
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == 'slack.exe':
                psutil.Process(process.info['pid']).terminate()


def run_game():
    # Check if the game is unlocked
    if not game_locked:
        return "Running the game for all users"
    else:
        return "Game is locked. Complete the task to unlock."

def exit_slack():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == 'slack.exe':
            print("Terminating Notepad...")
            try:
                show_yes_no_popup("Have you completed your work?", "Slack")

                # psutil.Process(process.info['pid']).terminate()
                print("Notepad terminated.")
            except psutil.NoSuchProcess:
                print("Notepad process not found.")
            return

def check_and_exit_notepad():
    while True:
        if game_locked:
            exit_slack()
        time.sleep(1)

@app.route('/unlock', methods=['GET', 'POST'])
def unlock():
    return jsonify({'message': unlock_game_content()})

@app.route('/lock', methods=['GET', 'POST'])
def lock():
    exit_slack()
    return lock_game_content()

@app.route('/run', methods=['GET', 'POST'])
def run():
    return jsonify({'message': run_game()})

@app.route('/assignment_data', methods=['POST'])
def thatscrayz():
    return jsonify({"hi": "ur mom heheheha"})

if __name__ == '__main__':
    # Start the Flask application in a separate thread
    threading.Thread(target=check_and_exit_notepad, daemon=True).start()
    app.run(debug=True, use_reloader=False)
