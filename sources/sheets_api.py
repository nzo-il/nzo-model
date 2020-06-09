# code mostly copied from https://developers.google.com/sheets/api/quickstart/python
from __future__ import print_function

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
DATA_SOURCE_SPREADSHEET_ID = '1nnd7Hx8Van63Rf21DYPV4kb-trxaW5oqG7Ndf6rCaPg'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
AREAS_SUMMARY_RANGE = 'Areas!A111:K120'


def get_data_for_areas():
    return get_values(range_name=AREAS_SUMMARY_RANGE)


def get_values(range_name):
    sheets_service = connect()

    result = get_sheet_values(sheets_service, range_name=range_name)
    values = result.get('values', [])
    return values


def get_sheet_values(sheets_service, spreadsheet_id=DATA_SOURCE_SPREADSHEET_ID,
                     range_name=AREAS_SUMMARY_RANGE):
    result = sheets_service.values().get(spreadsheetId=spreadsheet_id,
                                             range=range_name).execute()
    return result


def connect():
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
                'sources/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet


if __name__ == '__main__':
    get_values()
