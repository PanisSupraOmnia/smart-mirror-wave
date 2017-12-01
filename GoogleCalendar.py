from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

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

def get_calendar(credentials, calendar):
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    today = datetime.datetime.now().strftime('%Y-%m-%dT%00:00:00-04:00')# '-04:00' indicates timezone
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days = 1)).strftime('%Y-%m-%dT%00:00:00-04:00')# '-04:00' indicates timezone
    
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=today, timeMax=tomorrow, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    for event in range(0, len(events) - 1):
        calendar[event] = {}
        calendar[event]['name'] = events[event]['summary']
        calendar[event]['start'] = datetime.datetime.strptime(events[event]['start']['dateTime'][:19], '%Y-%m-%dT%H:%M:%S')
        calendar[event]['end'] = datetime.datetime.strptime(events[event]['start']['dateTime'][:19], '%Y-%m-%dT%H:%M:%S')

        try:
            calendar[event]['description'] = events[event]['description']
        except:
            calendar[event]['description'] = 'No Description Available'

        try:
            calendar[event]['location'] = events[event]['location']
        except:
            calendar[event]['location'] = 'No Location Available'

calendar = {}
credentials = get_credentials()
get_calendar(credentials, calendar)
print(calendar)
