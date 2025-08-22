from datetime import datetime
import re
from colorama import Fore, Style, init

# Initialize Colorama (colors reset automatically after each print)
init(autoreset=True)


def new_trip_info_valid(data_input, data_type):
    """
    Validate new trip information input depending on the type of data provided.

    Supported data types:
        - "trip_name": Must be 1–30 characters long, alphanumeric + spaces
        only
        - "trip_dates": Must contain exactly two valid dates (YYYY-MM-DD),
                        separated by a comma. The start date must be before
                        the end date, and the end date must be in the future
        - "trip_budget": Must be a positive integer (validated via
        int_input_valid)

    Args:
        data_input (str | list): User input (string for trip_name and budget,
                                 list of two strings for trip_dates).
        data_type (str): The type of data being validated
                         ("trip_name", "trip_dates", or "trip_budget").

    Returns:
        bool: True if the input is valid, False otherwise
    """
    if data_type == "trip_name":
        try:
            if len(data_input) > 30 or len(data_input) < 1:
                raise ValueError(
                    f"Min. 1 and not more than 30 characters allowed,\n"
                    f"you provided {len(data_input)}"
                )
            if not re.fullmatch(r"[A-Za-z0-9 ]+", data_input):
                raise ValueError(
                    "Trip name can only contain letters (A–Z), numbers (0–9)\n"
                    "and spaces"
                )
        except ValueError as e:
            print(
                Fore.RED +
                Style.NORMAL +
                f"Invalid data: {e}, please try again.\n"
                )
            return False

        return True

    if data_type == "trip_dates":
        try:
            # Check if provided strings can be transformed to a datetime object
            datetime_input = []
            for date_str in data_input:
                try:
                    datetime_input.append(
                        datetime.strptime(date_str, "%Y-%m-%d").date()
                        )
                except ValueError:
                    # Custom message for invalid date format
                    # Set up custom message because "YYYY-MM-DDD" triggers a
                    # different warning than e.g. "YYYY-MMM-DD" or "hello"
                    # Also get triggered if a wrong seperator has been used
                    raise ValueError(
                        f"'{date_str}'\nMake sure you provide two dates that "
                        f"are seperated by ','.\nDates must exist and be in "
                        f"the format 'YYYY-MM-DD'"
                        )

            # Check if exactly two dates have been submitted
            if len(data_input) != 2:
                raise ValueError(
                    f"Exactly two dates are expected, you provided "
                    f"{len(data_input)}"
                )

            # Check if end date is later than start date
            start_date = datetime_input[0]
            end_date = datetime_input[1]
            if end_date <= start_date:
                raise ValueError(
                    "Your start date needs to be at least one day before "
                    "your\nend date"
                )

            # Check if end date is in the future
            today = datetime.now().date()
            if today > end_date:
                raise ValueError(
                    "Your trip end date needs to be in the future"
                )

        except ValueError as e:
            print(
                Fore.RED +
                Style.NORMAL +
                f"Invalid data: {e}, please try again.\n"
                )
            return False

        return True

    if data_type == "trip_budget":
        return int_input_valid(data_input)


def int_input_valid(data_input):
    """
    Validate if the given input is a positive integer.

    Checks performed:
    1. Ensures the input can be converted into an integer
    2. Ensures the integer is strictly greater than zero

    Args:
        data_input (str): The user input string

    Returns:
        bool: True if the input is a valid positive integer,
              False otherwise
    """
    try:
        # Check if provided string can be transformed to an int object
        try:
            int_input = int(data_input)
        except ValueError:
            raise ValueError(
                f"Your input '{data_input}' is not a whole number"
                )

        # Check if provided integer is positive
        if int_input <= 0:
            raise ValueError(
                "The value must be larger than 0"
            )
    except ValueError as e:
        print(
            Fore.RED +
            Style.NORMAL +
            f"Invalid data: {e}, please try again.\n"
            )
        return False

    return True


def yes_no_input_valid(data_input):
    """
    Validate user input for yes/no questions.

    Checks performed:
    1. Converts input to lowercase for consistency
    2. Ensures that the input is strictly 'yes' or 'no'

    Args:
        data_input (str): The user input string

    Returns:
        bool: True if the input is valid ('yes' or 'no'), False otherwise
    """
    try:
        # Transform input to lowercase (e.g. "Yes" -> "yes")
        data_input_val = data_input.lower()
        # Only "yes" or "no" are accepted
        if data_input_val not in ["yes", "no"]:
            raise ValueError(
                f"'yes' or 'no' expected, you provided '{data_input_val}'"
                )
    except ValueError as e:
        print(
            Fore.RED +
            Style.NORMAL +
            f"Invalid data: {e}, please try again.\n"
            )
        return False

    return True


def expense_date_valid(date_input, trip):
    """
    Validate if a user-provided expense date is correct and usable.

    Checks performed:
    1. Ensures the input can be converted to a valid date in the format
    YYYY-MM-DD
    2. Ensures the date falls within the trip period
    3. Ensures the date is not set in the future

    Args:
        date_input (str): The user input string representing the date
        trip (Trip): The Trip object

    Returns:
        bool: True if the date is valid, False otherwise
    """
    try:
        # Check if provided string can be transformed to a datetime object
        try:
            expense_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            # Custom message for invalid date format
            # Set up custom message because "YYYY-MM-DDD" triggers a
            # different warning than e.g. "YYYY-MMM-DD" or "hello"
            raise ValueError(
                f"'{date_input}'. "
                f"Date must exist and be in the format\nYYYY-MM-DD"
                )

        # Check if date is within travel period
        if expense_date < trip.start_date or expense_date > trip.end_date:
            raise ValueError(
                f"Your expense date needs to be within your travel "
                f"period\n{trip.start_date} - {trip.end_date}"
            )

        # Check if date is not in the future
        today = datetime.now().date()
        if expense_date > today:
            raise ValueError(
                "Your expense date cannot be a future date"
            )
    except ValueError as e:
        print(
            Fore.RED +
            Style.NORMAL +
            f"Invalid data: {e}, please try again.\n"
            )
        return False

    return True
