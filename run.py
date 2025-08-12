# Import neccessary libraries
import gspread
from google.oauth2.service_account import Credentials

# The scope lists the APIs that the program should access in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Access the spreadsheet data
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('wander_wallet')

# Test data access
trip_info_sheet = SHEET.worksheet("trip_info")
trip_info = trip_info_sheet.get_all_values()
print(trip_info)

expenses_sheet = SHEET.worksheet("expenses")
expenses = expenses_sheet.get_all_values()
print(expenses)
