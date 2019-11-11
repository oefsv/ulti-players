from __future__ import print_function

import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ..models import Person
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)

SCOPES = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def get_google_sheet(spreadsheet_id, range_name) -> gspread.Worksheet:
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)  
    client = gspread.authorize(creds)
    return client.open_by_key(spreadsheet_id).sheet1
 


def get_player_data(gsheet: gspread.Worksheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    data = gsheet.get_all_values()
    h = data[2]  # Assumes first line is header!
    for row in data[3:]:
        user_data= {
            'username': row[1],
            'email': row[h.index('e-mail')],
        }

        user = User.objects.get_or_create(**user_data)[0]