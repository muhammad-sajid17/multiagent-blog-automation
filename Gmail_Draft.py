import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/blogger'
]


def create_gmail_draft(subject: str, html_content: str, to_email: str = "") -> str:
    """
    Authenticates with Gmail and creates a draft email with the provided HTML content.
    Returns the Draft ID if successful, or None if it fails.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Construct the email
        message = EmailMessage()
        message.set_content("Please enable HTML to view this email.")  # Plain text fallback
        message.add_alternative(html_content, subtype='html')
        message['To'] = to_email
        message['Subject'] = subject

        # Encode as URL-safe base64 string
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'message': {'raw': encoded_message}}

        # Execute the draft creation
        draft = service.users().drafts().create(userId="me", body=create_message).execute()

        return draft['id']

    except HttpError as error:
        print(f"❌ An error occurred interacting with Gmail API: {error}")
        return None