from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, static_url_path='/static')

# Dummy cache (replace with an actual caching solution)
assignment_completion_cache = {}
assignment_progress_cache = {}

@app.route('/')
def index():
    try:
        # Make a GET request
        api_url = "https://eo5bs0p3l6ch4f2.m.pipedream.net"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        api_data = response.json()
        assignments_data = api_data.get("$return_value", [])
        print("API Response:", assignments_data)
    except requests.RequestException as e:
        print(f"Error making API request: {e}")
        assignments_data = [{'courseId': '458036873054', 'id': '458036873150', 'title': 'what the dog doin', 'materials': [{'form': {'formUrl': 'https://docs.google.com/forms/d/1ujmrBTNPbX_nhzl9Z6HA7gRuuX04Vz2RvkJG6yhbfdA/edit', 'title': 'Test Quiz', 'thumbnailUrl': 'https://lh4.googleusercontent.com/waqd0yfAuD_oI6POOAK89sjLKbCBtnhcXS3Pr4IIM9BUo4pJChWKVuOa_726vA4ORcLaCAeivZs=w90-h90-p'}}], 'state': 'PUBLISHED', 'alternateLink': 'https://classroom.google.com/c/NDU4MDM2ODczMDU0/a/NDU4MDM2ODczMTUw/details', 'creationTime': '2022-01-15T02:07:47.819Z', 'updateTime': '2022-01-15T03:59:50.562Z', 'dueDate': {'year': 2022, 'month': 1, 'day': 13}, 'dueTime': {'hours': 11, 'minutes': 59}, 'maxPoints': 100, 'workType': 'ASSIGNMENT', 'submissionModificationMode': 'MODIFIABLE_UNTIL_TURNED_IN', 'creatorUserId': '111429679513355779060'}]

    return render_template('index.html', assignments=assignments_data)

@app.route('/save_completion', methods=['POST'])
def save_completion():
    data = request.get_json()
    assignment_id = data.get('assignmentId')

    if assignment_id:
        # Save the completion status to the cache (replace this with your caching logic)
        assignment_completion_cache[assignment_id] = True
        message = f"Completion status for assignment '{assignment_id}' saved to cache."
    else:
        message = "Invalid data received."

    return jsonify({'message': message})

@app.route('/save_progress', methods=['POST'])
def save_progress():
    data = request.get_json()
    assignment_id = data.get('assignmentId')
    goal = data.get('goal')

    if assignment_id and goal:
        # Save both completion status and goal to the cache (replace this with your caching logic)
        assignment_completion_cache[assignment_id] = True
        assignment_progress_cache[assignment_id] = goal
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
    app.run(debug=True, use_reloader=False)