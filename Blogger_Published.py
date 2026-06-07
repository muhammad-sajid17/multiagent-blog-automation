import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Notice we added the blogger scope alongside the gmail scope!
SCOPES = [
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/blogger'
]


def publish_to_blogger(title: str, html_content: str) -> str:
    """
    Authenticates with Google, finds the user's primary Blogger blog,
    and publishes the HTML content as a live post.
    Returns the public URL of the published post.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('blogger', 'v3', credentials=creds)

        # 1. Fetch the user's blogs to get the Blog ID
        # 1. Fetch the user's blogs to get the Blog ID
        blogs_response = service.blogs().listByUser(userId='self').execute()

        if 'items' not in blogs_response or not blogs_response['items']:
            print("❌ No blogs found. Please create a blog at blogger.com first.")
            return None

        # Default to the first blog on the account
        blog_id = blogs_response['items'][0]['id']
        blog_name = blogs_response['items'][0]['name']
        print(f"   -> 🌐 Connected to Blogger: '{blog_name}' (ID: {blog_id})")

        # 2. Construct the post payload
        body = {
            "title": title,
            "content": html_content
        }

        # 3. Publish the post
        post = service.posts().insert(blogId=blog_id, body=body, isDraft=False).execute()

        return post.get('url')

    except HttpError as error:
        print(f"❌ An error occurred interacting with Blogger API: {error}")
        return None