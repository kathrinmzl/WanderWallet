import gspread
from google.oauth2.service_account import Credentials


class SheetManager:
    """
    Sheet Manager ....
    """
    def __init__(self, creds_file: str, sheet_name: str):
        SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
            ]
        CREDS = Credentials.from_service_account_file(creds_file)
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
        self.client = gspread.authorize(SCOPED_CREDS)
        self.sheet = self.client.open(sheet_name)

    def get_worksheet_dict(self, worksheet_name: str) -> dict:
        """
        Return worksheet data as a dict with header names as keys and column values as lists.
        """
        sheet = self.sheet.worksheet(worksheet_name)
        sheet_list = sheet.get_all_values()
        
        if worksheet_name == "trip_info":
            if len(sheet_list) == 2:
                keys, values = sheet_list
                sheet_dict = dict(zip(keys, values))
            else:  # only headings
                sheet_dict = dict.fromkeys(sheet_list[0], "")
            
        else:  # "expenses"
            # Extract keys and rows
            keys = sheet_list[0]       # ['date', 'amount']
            rows = sheet_list[1:]      # [['2025-08-20', '12'], ['2025-08-20', '34']]
            # Create dict with list comprehensions
            sheet_dict = {key: [row[i] for row in rows] for i, key in enumerate(keys)}

        return sheet_dict 
        
    def del_worksheet_data(self, worksheet_name: str):
        """
        Delete all data from a worksheet, except the headings
        """
        print(f"⏳  Deleting data from {worksheet_name} worksheet...\n")
        sheet = self.sheet.worksheet(worksheet_name)
        n_rows = sheet.row_count
        # delete_rows only works if the rows actually exist
        if n_rows >= 2:
            sheet.delete_rows(2, n_rows)
        print(f"✅  {worksheet_name} worksheet updated successfully.\n")

    def update_worksheet(self, data: dict, worksheet_name: str):
        """
        Update worksheet "sheetname", add new row with the list data provided
        """
        print(f"⏳  Updating {worksheet_name} worksheet...\n")
        sheet = self.sheet.worksheet(worksheet_name)
        # First delete old data
        n_rows = sheet.row_count
        # delete_rows only works if the rows actually exist
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
        