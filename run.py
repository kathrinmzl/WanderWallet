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
            print("Data is valid!\n")
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
    

def continue_trip():
    """
    Get input if the user wants to continue with the current trip or start a new one
    """
    # Trip Name Input
    while True:
        
        print("Do you want to continue tracking expenses for this trip?")
        print("If 'yes', you can add new expenses in the next step.")
        print("If 'no', the current trip will be deleted and you can start with a new trip in the next step.")
        print("Example: yes")

        continue_trip_input = input("\nEnter your decision here (yes/no): ")

        if continue_trip_input_valid(continue_trip_input):
            print("Data is valid!\n")
            break
    
    if continue_trip_input == "yes":
        return True
    else: 
        return False


def continue_trip_input_valid(data_input):
    """
    Check if continue trip input data is valid 
    """
    try:
        data_input_val = data_input.lower()

        if data_input_val not in ["yes", "no"]:
            raise ValueError(
                f"'yes' or 'no' expected, you provided '{data_input_val}'"
                )    
    except ValueError as e:
        print(f"\nInvalid data: {e}, please try again.\n")
        return False
        
    return True


def del_workheet_data(sheetname):
    """
    Delete all data from a worksheet, except the headings
    """
    print(f"Deleting data from {sheetname} worksheet...\n")
    worksheet = SHEET.worksheet(sheetname)
    n_rows = worksheet.row_count
    # delete_rows only works if the rows actually exist
    if n_rows >= 2:
        worksheet.delete_rows(2, n_rows)
    print(f"{sheetname} worksheet updated successfully.\n")


# Code from love_sandwiches project
def update_worksheet(data, sheetname):
    """
    Update worksheet "sheetname", add new row with the list data provided
    """
    print(f"Updating {sheetname} worksheet...\n")
    worksheet = SHEET.worksheet(sheetname)
    worksheet.append_row(data)
    print(f"{sheetname} worksheet updated successfully.\n")


def start_new_trip(expenses):
    """
    Initialize new trip
    """
    print("No trip found. Let's set up a new trip.\n")
    # Get basic info for new trip
    new_trip_info = get_new_trip_info()
    # Set up Trip class and calculate trip_info values
    trip = Trip(new_trip_info, expenses)
    trip.update_trip_info()
    # Save new trip info to worksheet
    update_worksheet(list(trip.trip_info.values()), "trip_info")
    # Show trip summary
    print("Here is a summary of your initial trip information:")
    print(trip.summary())

    return trip


class Trip:
    """
    Trip class
    """
    def __init__(self, trip_info: dict, expenses: dict):
        self.trip_info = trip_info
        self.expenses = expenses
        # Get trip info input fields (for calculations)
        self.trip_name = trip_info["trip_name"]
        self.start_date = datetime.strptime(trip_info["start_date"], "%Y-%m-%d").date()
        self.end_date = datetime.strptime(trip_info["end_date"], "%Y-%m-%d").date()
        self.total_budget = int(trip_info["total_budget"])

    # Calculate different properties for trip info 
    @property
    def duration(self):
        """
        Calculate duration
        """
        # Add 1 to include the first and last days both
        return (self.end_date-self.start_date).days + 1
    
    @property
    def daily_budget(self):
        """
        Calculate daily budget
        """
        return round(self.total_budget/self.duration)
    
    @property
    def total_spent(self):
        """
        Calculate total expenses
        """
        # If there are no expenses or max. 1 expense tracked, the "amount" is a single value instead of a list
        if not isinstance(self.expenses["amount"], list):
            if self.expenses["amount"] == "":
                return 0
            else:
                return int(self.expenses["amount"])
        else:
            return sum(int(num) for num in self.expenses["amount"])
    
    @property
    def remaining_budget(self):
        """
        Calculate remaining budget
        """
        return self.total_budget - self.total_spent
    
    @property
    def days_left(self):
        """
        Calculate remaining days
        """
        today = datetime.now().date()
        if today > self.start_date and today < self.end_date:
            days_left_val = (self.end_date - today).days
        elif today > self.end_date:
            # Trip is over
            days_left_val = 0
        else:
            # Trip hasn't started yet
            days_left_val = self.duration
        return days_left_val
    
    @property
    def avg_daily_spent(self):
        """
        Calculate avg daily expenses
        """
        days_spent = self.duration - self.days_left
        # If trip hasn't started yet days_spent is 0
        if days_spent == 0:
            return 0

        return round(self.total_spent/days_spent)
    
    @property
    def budget_status(self):
        """
        Calculate budget status
        """
        if self.avg_daily_spent > self.daily_budget:
            budget_status = "over"
        elif self.avg_daily_spent < self.daily_budget:
            budget_status = "under"
        else:
            budget_status = "on"
        
        return budget_status
    
    def update_trip_info(self):
        """
        Updates the trip_info dict with current calculated values
        """
        self.trip_info["duration"] = self.duration
        self.trip_info["days_left"] = self.days_left
        self.trip_info["total_spent"] = self.total_spent
        self.trip_info["remaining_budget"] = self.remaining_budget
        self.trip_info["daily_budget"] = self.daily_budget
        self.trip_info["avg_daily_spent"] = self.avg_daily_spent
        self.trip_info["budget_status"] = self.budget_status

        return self.trip_info
    
    def summary(self):
        """
        Return a summary of the current trip data
        """
        # Adjust how budget status is display in summary
        if self.budget_status == "over":
            status_msg = "Over budget — try to slow down spending!"
        elif self.budget_status == "under":
            status_msg = "Under budget — great job managing your expenses!"
        else: 
            status_msg = "On track — keep spending balanced."

        return (
            f"{'Trip Name:':20} {self.trip_name}\n"
            f"{'Dates:':20} {self.start_date} - {self.end_date} ({self.duration} days)\n"
            f"{'Days Left:':20} {self.days_left} days\n"

            f"{'Total Budget:':20} {self.total_budget} €\n"
            f"{'Total Expenses:':20} {self.total_spent} €\n"
            f"{'Remaining Budget:':20} {self.remaining_budget} €\n"

            f"{'Daily Budget:':20} {self.daily_budget} €\n"
            f"{'Avg. Daily Expenses:':20} {self.avg_daily_spent} €\n"
            f"{'Budget Status:':20} {status_msg}\n"
            f"\n(All € values rounded to the nearest possible integer)\n")
    
    def add_expenses(self):
        """
        Get new expense entry as user input
        """
        # Get date input
        while True:
            print("Please enter the expense date (Format: YYYY-MM-DD):")
            print("Example: 2025-08-01")

            date_input = input("\nEnter your expense date here: ")

            # Validate date input
            try:
                # Check if provided string can be transformed to a datetime object
                try:
                    expense_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                except ValueError:
                    # Custom message for invalid date format
                    # Set up custom message because "YYYY-MM-DDD" triggers a different warning than e.g. "YYYY-MMM-DD" or "hello"
                    raise ValueError(f"'{expense_date}'. Date must be YYYY-MM-DD")

                # Check if date is within travel period
                if expense_date < self.start_date or expense_date > self.end_date:
                    raise ValueError(
                        f"Your expense date needs to be within your travel period {self.start_date} - {self.end_date}"
                    )
            except ValueError as e:
                print(f"\nInvalid data: {e}, please try again.\n")
                continue

              
            print("Data is valid!\n")
            break

        # Get amount input
        while True:
            print("How much did you spent on that day?")
            print("Please enter your expense in whole numbers in Euros (no cents or decimal points).")
            print("Example: 24")

            date_input = input("\nEnter your expense here: ")

            # Validate amount input
            try:
                # Check if provided string can be transformed to an int object
                int(date_input)
            except ValueError:
                print(f"\nInvalid data: Your budget is not a whole number, please try again.\n")
                continue
              
            print("Data is valid!\n")
            break
    
    
def main():
    """
    Main function that runs all program functions
    """
    print("Welcome to WanderWallet your personal Travel Expense Tracker\n")
    print("Checking if you have already started tracking travel expenses with us ...")

    trip_info = get_worksheet_dict("trip_info")
    expenses = get_worksheet_dict("expenses")

    if trip_exists(trip_info):
        trip = Trip(trip_info, expenses)
        print(f"Seems like you have been working on your trip '{trip.trip_name}' already.\n")
        # Show trip summary
        print("Here is a summary of your current trip information:")
        print(trip.summary())
        # Go to function to input decision about continuing with current trip
        continue_trip_val = continue_trip()
        # Delete old trip information if user decidess to start a new trip
        if not continue_trip_val:
            del_workheet_data("trip_info")
            del_workheet_data("expenses")
            # Set up new trip_info and expenses objects
            trip_info = get_worksheet_dict("trip_info")
            expenses = get_worksheet_dict("expenses")
            # Start new trip
            trip = start_new_trip(expenses)
    else:
        trip = start_new_trip(expenses)

    print("Great! Let's start adding some expenses.")   
    # Add expenses
    trip.add_expenses()
    print("Current trip summary:")
    print(trip.summary())

    # todo: ask to add another expense and put everything into a while loop

main()

# To Do: Add restriction that no changes can be made if the trip is already over -> 

"""
Trip Name	Start Date	End Date	Total Budget	Total Spent	Remaining Budget	Daily Budget	Avg Daily Spent	Budget Status	Days Left
Date	Amount (in €)
"""

