from __future__ import print_function

import sys
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import django
django.setup()

from ultimate_frisbee_management.models import Person, Club, Team, PersonToTeamMembership, PersonToClubMembership
from django.contrib.auth.models import User


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

SCOPES = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


def get_google_sheet(spreadsheet_id, range_name) -> gspread.Worksheet:
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = ServiceAccountCredentials.from_json_keyfile_name('/etc/credentials/google_drive_credentials.json', SCOPES)  
    client = gspread.authorize(creds)
    return client.open_by_key(spreadsheet_id).sheet1
 


def get_player_data(gsheet: gspread.Worksheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    admin_user = User.objects.get(username="admin")
    data = gsheet.get_all_values()
    h = data[2]  # Assumes first line is header!
    for row in data[3:]:
        user_data= {
            'username': row[1],
            'email': row[h.index('e-mail')],
        }

        try: 
            user = User.objects.update_or_create(**user_data)[0]
        except django.db.utils.IntegrityError:
            logger.info("spieler doppelt gemeldet.")
            continue
        
        person_data ={
            "firstname": row[h.index("firstname")],
            "lastname": row[h.index("lastname")],
            "sex":  row[h.index("sex")].lower(),
            "birthdate": f"{row[h.index('birthdate (year)')]}-01-01",
            "user": user
        }
        try: 
            person = Person.objects.update_or_create(**person_data)[0]
        except django.core.exceptions.ValidationError:
            logger.info("keine geburtsdatum angegeben wird auf 2019 gesetzt.")
            person_data["birthdate"] = "2019-01-01"
            person = Person.objects.update_or_create(**person_data)[0]
        except django.db.utils.IntegrityError:
            logger.info("person existiert.")
            continue
        
        club_data= {
            "name": row[h.index("club_membership_name")],
            "founded_on": "2000-01-01"
        }
        try: 
            club = Club.objects.update_or_create(**club_data)[0]
        except django.db.utils.IntegrityError:
            logger.info("club existiert.")
            continue

        team_data= {
            "founded_on": "2000-01-01",
            "name": row[h.index("team_membership_1 ÖSTMx_name")],
            "club_membership": club
        }
        try: 
            teams = Team.objects.filter(name=team_data["name"])
            if teams:
                team = teams[0]
            else:          
                team = Team.objects.update_or_create(**team_data)[0]
        except django.db.utils.IntegrityError:
            logger.info("club existiert.")
            continue
        
        role= row[h.index("team_membership_1 ÖSTMx_role")],
        if role == "":
            role = "Player"

        person_to_team_membership_data= {
            "valid_from": "2019-01-01",
            "role": row[h.index("team_membership_1 ÖSTMx_role")],
            "number": row[h.index("team_membership_1 ÖSTMx_number")],
            "person": person,
            "team": team,
            "approved_by":admin_user,
            "reporter":admin_user
        }

        try: 
            personToTeamMembership = PersonToTeamMembership.objects.update_or_create(**person_to_team_membership_data)[0]
        except ValueError:
            logger.info("keine Nummer vergeben wird auf 0 gesetzt.")
            person_to_team_membership_data["number"] = 0
            personToTeamMembership = PersonToTeamMembership.objects.update_or_create(**person_to_team_membership_data)[0]
        except django.db.utils.IntegrityError:
            logger.info("mitgliedschaft besteht bereits.")
            continue

        role= row[h.index("club_membership_role")]
        if role == "":
            role = "Member"

        person_to_club_membership_data= {
            "valid_from": f"{row[h.index('Entry OEFSV (year)')]}-01-01",
            "role": role,
            "person": person,
            "club": club,
            "approved_by":admin_user,
            "reporter":admin_user
        }

        try: 
            personToClubMembership = PersonToClubMembership.objects.update_or_create(**person_to_club_membership_data)[0]
        except django.core.exceptions.ValidationError:
            logger.info("keine Eintritsjahr angegeben eben wird auf 2019 gesetzt.")
            person_to_club_membership_data["valid_from"] = "2019-01-01"
            personToClubMembership = PersonToClubMembership.objects.update_or_create(**person_to_club_membership_data)[0]
        except django.db.utils.IntegrityError:
            logger.info("mitgliedschaft besteht bereits.")
            continue