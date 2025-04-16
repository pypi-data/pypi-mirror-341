import pandas
import gspread
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound
from pathlib import Path

def open_spreadsheet(spreadsheet: str,
                     credential: str | Path) -> gspread.Spreadsheet:
    """
    Opens a Google Spreadsheet using the given service account credentials.

    Args:
        spreadsheet (str): The name of the Google Spreadsheet to open.
        credential (str | Path): Path to the JSON credential file for Google API authentication.

    Returns:
        gspread.Spreadsheet: The opened Spreadsheet object, allowing further operations.

    Raises:
        gspread.exceptions.SpreadsheetNotFound: If the spreadsheet name is incorrect or inaccessible.
        FileNotFoundError: If the credential file is missing.
        ValueError: If authentication fails due to invalid credentials.
    """

    # Ensure the credential file exists
    credential = Path(credential)
    if not credential.exists():
        raise FileNotFoundError(f"Credential file not found: {credential}")

    # Define API scopes
    scope = ["https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive"]

    try:
        # Load credential to authenticate with Google Sheets        
        client = gspread.service_account(credential)

        # Open and return the spreadsheet object
        return client.open(spreadsheet)

    except SpreadsheetNotFound:
        raise SpreadsheetNotFound(f"Spreadsheet '{spreadsheet}' not found or inaccessible.")
    
    except Exception as e:
        raise ValueError(f"An error occurred while opening the spreadsheet: {e}")        

def get_sheet_to_dataframe(sheet: str,
                           spreadsheet: str,
                           credential: str | Path) -> pandas.DataFrame:
    """
    Retrieves data from a specific worksheet in a Google Spreadsheet and returns it as a pandas DataFrame.

    Args:
        sheet (str): The name of the worksheet to retrieve.
        spreadsheet (str): The name of the Google Spreadsheet to open.
        credential (str | Path): Path to the JSON credential file for Google API authentication.

    Returns:
        pandas.DataFrame: A DataFrame containing the worksheet data.

    Raises:
        FileNotFoundError: If the credential file is missing.
        gspread.exceptions.SpreadsheetNotFound: If the spreadsheet is incorrect or inaccessible.
        gspread.exceptions.WorksheetNotFound: If the worksheet name is incorrect.
        ValueError: If data retrieval fails.
    """

    try:
        # Open the spreadsheet
        spreadsheet_obj = open_spreadsheet(spreadsheet=spreadsheet, credential=credential)

        # Open the worksheet
        worksheet = spreadsheet_obj.worksheet(sheet)

        # Get all data from the worksheet
        data = worksheet.get_all_records()

        # Convert to pandas DataFrame
        df = pandas.DataFrame(data, index=None)

        return df

        
    except WorksheetNotFound:
        raise WorksheetNotFound(f"Worksheet '{sheet}' not found in '{spreadsheet}'.")
        
    except Exception as e:
        raise ValueError(f"An error occurred while retrieving the worksheet: {e}")

def get_spreadsheet(
    spreadsheet: str,
    credential: str | Path
) -> dict[str, pandas.DataFrame]:

    try:
        # Open the spreadsheet
        spreadsheet_obj = open_spreadsheet(spreadsheet=spreadsheet, credential=credential)

        spreadsheet_dict = {}
        for worksheet in spreadsheet_obj.worksheets():            
            # Get all data from the sheet
            data = worksheet.get_all_records()
    
            # Convert to pandas.DataFrame
            df = pandas.DataFrame(data, index=None)

            spreadsheet_dict[worksheet.title] = df

        return spreadsheet_dict

    except SpreadsheetNotFound:
        raise SpreadsheetNotFound(f"Spreadsheet '{spreadsheet}' not found or inaccessible.")
    
    except Exception as e:
        raise ValueError(f"An error occurred while opening the spreadsheet: {e}")

def sheet_exists(sheet: str, 
                 spreadsheet: gspread.Spreadsheet) -> bool:
    """
    Checks if a worksheet exists in a given Google Spreadsheet.

    Args:
        spreadsheet (gspread.Spreadsheet): The Google Spreadsheet object.
        sheet (str): The name of the worksheet to check.

    Returns:
        bool: True if the worksheet exists, False otherwise.
    """
    try:
        spreadsheet.worksheet(sheet)
        return True
    except WorksheetNotFound:
        return False

def upload_dataframe_to_spreadsheet(df: pandas.DataFrame,
                                    sheet: str,
                                    spreadsheet: str,
                                    credential: str | Path,
                                    formatting: bool = True) -> None:
    """
    Uploads a pandas DataFrame to a newly created formatted worksheet in a Google Spreadsheet.

    This function creates a new worksheet in the specified Google Spreadsheet and uploads the data
    from the provided DataFrame. If the DataFrame is empty, or if a worksheet with the specified name
    already exists, the function raises a ValueError. Optional formatting can be applied to the worksheet
    after data upload:
    - Bold formatting is applied to the header row.
    - All cells in columns A to Z are set to clip text wrapping.
    - The first row is frozen to keep the headers visible during scrolling.

    Args:
        df (pandas.DataFrame): The DataFrame to upload.
        sheet (str): The name of the worksheet to create and upload data to.
        spreadsheet (str): The name of the Google Spreadsheet to open.
        credential (str | Path): The path to the JSON credential file for Google API authentication.
        formatting (bool, optional): Whether to apply formatting to the worksheet after upload.
                                     Defaults to True.

    Raises:
        FileNotFoundError: If the credential file is missing.
        gspread.exceptions.SpreadsheetNotFound: If the spreadsheet is incorrect or inaccessible.
        ValueError: If the worksheet already exists or the DataFrame is empty.
        Exception: If an unexpected error occurs.

    Returns:
        None
    """

    try:
        # Open the spreadsheet
        spreadsheet_obj = open_spreadsheet(spreadsheet=spreadsheet, credential=credential)

        # Check if the worksheet already exists
        if sheet_exists(spreadsheet=spreadsheet_obj, sheet=sheet):
            
            raise ValueError(f"Error: Worksheet '{sheet}' already exists in '{spreadsheet}'.")

        # Ensure DataFrame is not empty
        if df.empty:
            raise ValueError("Error: The DataFrame is empty. Cannot upload an empty worksheet.")

        # Replace NaN values with an empty string
        df = df.fillna('')

        # Create a new worksheet
        worksheet = spreadsheet_obj.add_worksheet(title=sheet, rows="1", cols="1")

        # Convert DataFrame to list format
        data_to_write = [df.columns.values.tolist()] + df.values.tolist()
        
        # Write data to Google Sheets (starting from cell A1)
        worksheet.update(data_to_write, raw=False)

        if formatting:    
            # Get the sheet ID for formatting
            sheet_id = worksheet._properties["sheetId"]
    
            worksheet.format("A1:Z1",
                             {
                                 'textFormat': {'bold': True},
                             })
    
            worksheet.format("A:Z",
                             {
                                 "wrapStrategy": "CLIP"
                             })
    
            # Request to freeze the first row
            freeze_request = {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "gridProperties": {"frozenRowCount": 1}
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
            }
            
        
            # Send batch update request with separate operations
            spreadsheet_obj.batch_update({"requests": [freeze_request]})        

        print(f"Successfully uploaded pandas.DataFrame to new worksheet '{sheet}' in '{spreadsheet}'.")

    except ValueError as ve:
        print(ve)  # Handles worksheet existence and empty DataFrame errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def append_dataframe_to_sheet(
    df: pandas.DataFrame,
    sheet: str,
    spreadsheet: str,
    credential: str | Path,
    duplicates: bool = False
) -> None:
    """
    Appends new rows from a pandas DataFrame to an existing worksheet in a Google Spreadsheet.

    Args:
        df (pandas.DataFrame): The DataFrame containing the new rows to append.
        sheet (str): The name of the worksheet to append data to.
        spreadsheet (str): The name of the Google Spreadsheet.
        credential (str | Path): The path to the JSON credential file for Google API authentication.

    Raises:
        ValueError: If the worksheet does not exist or the DataFrame is empty.
    
    Returns:
        None
    """

    try:
        # Open the spreadsheet
        spreadsheet_obj = open_spreadsheet(spreadsheet=spreadsheet, credential=credential)

        if df.empty:
            raise ValueError("Error: The pandas.DataFrame is empty. Cannot append empty data. Verify the pandas.DataFrame.")

        # Check if the worksheet exists
        if not sheet_exists(sheet=sheet, spreadsheet=spreadsheet_obj):
            raise ValueError(f"Error: Worksheet '{sheet}' does not exist in '{spreadsheet}'.")

        # Replace NaN values with an empty string
        df = df.fillna('')

        # Open the existing worksheet
        worksheet = spreadsheet_obj.worksheet(sheet)

        # Get actual sheet data
        all_sheet_data = worksheet.get_all_values()
        if not all_sheet_data:
            raise ValueError(f"Error: The sheet {sheet} appears to be empty and has no header row.")

        # Get sheet headers
        existing_headers = all_sheet_data[0]

        # Get sheet rows data
        existing_rows = {tuple(row) for row in all_sheet_data[1:]}        

        data_to_append = []
        for row in df.to_dict(orient="records"):
            new_row = [row.get(header, "") for header in existing_headers]

            if not duplicates:
                if tuple(new_row) not in existing_rows:
                    data_to_append.append(new_row)

            else:
                data_to_append.append(new_row)

        worksheet.append_rows(data_to_append)

        print(f"Successfully appended `df` pd.DataFrame to '{sheet}' in '{spreadsheet}' spreadshet.")

    except ValueError as ve:
        print(str(ve))  # Handles worksheet existence and empty DataFrame errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")