from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import pandas as pd

df = pd.read_excel('contacts.xlsx')

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
l = []
try:
    contacts = pd.read_csv('allContacts.csv')
    names = list(contacts['Name'])
    for x in df['Name']:
        if x not in names:
            l.append(1)
        else:
            l.append(0)
except:
    for x in df['Name']:
        l.append(1)

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'People API Python Quickstart'


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

for i in range(df.shape[0]):
    if l[i] == 0:
        continue
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('people', 'v1', http=http, discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')


    service.people().createContact(parent='people/me', body={
	    "names": [
	        {
	            "givenName": df['Name'][i]
	        }
	    ],
	    "phoneNumbers": [
	        {
	            'value': df['Number'][i]
	        }
	    
        ]
	}).execute()
    print("Saved",df['Name'][i])
