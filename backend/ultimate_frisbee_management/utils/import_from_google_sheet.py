import ultimate_frisbee_management.utils.data_importer as importer

SPREADSHEET_ID = '1u6UrE3cRJRA00GjQf8wo2C-6iW3yyiyztmh9RC9BNTw'
RANGE_NAME = 'person'
 
gsheet = importer.get_google_sheet(SPREADSHEET_ID, RANGE_NAME)
importer.get_player_data(gsheet)
