from openai import OpenAI
import ctypes
import time
from flask import Flask, render_template, request, jsonify
import psutil
import threading
import requests


# Flag to track the game status (Initially, the game is locked)
game_locked = True
app = Flask(__name__, static_url_path='/static')
assignment_completion_cache = {}
assignment_progress_cache = {}
blacklist = ["Notion.exe"]
client = OpenAI(
    api_key="haha no api key for you",
)

def analyze_homework(content, goal):
    prompts = "This goal is:" + goal + "Has this homework alined with the goal? Say yes or no. Only say a single yes or no."

    response = client.chat.completions.create(
        messages=[{"role": "system", "content": prompts},
                    {"role": "user", "content": content}],
        model="gpt-3.5-turbo",
        temperature=0,
    )
    resp = response.choices[0].message.content.lower()
    if "yes" in resp:
        return True
    elif "no" in resp:
        return False
    else:
        print("SMTH HAPPENED:", resp)
        return False
    
def fetch_drive_content(id):
    data = requests.post("https://eoedmrclsi6vf08.m.pipedream.net", json={"id": id})
    print("Drive content fetched!")
    return data.text

def unlock_game_content():
    # Update the game status to unlocked
    global game_locked
    game_locked = False
    return "Game content unlocked for all users"

def lock_game_content():
    detect_game()
    global game_locked
    game_locked = True
    show_yes_no_popup("Have you completed your work?", "Slack")
    return jsonify({'message': 'Slack content locked for all users'})

def show_yes_no_popup(message, title):
    result = ctypes.windll.user32.MessageBoxW(0, message, title, 1 | 0x40)  # MB_YESNO flag

    if result == 1:  # User clicked "Yes"
        # do thingy here
        if game_locked:
            kill()
            ctypes.windll.user32.MessageBoxW(0, "You have not!", "Popup Message", 1)
        else:
            print("Ok Cool")
    else:
        kill()

def run_game():
    # Check if the game is unlocked
    if not game_locked:
        return "Running the game for all users"
    else:
        return "Game is locked. Complete the task to unlock."

def kill():
    # Terminate the Slack application or perform other actions
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] in blacklist:
            psutil.Process(process.info['pid']).terminate()
    
def detect_game():
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] in blacklist:
            print("Terminating...")
            try:
                psutil.Process(process.info['pid']).terminate()
                print("Notepad terminated.")

                show_yes_no_popup("Have you completed your work?", "Slack")
            except psutil.NoSuchProcess:
                print("Notepad process not found.")
            return

def check_and_exit_notepad():
    while True:
        if game_locked:
            detect_game()
        time.sleep(1)

@app.route('/unlock', methods=['GET', 'POST'])
def unlock():
    return jsonify({'message': unlock_game_content()})

@app.route('/lock', methods=['GET', 'POST'])
def lock():
    detect_game()
    return lock_game_content()

@app.route('/run', methods=['GET', 'POST'])
def run():
    return jsonify({'message': run_game()})

@app.route('/assignment_data', methods=['POST'])
def thatscrayz():
    global game_locked

    data = request.get_json()
    print(data)
    submitted_id = data["data"]["trigger"]['event']["courseWorkId"]
    print(assignment_completion_cache)
    print(assignment_progress_cache)

    print(submitted_id)

    if assignment_completion_cache:
        if submitted_id in assignment_completion_cache.keys():
            print("Assignment has been turned in! Goal achieved.")
            assignment_completion_cache.pop(submitted_id)
            game_locked = False
    elif assignment_progress_cache:
        if submitted_id in assignment_progress_cache.keys():
            goal = assignment_progress_cache[submitted_id]
            drive_files = data["data"]["trigger"]["event"]["assignmentSubmission"]["attachments"]
            one_file = drive_files[0]["driveFile"]["id"]
            content = fetch_drive_content(one_file)
            completed = analyze_homework(content, goal)
            if completed:
                print("Assignment goal has been achieved! Turning off lock.")
                assignment_progress_cache.pop(submitted_id)
                game_locked = False
    else:
        pass
    return jsonify({"received": 200})

@app.route('/')
def index():
    try:
        # Make a GET request
        api_url = "https://eoayxjelaldbg33.m.pipedream.net" # TODO CHANGE THIS TO WHATEVER THE URL IS
        response = requests.get(api_url)
        response.raise_for_status()
        api_data = response.json()
        assignments_data = api_data.get("$return_value", [])
        print("API Response:", assignments_data)
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        assignments_data = [{'courseId': '458036873054', 'id': '458036873150', 'title': 'what the dog doin', 'materials': [{'form': {'formUrl': 'https://docs.google.com/forms/d/1ujmrBTNPbX_nhzl9Z6HA7gRuuX04Vz2RvkJG6yhbfdA/edit', 'title': 'Test Quiz', 'thumbnailUrl': 'https://lh4.googleusercontent.com/waqd0yfAuD_oI6POOAK89sjLKbCBtnhcXS3Pr4IIM9BUo4pJChWKVuOa_726vA4ORcLaCAeivZs=w90-h90-p'}}], 'state': 'PUBLISHED', 'alternateLink': 'https://classroom.google.com/c/NDU4MDM2ODczMDU0/a/NDU4MDM2ODczMTUw/details', 'creationTime': '2022-01-15T02:07:47.819Z', 'updateTime': '2022-01-15T03:59:50.562Z', 'dueDate': {'year': 2022, 'month': 1, 'day': 13}, 'dueTime': {'hours': 11, 'minutes': 59}, 'maxPoints': 100, 'workType': 'ASSIGNMENT', 'submissionModificationMode': 'MODIFIABLE_UNTIL_TURNED_IN', 'creatorUserId': '111429679513355779060'}]

    return render_template('index.html', assignments=assignments_data)

@app.route('/save_completion', methods=['POST'])
def save_completion():
    global game_locked

    game_locked = True
    data = request.get_json()
    assignment_id = data.get('assignmentId')

    if assignment_id:
        # Save the completion status to the cache (replace this with your caching logic)
        assignment_completion_cache[assignment_id] = True # "id": True
        print(assignment_completion_cache)
        message = f"Completion status for assignment '{assignment_id}' saved to cache."
    else:
        message = "Invalid data received."

    return jsonify({'message': message})

@app.route('/save_progress', methods=['POST'])
def save_progress():
    global game_locked

    game_locked = True
    data = request.get_json()
    assignment_id = data.get('assignmentId')
    goal = data.get('goal')

    if assignment_id and goal:
        # Save both completion status and goal to the cache (replace this with your caching logic)
        assignment_progress_cache[assignment_id] = goal # "id": "goal"
        message = f"Completion status and goal for assignment '{assignment_id}' saved to cache."
    else:
        message = "Invalid data received."

    return jsonify({'message': message})

@app.route('/get_completion_cache', methods=['GET'])
def get_completion_cache():
    return jsonify({'completion_cache': assignment_completion_cache})

@app.route('/get_progress_cache', methods=['GET'])
def get_progress_cache():
    return jsonify({'progress_cache': assignment_progress_cache})

if __name__ == '__main__':
    # Start the Flask application in a separate thread
    threading.Thread(target=check_and_exit_notepad, daemon=True).start()
    app.run(debug=True, use_reloader=False)
