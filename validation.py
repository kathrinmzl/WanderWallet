from datetime import datetime


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
        return int_input_valid(data_input)

    
def int_input_valid(data_input):
    try:
        # Check if provided string can be transformed to an int object
        int(data_input)
    except ValueError:
        print("\nInvalid data: Your input is not a whole number, please try again.\n")
        return False
    
    return True


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


def expense_date_valid(date_input, trip):
    """
    Check if expense date input is valdid
    """
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
        return False
    
    return True

