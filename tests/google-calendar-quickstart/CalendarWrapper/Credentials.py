#! coding:utf8

"""
	Google Calendar API 认证相关
"""

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
# 只读
# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
# 可写可读
SCOPES = 'https://www.googleapis.com/auth/calendar'
# CLIENT_SECRET_FILE = 'client_secret.json'
CLIENT_SECRET_FILE = 'my-client-secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


class CredentialsHelper(object):
    """
            CredentialsHelper 用于获取credentials
    """

    @staticmethod
    def get_credentials():
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_path = "./credential.json"
        store = Storage(credential_path)
        credentials = store.get()

        if credentials:
            return credentials

        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        return credentials
