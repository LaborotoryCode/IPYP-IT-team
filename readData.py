import time
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

# Read Google Spreadsheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(credentials)

# For mentees

def read_rawMentees():
  mentee_spreadsheet_id='14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{mentee_spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Test_mentee")

  print('Raw Mentees read')
  print('20 sec cooldown')
  time.sleep(20)
  return df
  
def read_preMentees():
  mentee_spreadsheet_id='14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{mentee_spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Preselected_mentees")

  print('Preselected Mentees read')
  print('20 sec cooldown')
  time.sleep(20)
  return df

def read_rejMentees():
  mentee_spreadsheet_id='14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{mentee_spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Rejected_mentees")
  
  print('Rejected Mentees read')
  print('20 sec cooldown')
  time.sleep(20)
  return df

#For mentor

def read_rawMentors():
  mentor_spreadsheet_id='14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{mentor_spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Test_mentor")

  print('Raw Mentors read')
  print('20 sec cooldown')
  time.sleep(20)
  return df
  
def read_preMentors():
  mentor_spreadsheet_id='14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{mentor_spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Preselected_mentors")

  print('Preselected Mentors read')
  print('20 sec cooldown')
  time.sleep(20)
  return df

def read_rejMentors():
  mentor_spreadsheet_id='14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{mentor_spreadsheet_id}/gviz/tq?tqx=out:csv&sheet=Rejected_mentors")
  
  print('Rejected Mentors read')
  print('20 sec cooldown')
  time.sleep(20)
  return df