# Import neccessary libraries
# import gspread
# from google.oauth2.service_account import Credentials
from datetime import datetime
from trip import Trip
from sheet_manager import SheetManager
from validation import new_trip_info_valid, int_input_valid, yes_no_input_valid, expense_date_valid
from colorama import Fore, Style, init

# Initialize Colorama (colors reset automatically after each print)
init(autoreset=True)

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
        
        print(Style.BRIGHT + "Please enter a name for your new trip (1 - 30 characters).")
        print("Example: Italy Summer 2025")

        trip_name_input = input(Style.BRIGHT + "\n✏️  Enter your trip name here: ")

        if new_trip_info_valid(trip_name_input, "trip_name"):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break
    
    # Trip Dates Input
    while True:
        
        print(Style.BRIGHT + "When are you taking your trip?")
        print("Please enter the start and end date for your new trip.")
        print("The end date must be a future date.")
        print("The dates should be seperated by a comma and have the Format YYYY-MM-DD")
        print("Please type in the start date first!")
        print("Example: 2025-08-01,2025-08-15")

        trip_dates_input = input(Style.BRIGHT + "\n✏️  Enter your trip dates here: ")

        # Remove white space and seperate dates at the comma
        trip_dates_list = [date.strip() for date in trip_dates_input.split(",")]

        if new_trip_info_valid(trip_dates_list, "trip_dates"):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break

    # Trip Budget Input
    while True:
        
        print(Style.BRIGHT + "What is the total budget for your trip?")
        print("Please enter your budget in whole numbers in Euros (no cents or decimal points).")
        print("Example: 2500")

        trip_budget_input = input(Style.BRIGHT + "\n✏️  Enter your total trip budget here: ")

        if new_trip_info_valid(trip_budget_input, "trip_budget"):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break
    
    new_trip_info = [trip_name_input, *trip_dates_list, trip_budget_input]
    new_trip_info_keys = ['trip_name',
     'start_date', 'end_date', 'total_budget']

    new_trip_info_dict = dict(zip(new_trip_info_keys, new_trip_info))
    return new_trip_info_dict


def continue_trip():
    """
    Get input if the user wants to continue with the current trip or start a new one
    """
    # Trip Name Input
    while True:
        
        print(Style.BRIGHT + "\nDo you want to continue working on this trip?")
        print("If 'yes', you can add new expenses in the next step.")
        print("If 'no', we delete the current trip and you can start with a new trip in the\nnext step.")

        yes_no_input = input(Style.BRIGHT + "\n✏️  Enter your decision here (yes/no): ")

        if yes_no_input_valid(yes_no_input):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break
    
    if yes_no_input == "yes":
        return True
    else: 
        return False


def start_new_trip(expenses, sheet_manager):
    """
    Initialize new trip
    """
    print("✅ No trip found. Let's set up a new trip.\n")
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
            print(Style.BRIGHT + "Do you want to add another expense?\n")
            yes_no_input = input(Style.BRIGHT + "✏️  Enter your decision here (yes/no): ")

            # Validate input
            if yes_no_input_valid(yes_no_input):
                print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
                break
        
        if yes_no_input == "no":
            break

    if yes_no_input == "yes":
        return True
    else: 
        return False


def add_expenses(trip):
    """
    Get new expense entry as user input
    """
    # Get date input
    while True:
        print(Style.BRIGHT + "\nPlease enter the date for which you want to add an expense.")
        print("The expense date cannot be a future date.")
        print("Format: YYYY-MM-DD")
        print("Example: 2025-08-01")

        date_input = input(Style.BRIGHT + "\n✏️  Enter your expense date here: ")

        # Validate date input
        if expense_date_valid(date_input, trip):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
        else: 
            continue

        # Check if the date already exists in the database 
        # Ask user if they want to update it if it already exists
        if date_input in trip.expenses["date"]:
            old_date_index = trip.expenses["date"].index(date_input)
            old_amount = trip.expenses["amount"][old_date_index]
            while True:
                print(Style.BRIGHT + f"You already submitted an expense of {old_amount} € for {date_input}.\n")
                print(Style.BRIGHT + "Do you want to update it?\n")
                yes_no_input = input(Style.BRIGHT + "✏️  Enter your decision here (yes/no): ")

                # Validate input
                if yes_no_input_valid(yes_no_input):
                    print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
                    break
                
            if yes_no_input == "no":
                print("Okay, we will keep the old expense for this date.\n")
                return  # Exit the method without changing anything
            
        break

    # Get amount input
    while True:
        print(Style.BRIGHT + f"How much did you spend on {date_input}?")
        print("Please enter your expense in whole numbers in Euros (no cents or decimal points).")
        print("Example: 24")

        amount_input = input(Style.BRIGHT + "\n✏️  Enter your expense here: ")

        # Validate amount input          
        if int_input_valid(amount_input):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
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
        print(Style.BRIGHT + "Do you want to see a list of all currently tracked expenses?\n")
        yes_no_input = input(Style.BRIGHT + "✏️  Enter your decision here (yes/no): ")

        # Validate input
        if yes_no_input_valid(yes_no_input):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break
    
    if yes_no_input == "yes":
        print(Style.BRIGHT + "Here is a list of your current expenses:\n")
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
    logo = r"""
    __        __              _            __        __    _ _      _   
    \ \      / /_ _ _ __   __| | ___ _ __  \ \      / /_ _| | | ___| |_ 
     \ \ /\ / / _` | '_ \ / _` |/ _ \ '__|  \ \ /\ / / _` | | |/ _ \ __|
      \ V  V / (_| | | | | (_| |  __/ |      \ V  V / (_| | | |  __/ |_ 
       \_/\_/ \__,_|_| |_|\__,_|\___|_|       \_/\_/ \__,_|_|_|\___|\__|
   """
    print(f"{Style.BRIGHT}{Fore.GREEN}{logo}")

    print("\nWelcome to Wander Wallet, your personal Travel Expense Tracker!\n")
    print("⏳ Checking if you have already started tracking travel expenses with us ...")

    creds_file = "creds.json"
    sheet_name = "wander_wallet"
    sheet_manager = SheetManager(creds_file, sheet_name)

    trip_info = sheet_manager.get_worksheet_dict("trip_info")
    expenses = sheet_manager.get_worksheet_dict("expenses")

    today = datetime.now().date()

    trip_exists_answer = trip_exists(trip_info)
    if trip_exists_answer:
        trip = Trip(trip_info, expenses, sheet_manager)
        print(f"✅ Seems like you have been working on your trip '{trip.trip_name}' already.\n")
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

    if not get_new_expense_input:
        # Check if user wants to see a list of all currently tracked expenses
        show_expenses_summary(trip)
        print("\nThank you for using Wander Wallet!")
        print("Come back to this app to add some more expenses to your trip or set up a new one!")
        print("See you next time!\n")
        print("End of program")
        return
    

main()



# To Do: Add restriction that no changes can be made if the trip is already over -> 

