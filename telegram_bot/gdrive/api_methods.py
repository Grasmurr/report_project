import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_sheet(list_name):

    creds = service_account.Credentials.from_service_account_file(
        '/usr/src/telegram_bot/gdrive/assets/refined-veld-380115-d8a66c99ae72.json'
    )

    service = build('sheets', 'v4', credentials=creds)
    sheet_id = '1TGKgdCyKEx2cwhlchEwadg5cUSYVBmT6PoO7QnLeq8A'
    name_of_list = list_name
    request_body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": name_of_list,
                        "gridProperties": {
                            "rowCount": 100,
                            "columnCount": 26
                        }
                    }
                }
            }
        ]
    }
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body=request_body
        ).execute()
    except HttpError:
        print('Лист уже существует')


def format_data_for_google_sheets(data):
    headers = [
        "ID", "Event", "Ticket Number", "Имя",
        "Фамилия", "Тип билета", "Дата рождения",
        "Цена", "Программа обучения", "Курс", "Номер телефона"
    ]

    rows = [[
        item["id"], item["event"], item["ticket_number"],
        item["ticket_holder_name"], item["ticket_holder_surname"],
        item["ticket_type"], item["date_of_birth"], item["price"],
        item["educational_program"], item["educational_course"], item["phone_number"]
    ] for item in data["data"]]

    formatted_data = [headers] + rows
    return formatted_data


async def update_gdrive(list_name, data):
    creds = service_account.Credentials.from_service_account_file(
        '/usr/src/telegram_bot/gdrive/assets/refined-veld-380115-d8a66c99ae72.json'
    )

    formatted_data = format_data_for_google_sheets(data)

    service = build('sheets', 'v4', credentials=creds)
    sheet_id = '1TGKgdCyKEx2cwhlchEwadg5cUSYVBmT6PoO7QnLeq8A'
    name_of_list = list_name
    sheet_range = f'{name_of_list}!A1'
    request = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=sheet_range,
        valueInputOption='RAW',
        body={'values': formatted_data}
    )
    response = request.execute()
    print(f'Updated {response["updatedCells"]} cells in Google Sheets')
