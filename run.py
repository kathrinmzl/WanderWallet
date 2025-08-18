# Import neccessary libraries
# import gspread
# from google.oauth2.service_account import Credentials
from datetime import datetime
from trip import Trip
from sheet_manager import SheetManager


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
        print("The end date must be a future date.")
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

            # Check if end date is in the future 
            today = datetime.now().date()
            if today > end_date:
                raise ValueError(
                    "Your trip end date needs to be in the future"
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
            print("\nInvalid data: Your budget is not a whole number, please try again.\n")
            return False
        
        return True
    

def continue_trip():
    """
    Get input if the user wants to continue with the current trip or start a new one
    """
    # Trip Name Input
    while True:
        
        print("\nDo you want to continue working on this trip?")
        print("If 'yes', you can add new expenses in the next step.")
        print("If 'no', we delete the current trip and you can start with a new trip in the\nnext step.")

        yes_no_input = input("\nEnter your decision here (yes/no): ")

        if yes_no_input_valid(yes_no_input):
            print("Data is valid!\n")
            break
    
    if yes_no_input == "yes":
        return True
    else: 
        return False


def yes_no_input_valid(data_input):
    """
    Check if yes/no input data is valid 
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


def start_new_trip(expenses, sheet_manager):
    """
    Initialize new trip
    """
    print("No trip found. Let's set up a new trip.\n")
    # Get basic info for new trip
    new_trip_info = get_new_trip_info()
    # Set up Trip class and calculate trip_info values
    trip = Trip(new_trip_info, expenses, sheet_manager)
    trip.update_trip_info()
    # Save new trip info to worksheet
    sheet_manager.update_worksheet(trip.trip_info, "trip_info")
    # Show trip summary
    print(trip.summary())

    return trip


def get_new_expense(trip):
    """
    Ask user to get a new expense
    """
    while True:
        # Add expenses
        add_expenses(trip)

        print(trip.summary())

        # Check if user wants to add another expense
        while True:
            print("Do you want to add another expense?\n")
            yes_no_input = input("Enter your decision here (yes/no): ")

            # Validate input
            if yes_no_input_valid(yes_no_input):
                print("Data is valid!\n")
                break
        
        if yes_no_input == "no":
            break

    return yes_no_input


def add_expenses(trip):
    """
    Get new expense entry as user input
    """
    # Get date input
    while True:
        print("\nPlease enter the date for which you want to add an expense.")
        print("The expense date cannot be a future date.")
        print("Format: YYYY-MM-DD")
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
            if expense_date < trip.start_date or expense_date > trip.end_date:
                raise ValueError(
                    f"Your expense date needs to be within your travel period {trip.start_date} - {trip.end_date}"
                )
            
            # Check if date is not in the future
            today = datetime.now().date()
            if expense_date > today:
                raise ValueError(
                    "Your expense date cannot be a future date"
                )
        except ValueError as e:
            print(f"\nInvalid data: {e}, please try again.\n")
            continue

        print("Data is valid!\n")

        # Check if the date already exists in the database 
        # Ask user if they want to update it if it already exists
        if date_input in trip.expenses["date"]:
            old_date_index = trip.expenses["date"].index(date_input)
            old_amount = trip.expenses["amount"][old_date_index]
            while True:
                print(f"You already submitted an expense of {old_amount} € for {date_input}.\n")
                print("Do you want to update it?\n")
                yes_no_input = input("Enter your decision here (yes/no): ")

                # Validate input
                if yes_no_input_valid(yes_no_input):
                    print("Data is valid!\n")
                    break
                
            if yes_no_input == "no":
                print("Okay, we will keep the old expense for this date.\n")
                return  # Exit the method without changing anything
            
        break

    # Get amount input
    while True:
        print(f"How much did you spend on {expense_date}?")
        print("Please enter your expense in whole numbers in Euros (no cents or decimal points).")
        print("Example: 24")

        amount_input = input("\nEnter your expense here: ")

        # Validate amount input
        try:
            # Check if provided string can be transformed to an int object
            int(amount_input)
        except ValueError:
            print("\nInvalid data: Your budget is not a whole number, please try again.\n")
            continue
            
        print("Data is valid!\n")
        break

    # Add/update expense amount to/in expense dict
    if date_input in trip.expenses["date"]:
        # Update value in expenses dict if date already exists
        date_index = trip.expenses["date"].index(date_input)
        trip.expenses["amount"][date_index] = amount_input
        print(f"Updated expense for {date_input}.\n")
    else:
        # Add value in expenses dict if date doesn't exist yet
        trip.expenses["date"].append(date_input)
        trip.expenses["amount"].append(amount_input)
        print(f"Added new expense for {date_input}.\n")
        # print(trip.expenses)
    
    # Update trip_info dict with new expense data
    trip.update_trip_info()

    # Save new trip info and expenses to worksheet
    trip.sheet_manager.update_worksheet(trip.trip_info, "trip_info")
    trip.sheet_manager.update_worksheet(trip.expenses, "expenses")


def show_expenses_summary(trip):
    """
    Check if user wants to see a list of all currently tracked expenses
    """
    while True:
        print("Do you want to see a list of all currently tracked expenses?\n")
        yes_no_input = input("Enter your decision here (yes/no): ")

        # Validate input
        if yes_no_input_valid(yes_no_input):
            print("Data is valid!\n")
            break
    
    if yes_no_input == "yes":
        print("Here is a list of your current expenses:\n")
        print(f"{'Date':<15}{'Amount':>12}")
        print("-" * 27)
        for date, amount in zip(trip.expenses['date'], trip.expenses['amount']):
            print(f"{date:<15}{amount:>10} €")
    else: 
        print("Okay, let's move on.")


def main():
    """
    Main function that runs all program functions
    """
    print("Welcome to WanderWallet your personal Travel Expense Tracker\n")
    print("Checking if you have already started tracking travel expenses with us ...")

    creds_file = "creds.json"
    sheet_name = "wander_wallet"
    sheet_manager = SheetManager(creds_file, sheet_name)

    trip_info = sheet_manager.get_worksheet_dict("trip_info")
    expenses = sheet_manager.get_worksheet_dict("expenses")

    today = datetime.now().date()

    trip_exists_answer = trip_exists(trip_info)
    if trip_exists_answer:
        trip = Trip(trip_info, expenses, sheet_manager)
        print(f"Seems like you have been working on your trip '{trip.trip_name}' already.\n")
        # Show trip summary
        print(trip.summary())
        # Check if user wants to see a list of all currently tracked expenses
        show_expenses_summary(trip)
        # Go to function to input decision about continuing with current trip
        continue_trip_val = continue_trip()
        # Delete old trip information if user decidess to start a new trip
        if not continue_trip_val:
            sheet_manager.del_worksheet_data("trip_info")
            sheet_manager.del_worksheet_data("expenses")
            # Set up new trip_info and expenses objects
            trip_info = sheet_manager.get_worksheet_dict("trip_info")
            expenses = sheet_manager.get_worksheet_dict("expenses")
            # Start new trip
            trip = start_new_trip(expenses, sheet_manager)
    else:
        trip = start_new_trip(expenses, sheet_manager)

    # Check if the trip has already started, if not, end the program, otherwise continue
    if trip.start_date > today:
        print("Thank you for setting up your trip with Wander Wallet!")
        print("Your trip hasn't started yet.")
        print("Return to Wander Wallet once your trip starts and you want to start tracking expenses!\n")
        print("End of program")
        return
    else:
        print("Great! Your trip has already started! Let's start adding some expenses.")   

    # Get new expense from user and check if they want to add another one
    get_new_expense_input = get_new_expense(trip)

    if get_new_expense_input == "no":
        # Check if user wants to see a list of all currently tracked expenses
        show_expenses_summary(trip)
        print("\nThank you for using Wander Wallet!")
        print("Come back to this app to add some more expenses to your trip or set up a new one!")
        print("See you next time!\n")
        print("End of program")
        return
    

main()



# To Do: Add restriction that no changes can be made if the trip is already over -> 

