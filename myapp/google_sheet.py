import gspread
from oauth2client.service_account import ServiceAccountCredentials 
import os

def google_sheet(sheet_id):
    credentials_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    scopes = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scopes)
    gss_client = gspread.authorize(creds)
    sheet = gss_client.open_by_key(sheet_id).sheet1
    return sheet