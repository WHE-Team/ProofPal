from google.oauth2 import service_account
from googleapiclient.discovery import build
import mimetypes
from googleapiclient.errors import HttpError

import base64

# Replace these values with your own credentials and classroom information
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.coursework.students.readonly']
SERVICE_ACCOUNT_FILE = 'C:/Users/arnna/OneDrive/Desktop/ProofPal/service-account-file.json'
COURSE_ID = ''
ASSIGNMENT_ID = ''

# Add your game unlocking mechanism here
def authenticate():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject('darrensu09@gmail.com')

    service = build('classroom', 'v1', credentials=delegated_credentials)
    return service

def check_assignment_completion():
    service = authenticate()

    try:
        # Get student submissions for the assignment
        submissions = service.courses().courseWork().studentSubmissions().list(
            courseId=COURSE_ID,
            courseWorkId=ASSIGNMENT_ID
        ).execute()

        # Check if there are submissions
        if 'studentSubmissions' in submissions:
            print("Assignment completion verified! Students have submitted the assignment.")

            # Unlock game content for each student
            for submission in submissions['studentSubmissions']:
                student_email = submission['userId']
                unlock_game_content(student_email)
        else:
            print("No submissions found. Please check if students have submitted the assignment.")
    except HttpError as e:
        print(f"HTTP Error occurred: {e}")
        print(f"Details: {e._get_reason()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def unlock_game_content(student_email):
    # Your game-specific logic to unlock content for the given student
    print(f"Game content unlocked for student: {student_email}")

# Run the script
check_assignment_completion()
