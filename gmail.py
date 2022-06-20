from __future__ import print_function
import os.path, base64, config, json, pprint as pp, email
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

def get_tradingview_label_content():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    #Unread threads for the tradingview label
    service = build('gmail', 'v1', credentials=creds) 
    results = service.users().threads().list(userId="me", labelIds=[config.TRADINGVIEW_LABEL], q="is:UNREAD").execute()
    threads = results.get('threads', [])

    if not threads:
        return 'No messages'
    else:
        for thread in threads:
            threadData = service.users().threads().get(userId="me", id=thread["id"]).execute()

            for i in range(len(threadData) - 1):
                msg = threadData['messages'][i]['payload']['body']['data']
                msg = base64.urlsafe_b64decode(msg)
                mime_msg = email.message_from_bytes(msg)

                if  "<!DOCTYPE html>" not in str(mime_msg):
                    #convert to json
                    order = json.loads(str(mime_msg))
                    #pp.pprint(order)   

                #Mark as read
                '''
                service.users().threads().modify(
                userId="me",
                id=threadData["id"], 
                body={
                    "removeLabelIds": ['UNREAD']
                }).execute()'''
    
    return order