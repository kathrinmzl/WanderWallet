from datetime import datetime
import time
from trip import Trip
from sheet_manager import SheetManager
from validation import (
    new_trip_info_valid,
    int_input_valid,
    yes_no_input_valid,
    expense_date_valid
)
from colorama import Fore, Style, init

# Initialize Colorama (colors reset automatically after each print)
init(autoreset=True)


# From https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
def clear():
    """
    Clear function to clean-up the terminal so things don't get messy
    """
    print("\033c")


def trip_exists(trip_info_data):
    """
    Check if a trip already exists in the worksheet data.

    Args:
        trip_info_data (dict): A dictionary containing trip information

    Returns:
        bool:
        True if the "trip_name" field is not empty (a trip is stored),
        False if only the worksheet headers exist (no trip stored yet)
    """
    if trip_info_data["trip_name"] != "":
        return True
    else:
        # Only headings exist
        return False


def get_new_trip_info():
    """
    Prompt the user for new trip details (trip name, dates, budget).

    The function validates user input step by step:
    - Trip name: must be 1–30 characters, containing only letters, numbers and
    spaces
    - Trip dates: start and end date in YYYY-MM-DD format, separated by a
    comma.
      End date must be in the future
    - Trip budget: positive integer value in euros (whole numbers only)

    Returns:
        dict: A dictionary with the following keys:
            - 'trip_name' (str): the chosen trip name
            - 'start_date' (str): trip start date
            - 'end_date' (str): trip end date
            - 'total_budget' (str): total budget in euros
    """
    # Trip Name Input
    while True:
        print(
            Style.BRIGHT +
            "Please enter a name for your new trip "
            "(1 - 30 characters)."
            )
        print(
            "It can only contain letters (A–Z), numbers (0–9) "
            "and spaces."
            )
        print("Example: Italy Summer 2025")

        trip_name_input = input(
            Style.BRIGHT + "\n✏️  Enter your trip name here: "
            )

        # Validate trip name
        if new_trip_info_valid(trip_name_input, "trip_name"):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break

    # Trip Dates Input
    while True:
        print(Style.BRIGHT + "When are you taking your trip?")
        print("Please enter the start and end date for your new trip.")
        print("The end date must be a future date.")
        print("Dates should be separated by a comma (YYYY-MM-DD,YYYY-MM-DD).")
        print("Please type in the start date first!")
        print("Example: 2025-08-01,2025-08-15")

        trip_dates_input = input(
            Style.BRIGHT +
            "\n✏️  Enter your trip dates here: "
            )

        # Remove white space and seperate dates at the comma
        trip_dates_list = [date.strip() for date in trip_dates_input
                           .split(",")]

        # Validate dats
        if new_trip_info_valid(trip_dates_list, "trip_dates"):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break

    # Trip Budget Input
    while True:
        print(Style.BRIGHT + "What is the total budget for your trip?")
        print("Enter as a positive whole number in euros (no decimals).")
        print("Example: 2500")

        trip_budget_input = input(
            Style.BRIGHT +
            "\n✏️  Enter your total trip budget here: "
            )

        # Validate budget
        if new_trip_info_valid(trip_budget_input, "trip_budget"):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break

    # Save validated data into dictionary
    new_trip_info = [trip_name_input, *trip_dates_list, trip_budget_input]
    new_trip_info_keys = ['trip_name',
                          'start_date',
                          'end_date',
                          'total_budget']
    new_trip_info_dict = dict(zip(new_trip_info_keys, new_trip_info))

    return new_trip_info_dict


def continue_trip():
    """
    Ask the user whether to continue with the current trip or start a new one.

    Returns:
        bool:
            True if the user chooses to continue the current trip,
            False if the user chooses to start a new trip
    """
    # Continue Trip Input
    while True:

        print(Style.BRIGHT + "\nDo you want to continue working on this trip?")
        print("If 'yes', you can add new expenses in the next step.")
        print(
            "If 'no', the current trip will be deleted and you can start a "
            "new trip in the next step."
            )

        yes_no_input = input(
            Style.BRIGHT +
            "\n✏️  Enter your decision here (yes/no): "
            )

        # Validate yes/no input
        if yes_no_input_valid(yes_no_input):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break

    # Small pause + clear screen for better UX
    time.sleep(2)
    clear()

    if yes_no_input == "yes":
        return True
    else:
        return False


def start_new_trip(expenses, sheet_manager):
    """
    Initialize a new trip.

    This function:
    - Prompts the user to enter basic trip details (name, dates, budget).
    - Creates a new `Trip` object using the provided `expenses`.
    - Updates the trip information and stores it in the worksheet.
    - Displays a trip summary to the user.

    Args:
        expenses (dict): A dictionary of expenses to initialize the trip with
        sheet_manager (object): Handles worksheet updates

    Returns:
        Trip: The initialized Trip object containing all trip details.
    """
    print("✅  No trip found. Let's set up a new trip.")
    input(
        Style.BRIGHT +
        "\nPress ENTER to continue\n"
        )

    # Small pause + clear screen for better UX
    time.sleep(2)
    clear()

    # Get basic info for new trip (name, dates, budget)
    new_trip_info = get_new_trip_info()

    # Set up Trip class and calculate trip_info values
    trip = Trip(new_trip_info, expenses)
    trip.update_trip_info()

    # Save new trip info to worksheet
    sheet_manager.update_worksheet(trip.trip_info, "trip_info")
    input(
            Style.BRIGHT +
            "\nPress ENTER to continue\n"
            )

    # Small pause + clear screen for better UX
    time.sleep(2)
    clear()

    # Show trip summary
    print(trip.summary())

    return trip


def get_new_expense(trip, sheet_manager):
    """
    Prompt the user to add one or more expenses to the current trip.

    This function:
    - Calls `add_expenses()` to let the user input a new expense.
    - Displays the updated trip summary after each addition.
    - Asks the user if they want to add another expense, repeating if "yes".
    - Ends once the user answers "no".

    Args:
        trip (Trip): The current Trip object to which expenses will be added
        sheet_manager (object): Handles worksheet updates

    Returns:
        bool:
            True if the last user decision was "yes" (continue adding),
            False if the last user decision was "no" (stop adding expenses)
    """
    while True:
        # Add a new expense and update the worksheet
        add_expenses(trip, sheet_manager)

        # Show the updated trip summary
        print(trip.summary())

        # Check if user wants to add another expense
        while True:
            print(Style.BRIGHT + "Do you want to add another expense?\n")
            yes_no_input = input(
                Style.BRIGHT +
                "✏️  Enter your decision here (yes/no): "
                )

            # Validate input
            if yes_no_input_valid(yes_no_input):
                print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
                break

        if yes_no_input == "no":
            break


def add_expenses(trip, sheet_manager):
    """
    Prompt the user to add or update an expense for a specific date in the
    trip.

    This function:
    - Asks the user to input a date within the trip range.
    - Checks if an expense already exists for that date and optionally updates
    it.
    - Prompts the user to input the expense amount.
    - Adds or updates the expense in the trip's expenses dictionary.
    - Sorts expenses by date.
    - Updates trip information and saves both trip info and expenses to the
    worksheet.

    Args:
        trip (Trip): The current Trip object containing trip info and expenses
        sheet_manager (object): Handles worksheet updates
    """
    # Get date input
    while True:
        print(
            Style.BRIGHT +
            "Please enter the date for which you want to add an expense."
            )
        print(
            "The expense date needs to be within your travel dates,"
            "\nbut cannot be a future date."
            )
        print("Format: YYYY-MM-DD")
        print("Example: 2025-08-01")
        print(
            "\nNote: If you enter a date that already exists in the database, "
            "then you\nyou will be able to update the expense for this date."
            )

        date_input = input(
            Style.BRIGHT +
            "\n✏️  Enter your expense date here: "
            )

        # Validate date input
        if expense_date_valid(date_input, trip):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
        else:
            continue

        # Check if the date already exists in the database
        if date_input in trip.expenses["date"]:
            old_date_index = trip.expenses["date"].index(date_input)
            old_amount = trip.expenses["amount"][old_date_index]
            # Ask user if they want to update the existing expense
            while True:
                print(
                    Style.BRIGHT +
                    f"You already submitted an expense of {old_amount} € "
                    f"for {date_input}.\n"
                    )
                print(Style.BRIGHT + "Do you want to update it?\n")
                yes_no_input = input(
                    Style.BRIGHT +
                    "✏️  Enter your decision here (yes/no): "
                    )

                # Validate input
                if yes_no_input_valid(yes_no_input):
                    print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
                    break

            if yes_no_input == "no":
                # Small pause + clear screen for better UX
                time.sleep(2)
                clear()
                # Exit without changing anything
                print("Okay, we will keep the old expense for this date.\n")
                return

        break  # Exit date input loop

    # Get amount input
    while True:
        print(Style.BRIGHT + f"How much did you spend on {date_input}?")
        print("Enter as a positive whole number in euros (no decimals).")
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
        update_amount = True
    else:
        # Add value in expenses dict if date doesn't exist yet
        trip.expenses["date"].append(date_input)
        trip.expenses["amount"].append(amount_input)
        update_amount = False

    # Sort dates, so that the expenses are saved and shown ordered by date
    # Zip dates and amounts together
    combined = list(zip(trip.expenses['date'], trip.expenses['amount']))
    # Sort by date (convert string to datetime to be able to order the dates)
    combined.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))
    # Unzip data back into dict
    trip.expenses['date'], trip.expenses['amount'] = map(list, zip(*combined))

    # Update trip_info dict with new expense data
    trip.update_trip_info()

    # Save new trip info and expenses to worksheet
    sheet_manager.update_worksheet(trip.trip_info, "trip_info")
    sheet_manager.update_worksheet(trip.expenses, "expenses")

    input(
            Style.BRIGHT +
            "\nPress ENTER to continue\n"
            )

    # Small pause + clear screen for better UX
    time.sleep(2)
    clear()

    # Print confirmation to user
    if update_amount:
        print(f"🎉  Updated expense for {date_input} ({amount_input} €).\n")
    else:
        print(f"🎉  Added new expense for {date_input} ({amount_input} €).\n")


def show_expenses_summary(trip):
    """
    Ask the user if they want to see a summary of all tracked expenses
    and display it if requested.

    This function:
    - Prompts the user with a yes/no question.
    - If 'yes', prints a formatted list of all expense dates and amounts.
    - If no expenses are recorded yet, informs the user accordingly.

    Args:
        trip (Trip): The current Trip object containing expense data.
    """
    # Ask if user wants to see the expenses summary
    while True:
        print(
            Style.BRIGHT +
            "Do you want to see a list of all currently tracked expenses?\n"
            )
        yes_no_input = input(
            Style.BRIGHT +
            "✏️  Enter your decision here (yes/no): "
            )

        # Validate input
        if yes_no_input_valid(yes_no_input):
            print(Fore.GREEN + Style.NORMAL + "Data is valid!\n")
            break

    # Display expenses
    if yes_no_input == "yes":
        print(Style.BRIGHT + "Here is a list of your current expenses:\n")
        if len(trip.expenses["date"]) == 0:
            print("⚠️  You haven't tracked any expenses yet.")
        else:
            print(f"{'Date':<15}{'Amount':>12}")
            print("-" * 27)
            for date, amount in zip(trip.expenses["date"],
                                    trip.expenses["amount"]):
                print(f"{date:<15}{amount:>10} €")

    else:
        # User chose not to view expenses
        print("Okay, let's move on.")


def main():
    """
    Main function that runs the Wander Wallet application.

    This function:
    - Welcomes the user and explains the app.
    - Checks if a trip already exists in the worksheet.
    - Prompts the user to continue the current trip or start a new one.
    - Shows trip summary and expense summary if requested.
    - Allows the user to add new expenses for the trip.
    - Ends the program with a summary and closing message if the trip hasn't
    started or after adding expenses.

    No arguments or return values.
    """
    # Welcome Message
    print(
        "\nWelcome to Wander Wallet — Your Personal Travel Expense Tracker\n\n"
        "This is a command-line app designed to help you manage your travel "
        "budget\nwhile you're on your trip.\nYou can track expenses day by "
        "day and get real-time updates on how your spending\naligns with "
        "your budget.\n"
        )
    print(
        "⏳  Checking if you have already started tracking "
        "travel expenses with us ..."
        )

    # Setup SheetManager
    creds_file = "creds.json"
    sheet_name = "wander_wallet"
    sheet_manager = SheetManager(creds_file, sheet_name)

    # Load trip data from worksheet
    trip_info = sheet_manager.get_worksheet_dict("trip_info")
    expenses = sheet_manager.get_worksheet_dict("expenses")

    today = datetime.now().date()

    # Check if a trip already exists
    trip_exists_answer = trip_exists(trip_info)
    if trip_exists_answer:
        # Load existing trip
        trip = Trip(trip_info, expenses)
        print(
            f"✅  Seems like you have been working on your trip "
            f"'{trip.trip_name}' already."
            )
        input(
            Style.BRIGHT +
            "\nPress ENTER to continue\n"
            )
        # Small pause + clear screen for better UX
        time.sleep(2)
        clear()

        # Show trip summary
        print(trip.summary())
        # Check if user wants to see a list of all currently tracked expenses
        show_expenses_summary(trip)

        # Ask if user wants to continue current trip
        continue_trip_val = continue_trip()

        # If user starts a new trip, delete old data and initialize new trip
        if not continue_trip_val:
            sheet_manager.del_worksheet_data("trip_info")
            sheet_manager.del_worksheet_data("expenses")
            # Set up new trip_info and expenses objects
            trip_info = sheet_manager.get_worksheet_dict("trip_info")
            expenses = sheet_manager.get_worksheet_dict("expenses")
            # Start new trip
            trip = start_new_trip(expenses, sheet_manager)
    else:
        # No existing trip, start a new one
        trip = start_new_trip(expenses, sheet_manager)

    # Check if the trip has already started, if not, end the program
    if trip.start_date > today:
        print("🎉  Thank you for setting up your trip with Wander Wallet!\n")
        print("Your trip hasn't started yet.")
        print(
            "Return to Wander Wallet once your trip starts and you want "
            "to start\ntracking expenses!\n\n"
            )
        print("End of program")
        return
    else:
        print(
            f"Great! Your trip has already started "
            f"({trip.start_date} - {trip.end_date})!\n"
            f"Let's start adding some expenses.\n"
            )

    # Get new expense from user and check if they want to add another one
    get_new_expense(trip, sheet_manager)

    # Continue when user finished adding expenses
    # Small pause + clear screen for better UX
    time.sleep(2)
    clear()
    # Check if user wants to see a list of all currently tracked expenses
    show_expenses_summary(trip)

    # Add an empty input forcing the app to pause before showing the
    # summary in the next step
    input(
        Style.BRIGHT +
        "\nPress ENTER to continue to your trip summary and "
        "end the program\n"
        )
    # Small pause + clear screen for better UX
    time.sleep(2)
    clear()

    # Show trip summary and then end the program
    print(trip.summary())
    print("\n🎉  Thank you for using Wander Wallet!\n")
    print(
        "Come back to this app to add some more expenses to "
        "your trip or\nset up a new one! See you next time!\n\n"
        )
    print("End of program")

    return


"""
Entry point for the Wander Wallet application.

This ensures that the main program loop runs only when this file is executed
directly, not when it is imported as a module elsewhere.
"""
# Run main loop only if the script is launched directly
if __name__ == "__main__":
    # Clear console to remove startup output for cleaner UX
    clear()

    # Run the main program loop with automatic restart on unexpected errors
    while True:
        try:
            main()
            # Exit loop if main function finishes without error
            break
        except Exception as e:
            print(Fore.RED + Style.NORMAL + "\nAn unexpected error occurred.")
            print(Fore.RED + Style.NORMAL + f"Details: {e}\n")
            print(Fore.RED + Style.NORMAL + "We will restart the app for you.")
            # Restart app if main function throws an unhandled error
            continue
