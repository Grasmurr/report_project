import gspread
from google.oauth2.service_account import Credentials


def authenticate_google_sheets():
    creds = Credentials.from_service_account_file(
        'myapi/myapp/assets/refined-veld-380115-d8a66c99ae72.json',
        scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )
    client = gspread.authorize(creds)
    return client


def export_data_to_google_sheets(data):
    client = authenticate_google_sheets()
    sheet = client.open("Your Spreadsheet Name").sheet1
    for row in data:
        sheet.append_row(row)


def create_google_sheet(sheet_title):
    client = authenticate_google_sheets()
    sheet = client.create(sheet_title)
    return sheet