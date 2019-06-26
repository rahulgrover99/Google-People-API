from __future__ import print_function
from flask import (
    flash, g, redirect, render_template, request, url_for, Flask, send_from_directory
)
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

app = Flask(__name__)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete the file token.pickle.
SCOPES1 = ['https://www.googleapis.com/auth/contacts.readonly']
SCOPES = 'https://www.googleapis.com/auth/contacts'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'People API Python Quickstart'

df = pd.DataFrame()
l = []

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('./')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'people.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def addContact(data):
    chk = 1
    try:
        contacts = pd.read_csv('allContacts.csv')
        names = list(contacts['Name'])
        if data['name'] in names:
            chk = 0
    except:
        chk = 1
    print(chk)
    if chk == 1:
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('people', 'v1', http=http, discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
        service.people().createContact(parent='people/me', body={
            "names": [
                {
                    "givenName": data['name']
                }
            ],
            "phoneNumbers": [
                {
                    'value': data['number']
                }
            
            ]
        }).execute()
        print("Saved",data['name'])
        
def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES1)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    # Call the People API
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,emailAddresses').execute()
    connections = results.get('connections', [])

    for person in connections:
        names = person.get('names', [])
        if names:
            name = names[0].get('displayName')
            print(name)
            l.append(name)
    df['Name'] = l
    df.to_csv('allContacts.csv',index = False)

@app.route("/")
def create():
    main()
    try:
        name = request.args.get('name')
        number = "+91 "+request.args.get('number')
        data = {"name": name, "number": number}
        addContact(data)
        return render_template("index.html")
    except:
        error = "missing argument (name, number, or message), check if QR scan scene is present"
        return render_template("error.html", error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port="8091")