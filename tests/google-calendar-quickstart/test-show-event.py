#! coding:utf8

import httplib2
import datetime

from CalendarWrapper import Credentials
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def main():
    credentials = Credentials.CredentialsHelper.get_credentials()
    http = credentials.authorize(httplib2.Http())

    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print start, event['summary']


if __name__ == '__main__':
    main()
