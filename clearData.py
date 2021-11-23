import time
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials 

def clearData():
  # Read Google Spreadsheets
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
  gc = gspread.authorize(credentials)

  df_mentee_clear = pd.read_csv("mentees_clear.csv", sep = ";")
  df_mentor_clear = pd.read_csv("mentors_clear.csv", sep = ";")
  
  test_spreadsheet_id = '14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  d2g.upload(df_mentee_clear, test_spreadsheet_id, 'Test_mentee', credentials=credentials, row_names = False)
  d2g.upload(df_mentor_clear, test_spreadsheet_id, 'Test_mentor', credentials=credentials, row_names = False)
  d2g.upload(df_mentee_clear, test_spreadsheet_id, 'Rejected_mentees', credentials=credentials, row_names = False)
  d2g.upload(df_mentor_clear, test_spreadsheet_id, 'Rejected_mentors', credentials=credentials, row_names = False)
  d2g.upload(df_mentee_clear, test_spreadsheet_id, 'Preselected_mentees', credentials=credentials, row_names = False)
  d2g.upload(df_mentor_clear, test_spreadsheet_id, 'Preselected_mentors', credentials=credentials, row_names = False)

  print('Data cleared\n20 seconds cooldown')
  time.sleep(20)