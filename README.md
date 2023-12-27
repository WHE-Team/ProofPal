# ProofPal: Homework Sentry
ProofPal: Homework Sentry is a tool designed to verify and track homework completion within the context of Google Classroom. This script utilizes the Google Classroom API to check if students have submitted their assignments, and as a reward, it unlocks games for the students who have successfully completed their homework.

## Getting Started
To use ProofPal: Homework Sentry, follow these steps:

## Prerequisites
### Google Classroom API Credentials:
- Create a project in the [Google Cloud Console](https://console.cloud.google.com).
- Enable the Google Classroom API for your project.
- Create a service account and download the JSON credentials file.
- Share your Google Classroom course with the service account email.
### Python Dependencies:
- Install the required Python dependencies using `pip install -r requirements.txt`
  
## Configuration
Replace placeholder values in the script (SERVICE_ACCOUNT_FILE, COURSE_ID, and ASSIGNMENT_ID) with your actual service account file path, course ID, and assignment ID.

## Usage
Run the script using the following command:
```
python proofpal.py
```
The script will prompt you for confirmation of homework completion, ask for an image file as proof, and unlock games for students who have successfully completed their assignments.

## Important Notes
- This script includes a game unlocking feature as a reward for completing assignments.
- Ensure you have the necessary permissions and comply with Google's API usage policies.
- Respect user privacy and consent when collecting and verifying personal data.
- Modify the unlock_games_for_student function to suit your specific game unlocking mechanism.

## Contributing
If you have suggestions or improvements, feel free to open an issue or submit a pull request. Contributions are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.






