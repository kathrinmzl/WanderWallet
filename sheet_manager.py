import gspread
from google.oauth2.service_account import Credentials


class SheetManager:
    """
    Manages interaction with a Google Spreadsheet.

    This class handles authentication with the Google Sheets API and provides
    methods to:
    - Retrieve worksheet data as a dictionary
    - Delete all worksheet data except headers
    - Update worksheets with new trip or expense data
    """
    def __init__(self, creds_file: str, sheet_name: str):
        # Define the scope of access for the Google Sheets API
        SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        # Load service account credentials from the given file
        CREDS = Credentials.from_service_account_file(creds_file)
        # Apply scope permissions to credentials
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        # Authorize gspread client with the scoped credentials
        self.client = gspread.authorize(SCOPED_CREDS)
        # Open the Google Spreadsheet by name
        self.sheet = self.client.open(sheet_name)

    def get_worksheet_dict(self, worksheet_name: str) -> dict:
        """
        Retrieve all data from a worksheet and return it as a dictionary.
        """
        # Open the specific worksheet by name
        sheet = self.sheet.worksheet(worksheet_name)
        sheet_list = sheet.get_all_values()

        if worksheet_name == "trip_info":
            # If trip_info worksheet has exactly one row of data
            if len(sheet_list) == 2:
                keys, values = sheet_list
                sheet_dict = dict(zip(keys, values))
            else:
                # Only headers exist: initialize dict with empty strings
                sheet_dict = dict.fromkeys(sheet_list[0], "")

        else:  # "expenses"
            # Extract column headers ['date', 'amount']
            keys = sheet_list[0]
            # Extract all data rows
            # e.g. [['2025-08-20', '12'], ['2025-08-21', '34']]
            rows = sheet_list[1:]
            # Create dict with list comprehensions
            sheet_dict = {
                key: [row[i] for row in rows] for i, key in enumerate(keys)
                }

        return sheet_dict

    def del_worksheet_data(self, worksheet_name: str):
        """
        Delete all data from a worksheet, except the headings
        """
        print(f"⏳  Deleting data from {worksheet_name} worksheet...\n")
        sheet = self.sheet.worksheet(worksheet_name)
        n_rows = sheet.row_count
        # Only delete rows if there is data beyond the header
        if n_rows >= 2:
            sheet.delete_rows(2, n_rows)
        print(f"✅  {worksheet_name} worksheet updated successfully.\n")

    def update_worksheet(self, data: dict, worksheet_name: str):
        """
        Update a worksheet with new data.
        - For "trip_info", add one row with trip details
        - For "expenses", add multiple rows with date/amount pairs
        """
        print(f"⏳  Updating {worksheet_name} worksheet...\n")
        sheet = self.sheet.worksheet(worksheet_name)
        # First delete old data
        n_rows = sheet.row_count
        # Delete_rows only works if the rows actually exist
        if n_rows >= 2:
            sheet.delete_rows(2, n_rows)
        # Then add new data
        if worksheet_name == "trip_info":
            row_list = list(data.values())
            sheet.append_row(row_list)
        else:  # worksheet_name = "expenses"
            dates = data.get("date", [])
            amounts = data.get("amount", [])
            row_list = list(zip(dates, amounts))
            sheet.append_rows(row_list)

        print(f"✅  {worksheet_name} worksheet updated successfully.\n")
