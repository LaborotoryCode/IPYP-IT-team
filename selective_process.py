import time
from datetime import date 
import pandas as pd
import gspread
import readData as rD
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

'''
CHECK
2.1. Over 13
2.2. Do they have B2 English proficiency or above?
2.3. Is their availability time al least [idk] hours a week?
2.4. Is their paragraph's score equal or more than [idk] points? 
'''

# Read the imported csvs
def read():
  global df_mentee_raw
  global df_mentor_raw
  df_mentee_raw = rD.read_rawMentees()
  df_mentor_raw = rD.read_rawMentors()

  print("Columnas:",len(df_mentee_raw.columns))
  print("Columnas:",len(df_mentor_raw.columns))

  # Add new columns to the dfs and sort
  # Later on this will be used to correct the schedules

  #Mentees
  for i in range(6):
    df_mentee_raw[f'List ALL the days and times you would have available to learn. [0{i}:00]'] = ""
    df_mentee_raw[f'List ALL the days and times you would have available to learn. [0{i}:30]'] = ""
  
  cols = list(df_mentee_raw.columns)

  index = df_mentee_raw.columns.get_loc('List ALL the days and times you would have available to learn. [06:00]')
  # Sort the columns
  # df_mentee_raw = df_mentee_raw[cols[0:index] + cols[-6:] + cols[index:-6]]

  df_mentee_raw["List ALL the days and times you would have available to learn. [22:30]"] = ""
  df_mentee_raw["List ALL the days and times you would have available to learn. [23:00]"] = ""
  df_mentee_raw["List ALL the days and times you would have available to learn. [23:30]"] = ""

  index = df_mentee_raw.columns.get_loc('List ALL the days and times you would have available to learn. [22:00]')
  # Sort the columns
  # df_mentee_raw = df_mentee_raw[cols[0:index] + cols[-3:] + cols[index:-3]]
  
  #Mentors
  for i in range(6):
    df_mentor_raw[f'List ALL the days and times you would have available to teach. [0{i}:00]'] = ""
    df_mentor_raw[f'List ALL the days and times you would have available to teach. [0{i}:30]'] = ""
  
  cols = list(df_mentor_raw.columns)

  index = df_mentor_raw.columns.get_loc('List ALL the days and times you would have available to teach. [06:00]')
  # Sort the columns
  # df_mentor_raw = df_mentor_raw[cols[0:index] + cols[-6:] + cols[index:-6]]

  df_mentor_raw["List ALL the days and times you would have available to teach. [22:30]"] = ""
  df_mentor_raw["List ALL the days and times you would have available to teach. [23:00]"] = ""
  df_mentor_raw["List ALL the days and times you would have available to teach. [23:30]"] = ""

  index = df_mentor_raw.columns.get_loc('List ALL the days and times you would have available to teach. [22:00]')
  
  # Sort the columns
  # df_mentor_raw = df_mentor_raw[cols[0:index] + cols[-3:] + cols[index:-3]]

  print("Columnas:",len(df_mentee_raw.columns))
  print("Columnas:",len(df_mentor_raw.columns))
  time.sleep(20)

  global df_preselected_mentees
  global df_preselected_mentors
  global df_rejected_mentees
  global df_rejected_mentors

  df_preselected_mentees = rD.read_preMentees()
  df_preselected_mentors = rD.read_preMentors()
  df_rejected_mentees = rD.read_rejMentees()
  df_rejected_mentors = rD.read_rejMentors()

# Returns the age of the applicant
def calculateAge(bday, limit):
  age = limit.year - bday.year
  if limit.month == bday.month:
    if limit.day < bday.day:
      age -= 1
  if limit.month < bday.month:
    age -= 1
  return age

# Returns an array converted to string 
def list_to_string(l):
  str1 = ""  
  str1 = ",".join(l)
  return (str1)

# Converts the days according to the GMT
week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
def change_day(day,next):
  temp_index = week.index(day)
  
  # Converts to next day if true
  if next:
    if (temp_index + 1) >= len(week):
      temp_index -= len(week)
    temp_index += 1

  # else to the previous one
  else:
    if (temp_index - 1) < 0:
     temp_index += len(week)
    temp_index -= 1

  return week[temp_index]

df_schedule=pd.DataFrame()

def upload():
  # license
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
  credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
  gc = gspread.authorize(credentials)

  test_spreadsheet_id = '14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  d2g.upload(df_rejected_mentees, test_spreadsheet_id, 'Rejected_mentees', credentials=credentials, row_names = False)
  d2g.upload(df_rejected_mentors, test_spreadsheet_id, 'Rejected_mentors', credentials=credentials, row_names = False)
  d2g.upload(df_preselected_mentees, test_spreadsheet_id, 'Preselected_mentees', credentials=credentials, row_names = False)
  d2g.upload(df_preselected_mentors, test_spreadsheet_id, 'Preselected_mentors', credentials=credentials, row_names = False)
  
  df_preselected_mentees.to_csv('preMentee.csv', sep=';', na_rep='', index=False)
  df_preselected_mentors.to_csv('preMentor.csv', sep=';', na_rep='', index=False)

def evaluate(iMentee, iMentor):
  print('Evaluating...')
  time.sleep(20)

  # Read the csvs
  read()
  
  # Parameters
  # Minimun age by the beginning of the project
  beginning_date = date(2022, 2, 1)

  for e in range(iMentee, len(df_mentee_raw.index)):
    print(df_mentee_raw.iloc[e,2])
    
    # 1. Check the minum age 13
    bday = date(int((df_mentee_raw.iloc[e,4])[-4:]), int((df_mentee_raw.iloc[e,4])[3:5]), int((df_mentee_raw.iloc[e,4])[:2]))
    if calculateAge(bday,beginning_date) < 13:
      print(f'rejected by age {calculateAge(bday,beginning_date)}')
      # Add to the rejected group
      df_mentee_raw.iloc[e,0] = f'rejected by age {calculateAge(bday,beginning_date)}'
      df_rejected_mentees.loc[len(df_rejected_mentees.index)] = df_mentee_raw.iloc[e]
      continue
    
    # 2. Check if they have a B2 proficiency level
    if df_mentee_raw.iloc[e,11] != "Yes" :
      print(f'rejected by English level {df_mentee_raw.iloc[e,11]}')
      # Add to the rejected group
      df_mentee_raw.iloc[e,0] = f'rejected by English level {df_mentee_raw.iloc[e,11]}'
      df_rejected_mentees.loc[len(df_rejected_mentees.index)] = df_mentee_raw.iloc[e]
      continue
    
    # 3. Check their minimun availability
    availabilityCounter = 0
    schedule_begin_index = 28
    for i in range(schedule_begin_index, schedule_begin_index + 33):
      if not isinstance(df_mentee_raw.iloc[e,i], float): 
        availabilityCounter += len(df_mentee_raw.iloc[e,i].split(', '))

    if availabilityCounter < 2 * 3:
      print(f'rejected by low availability {availabilityCounter}')
      # Add to the rejected group
      df_mentee_raw.iloc[e,0] = f'rejected by low availability {availabilityCounter}'
      df_rejected_mentees.loc[len(df_rejected_mentees.index)] = df_mentee_raw.iloc[e]
      continue

    print(f'So far so good\n\tAge: {calculateAge(bday,beginning_date)}\n\tAvailability: {availabilityCounter}')

    # Get the GMT of the preselected mentee
    GMT = df_mentee_raw.iloc[e,df_mentee_raw.columns.get_loc('Time zone')]
    print(GMT)
    try:
      GMT = int(GMT[4:])
    except ValueError:
      if GMT[6] != ":":
        GMT = int(GMT[4:7])
      else:
        GMT = int(GMT[4:6])

      if GMT >= 0:
        GMT += 0.5
      else:
        GMT -= 0.5
    print(GMT)
    
    df_preselected_mentees.loc[len(df_preselected_mentees.index)]=df_mentee_raw.iloc[e]

  for o in range(iMentor, len(df_mentor_raw.index)):
    print(df_mentor_raw.iloc[o,2])
    # 1. Check the minum age 14
    bday = date(int((df_mentor_raw.iloc[o,4])[-4:]), int((df_mentor_raw.iloc[o,4])[3:5]), int((df_mentor_raw.iloc[o,4])[:2]))
    if calculateAge(bday,beginning_date) < 14:
      print(f'rejected by age {calculateAge(bday,beginning_date)}')
      # Add to the rejected group
      df_mentor_raw.iloc[o,0] = f'rejected by age {calculateAge(bday,beginning_date)}'
      df_rejected_mentors.loc[len(df_rejected_mentors.index)] = df_mentor_raw.iloc[o]
      continue
    
    # 2. Check if they have a B2 proficiency level
    if df_mentor_raw.iloc[o,11] != "Yes" :
      print(f'rejected by English level {df_mentor_raw.iloc[o,11]}')
      # Add to the rejected group
      df_mentor_raw.iloc[o,0] = f'rejected by English level {df_mentor_raw.iloc[o,11]}'
      df_rejected_mentors.loc[len(df_rejected_mentors.index)] = df_mentor_raw.iloc[o]
      continue
    
    # 3. Check their minimun availability
    availabilityCounter = 0
    schedule_begin_index = 35
    for i in range(schedule_begin_index, schedule_begin_index + 33):
      if not isinstance(df_mentor_raw.iloc[o,i], float):
        availabilityCounter += len(df_mentor_raw.iloc[o,i].split(', '))
    
    if availabilityCounter < 2 * 3:
      print(f'rejected by low availability {availabilityCounter}')
      # Add to the rejected group
      df_mentor_raw.iloc[o,0] = f'rejected by low availability {availabilityCounter}'
      df_rejected_mentors.loc[len(df_rejected_mentors.index)] = df_mentor_raw.iloc[o]
      continue
    
    print(f'So far so good\n\tAge: {calculateAge(bday,beginning_date)}\n\tAvailability: {availabilityCounter}')

    # Get the GMT of the preselected mentor
    GMT = df_mentor_raw.iloc[o,df_mentor_raw.columns.get_loc('Time zone')]
    print(GMT)
    try:
      GMT = int(GMT[4:])
    except ValueError:
      if GMT[6] != ":":
        GMT = int(GMT[4:7])
      else:
        GMT = int(GMT[4:6])

      if GMT >= 0:
        GMT += 0.5
      else:
        GMT -= 0.5
    print(GMT)

    df_preselected_mentors.loc[len(df_preselected_mentors.index)] = df_mentor_raw.iloc[o]

  upload()

  print("Columnas:")
  print("Mentee raw",len(df_mentee_raw.columns))
  print("Mentor raw:",len(df_mentor_raw.columns))
  print("Mentee pre",len(df_preselected_mentees.columns))
  print("Mentor pre:",len(df_preselected_mentors.columns))
  print("Mentee rej",len(df_rejected_mentees.columns))
  print("Mentor rej:",len(df_rejected_mentors.columns))

  return [len(df_mentee_raw.index), len(df_mentor_raw.index)]