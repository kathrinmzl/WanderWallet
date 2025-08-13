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
# print(trip_info)

expenses_sheet = SHEET.worksheet("expenses")
expenses = expenses_sheet.get_all_values()
print(expenses)
print(len(expenses))
print(len(expenses[0]))



# def sheet_valid(sheet_data, sheet_name):
#     """
#     """
#     sheet_data_empty = all(len(entry) == 0 for entry in sheet_data)

#     if sheet_data_empty:
#         return False
#     else:
#         if sheet_name == "trip_info":
#             headings_exist = sheet_data[0][0] == "trip_name"
#         else:
#             headings_exist = sheet_data[0][0] == "date"
#         return headings_exist

# def set_sheet_headings(sheet_data, sheet_name):

# sheetvalid = sheet_valid(expenses, "expenses")
# print(sheetvalid)

# if not sheetvalid:
    


def trip_exists(trip_info_data):
    """
    Check if trip exists already
    """
    # Only headings exist
    if len(trip_info_data) == 1:
        return False
    else:
        return True








def main():
    """
    Main function that runs all program functions
    """
    print("Welcome to WanderWallet your personal Travel Expense Tracker\n")
    trip_found = trip_exists(trip_info)
    if trip_found:
        print("Seems like you have been working on a trip already. Do you want to continue?")
        # Go to function to input decision about continuing with current trip
    else:
        # Get basic info for new trip
        print("Get new trip info")



main()

"""
Trip Name	Start Date	End Date	Total Budget	Total Spent	Remaining Budget	Daily Budget	Avg Daily Spent	Budget Status	Days Left
Date	Amount (in €)
"""

