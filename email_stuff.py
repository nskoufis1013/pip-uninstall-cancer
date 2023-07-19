from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import email
from email.mime.text import MIMEText

from small_call_punc import respond

# Set up credentials
CLIENT_ID = '212097183239-6252de0kbe7m95csiktv9gm6fvtlmf02.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret_212097183239-6252de0kbe7m95csiktv9gm6fvtlmf02.apps.googleusercontent.com.json',
    scopes=SCOPES
)
credentials = flow.run_local_server(port=0)

# Create a service object
service = build('gmail', 'v1', credentials=credentials)

# Retrieve only unread email messages
results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
messages = results.get('messages', [])

# Process each unread message
for message in messages:
    msg = service.users().messages().get(userId='me', id=message['id']).execute()

    # Get the message payload
    payload = msg['payload']

    # Check if the payload is multipart (e.g., contains both text and HTML)
    if 'multipart' in payload['mimeType']:
        parts = payload['parts']
        for part in parts:
            if part['mimeType'] == 'text/plain':
                # Print the plain text content
                data = part['body']['data']
                text = base64.urlsafe_b64decode(data).decode('utf-8')
                print("Text content:", text)
    else:
        # Print the message body directly
        data = payload['body']['data']
        text = base64.urlsafe_b64decode(data).decode('utf-8')
        print("Text content:", text)

    print("---")

    # Draft a reply
    reply_message = respond(text)

    # Get the sender from the headers
    sender = next((header['value'] for header in payload['headers'] if header['name'].lower() == 'from'), '')

    # Create the reply email as an RFC822 message string
    reply_email = MIMEText(reply_message)
    reply_email['Subject'] = f"Re: {msg.get('subject', 'No Subject')}"
    reply_email['To'] = sender
    reply_email['From'] = 'me'

    raw_message = base64.urlsafe_b64encode(reply_email.as_string().encode('utf-8')).decode('utf-8')

    # Send the reply
    reply = {'raw': raw_message}
    service.users().messages().send(userId='me', body=reply).execute()

    # Mark the message as read
    service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
