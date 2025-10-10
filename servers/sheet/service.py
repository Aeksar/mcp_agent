from __future__ import print_function
from typing import List, Any
import os.path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from base import SheetService

class GoogleSheetService(SheetService):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, spreadsheet_id: str, range_name: str, credentials_file="credentials.json", token_file="token.json"):
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.service = None
        self._authenticate()

    # ---------- Авторизация ----------
    def _authenticate(self):
        """Авторизация и создание клиента Google Sheets API."""
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_file, "w") as token:
                token.write(self.creds.to_json())

        self.service = build("sheets", "v4", credentials=self.creds)

    # ---------- Методы интерфейса ----------
    def get_data(self) -> List[List[Any]]:
        """Возвращает данные из указанного диапазона."""
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.range_name).execute()
        values = result.get("values", [])
        return values or []

    def set_data(self, data: List[List[Any]]):
        """Заменяет данные в диапазоне."""
        body = {"values": data}
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        return {"message": "Data successfully set"}

    def append_data(self, data: List[List[Any]]):
        """Добавляет строки в конец таблицы."""
        body = {"values": data}
        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        return {"message": "Data appended"}

    def clear_data(self):
        """Очищает диапазон данных."""
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name,
            body={}
        ).execute()
        return {"message": "Data cleared"}
    

if __name__ == "__main__":
    # Пример использования
    SHEET_ID = "1MMMMlokYvOO_jW7L40WrzNvAO3hUbK_fPGaodSrmzsc"
    RANGE = "Лист1!A1:C5"

    service = GoogleSheetService(SHEET_ID, RANGE)
    
    # Пример записи
    service.set_data([["Имя", "Возраст"], ["Александр", 29]])
    
    # Добавление новой строки
    service.append_data([["Ольга", 24]])
    
    # Получение данных
    print(service.get_data())