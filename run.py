# Import neccessary libraries
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

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


def get_worksheet_dict(sheet_name):
    """
    Get worksheet data and transform it into a dictionary
    """
    sheet = SHEET.worksheet(sheet_name)
    sheet_list = sheet.get_all_values()

    # print(sheet_list)

    if len(sheet_list) == 2:
        keys, values = sheet_list
        sheet_dict = dict(zip(keys, values))
    
    elif len(sheet_list) > 2:
        # Extract keys and rows
        keys = sheet_list[0]       # ['date', 'amount']
        rows = sheet_list[1:]      # [['h', '1212'], ['s', '3435']]

        # Create dict with list comprehensions
        sheet_dict = {key: [row[i] for row in rows] for i, key in enumerate(keys)}        

    else:  # only headings
        sheet_dict = dict.fromkeys(sheet_list[0], "")
    
    return sheet_dict 


def trip_exists(trip_info_data):
    """
    Check if trip exists already
    """
    if trip_info_data["trip_name"] != "":
        return True
    else:
        # Only headings exist
        return False


def get_new_trip_info():
    """
    Get info for a new trip (start, end dates, trip name, budget)
    """
    print("Are you ready to start tracking expenses for your next adventure?\n")

    # Trip Name Input
    while True:
        
        print("Please enter a name for your new trip (1 - 30 characters).")
        print("Example: Italy Summer 2025")

        trip_name_input = input("\nEnter your trip name here: ")

        if new_trip_info_valid(trip_name_input, "trip_name"):
            print("Data is valid!\n")
            break
    
    # Trip Dates Input
    while True:
        
        print("When are you taking your trip?")
        print("Please enter the start and end date for your new trip.")
        print("The start date cannot be a past date.")
        print("The dates should be seperated by a comma and have the Format YYYY-MM-DD")
        print("Please type in the start date first!")
        print("Example: 2025-08-01,2025-08-15")

        trip_dates_input = input("\nEnter your trip dates here: ")

        # Remove white space and seperate dates at the comma
        trip_dates_list = [date.strip() for date in trip_dates_input.split(",")]

        if new_trip_info_valid(trip_dates_list, "trip_dates"):
            print("Data is valid!")
            break

    # Trip Budget Input
    while True:
        
        print("What is the total budget for your trip?")
        print("Please enter your budget in whole numbers in Euros (no cents or decimal points).")
        print("Example: 2500")

        trip_budget_input = input("\nEnter your total trip budget here: ")

        if new_trip_info_valid(trip_budget_input, "trip_budget"):
            print("Data is valid!\n")
            break
    
    new_trip_info = [trip_name_input, *trip_dates_list, trip_budget_input]
    new_trip_info_keys = ['trip_name', 'start_date', 'end_date', 'total_budget']

    new_trip_info_dict = dict(zip(new_trip_info_keys, new_trip_info))
    return new_trip_info_dict


def new_trip_info_valid(data_input, data_type):
    """
    Check if trip info input data is valid depending on the data type
    """
    if data_type == "trip_name":
        try:
            if len(data_input) > 30 or len(data_input) < 1:
                raise ValueError(
                    f"Min. 1 and not more than 20 characters allowed, you provided {len(data_input)}"
                )    
        except ValueError as e:
            print(f"\nInvalid data: {e}, please try again.\n")
            return False
        
        return True
    
    if data_type == "trip_dates":
        try:
            # Check if provided strings can be transformed to a datetime object
            datetime_input = []
            for date_str in data_input:
                try:
                    datetime_input.append(datetime.strptime(date_str, "%Y-%m-%d").date())
                except ValueError:
                    # Custom message for invalid date format
                    # Set up custom message because "YYYY-MM-DDD" triggers a different warning than e.g. "YYYY-MMM-DD" or "hello"
                    raise ValueError(f"'{date_str}'. Dates must be YYYY-MM-DD")

            # Check if exactly two dates have been submitted
            if len(data_input) != 2:
                raise ValueError(
                    f"Exactly two dates are expected, you provided {len(data_input)}"
                ) 

            # Check if end date is later than start date
            start_date = datetime_input[0]
            end_date = datetime_input[1]
            if end_date <= start_date:
                raise ValueError(
                    "Your start date needs to be at least one day before your end date"
                )

            # Check if travel dates are in the future 
            today = datetime.now().date()
            if today > start_date:
                raise ValueError(
                    "Your trip cannot start in the past"
                ) 
            
        except ValueError as e:
            print(f"\nInvalid data: {e}, please try again.\n")
            return False
        
        return True

    if data_type == "trip_budget":
        try:
            # Check if provided string can be transformed to an int object
            int(data_input)
        except ValueError:
            print(f"\nInvalid data: Your budget is not a whole number, please try again.\n")
            return False
        
        return True


def calculate_duration(trip_info):
    """
    Calculate duration
    """
    start_date = datetime.strptime(trip_info["start_date"], "%Y-%m-%d").date()
    end_date = datetime.strptime(trip_info["end_date"], "%Y-%m-%d").date()

    # Add 1 to include the first and last days both
    duration = (end_date-start_date).days + 1

    return duration


def calculate_daily_budget(trip_info, duration):
    """
    Calculate daily budget
    """
    total_budget = trip_info["total_budget"]

    daily_budget = round(int(total_budget)/duration, ndigits=2)

    return daily_budget


def calculate_total_spent(expenses):
    """
    Calculate total expenses
    """
    if not isinstance(expenses["amount"], list):
        total_spent = int(expenses["amount"])
    else:
        total_spent = sum(int(num) for num in expenses["amount"])

    return total_spent


def calculate_remaining_budget(trip_info, total_spent):
    """
    Calculate remaining budget
    """
    remaining_budget = int(trip_info["total_budget"]) - total_spent

    return remaining_budget


def calculate_days_left(trip_info):
    """
    Calculate remaining days
    """
    days_left = (datetime.strptime(trip_info["end_date"], "%Y-%m-%d").date() - datetime.now().date()).days

    return days_left


def calculate_avg_daily_spent(total_spent, duration, days_left):
    """
    Calculate avg daily expenses
    """
    days_spent = duration - days_left
    print(total_spent)
    print(days_spent)
    avg_daily_spent = total_spent/days_spent

    return avg_daily_spent


def main():
    """
    Main function that runs all program functions
    """
    print("Welcome to WanderWallet your personal Travel Expense Tracker\n")
    trip_info = get_worksheet_dict("trip_info")
    expenses = get_worksheet_dict("expenses")
    # print(trip_info)
    # print(expenses)
    calculate_total_spent(expenses)

    trip_found = trip_exists(trip_info)
    if trip_found:
        print("Seems like you have been working on a trip already. Do you want to continue?")
        # Go to function to input decision about continuing with current trip
    else:
        # Get basic info for new trip
        # print("Get new trip info")
        new_trip_info = get_new_trip_info()
        # print(new_trip_info)
        # print(trip_info)

        duration = calculate_duration(new_trip_info)
        # print(duration)
        daily_budget = calculate_daily_budget(new_trip_info, duration)
        print("daily budget")
        print(daily_budget)
        total_spent = calculate_total_spent(expenses)
        print("total spent")
        print(total_spent)
        remaining_budget = calculate_remaining_budget(new_trip_info, total_spent)
        days_left = calculate_days_left(new_trip_info)
        # print(days_left)
        avg_daily_spent = calculate_avg_daily_spent(total_spent, duration, days_left)
        print(avg_daily_spent)





main()

"""
Trip Name	Start Date	End Date	Total Budget	Total Spent	Remaining Budget	Daily Budget	Avg Daily Spent	Budget Status	Days Left
Date	Amount (in €)
"""

