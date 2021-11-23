import time
import random
import pandas as pd
import gspread
import readData as rD
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

# Read Google Spreadsheets
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(credentials)

'''
mentee_spreadsheet_id='1shFQ5KtOxGZ9IJdCcFVo9FtAGtpnoJ7GYYfc7x8SaVs'
mentor_spreadsheet_id='1PGNGMNS5vg3Lt4xGIuSmHBXgKgTQQlIPF8rJXUbBnuQ'

df_mentee_origin = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{mentee_spreadsheet_id}/export?format=csv")
df_mentor_origin = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{mentor_spreadsheet_id}/export?format=csv")
'''
df_mentee_origin = pd.DataFrame()
df_mentor_origin = pd.DataFrame()

def read():
  global df_mentee_origin
  global df_mentor_origin

  df_mentee_origin = rD.read_rawMentees()
  df_mentor_origin = rD.read_rawMentors()

def pickDays():
  dayTemp = []
  days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
  minIndex = 0
  for i in range(9):
    minIndex = random.randint(minIndex,50)
    try:
      tempDay = days[minIndex]
    except IndexError:
      continue
    else:
      if not (tempDay in dayTemp):
        dayTemp.append(days[minIndex])
  
  return ', '.join(dayTemp)

def createDataMentees():
  # Mentee creation
  for i in range(20):
    temp = []
    # Chronological information
    temp.append('01/01/2022')
    # email
    temp.append(f'mentee{len(df_mentee_origin.index)}@mail.com')
    # name
    temp.append(f'mentee{len(df_mentee_origin.index)}')
    # social name
    temp.append('tee')
    # Birthday
    month = random.randint(1,12)
    if month in [1,3,5,7,8,10,12]:
      day = random.randint(1,31)
    elif month in [4,6,9,11]:
      day = random.randint(1,30)
    else:
      day = random.randint(1,28)
    if month < 10:
      month = f'0{month}'
    if day < 10:
      day = f'0{day}'
    temp.append(f'{day}/{month}/{random.randint(1995,2011)}')

    # Time Zone
    temp.append(f'{random.choice(["GMT +14","GMT +13:45","GMT +13","GMT +12","GMT +11","GMT +10:30","GMT +10","GMT +9:30","GMT +9","GMT +8:45","GMT +8","GMT +7","GMT +6:30","GMT +6","GMT +5:45","GMT +5:30","GMT +5","GMT +4:30","GMT +4","GMT +3:30","GMT +3","GMT +2","GMT +1","GMT +0","GMT -1","GMT -2","GMT -2:30","GMT -3","GMT -4","GMT -5","GMT -6","GMT -7","GMT -8","GMT -9","GMT -9:30","GMT -10","GMT -11","GMT -12"])}')

    # Link for social network
    temp.append('https://www.instagram.com/andreparedes06/')
    # WhatsApp Number
    temp.append(f'{random.randint(1111111111,9999999999)}')
    # Gender
    temp.append(f'{random.choice(["Female","Male","Female","Male","Female","Male","Female","Male","Female","Male","Female","Male","Female","Male","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Non-binary","Non-binary","Prefer not to say","[Other]"])}')
    # Birth Location
    temp.append('Somewhere, Else')
    # Current Location
    temp.append('Not, Important')
    # English proficiency == B2
    temp.append(f'{random.choice(["Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","No"])}')
    # Race - color
    temp.append('bot')
    # Religion
    temp.append('ohn McCarthy')
    # How did you find the IPYP?
    temp.append('Instagram')
    # Plans with the learning you'll recieve
    temp.append('[Some text]')
    # Commitment and expectatives
    temp.append('[Some text]')

    ###LANGAUGE###
    # There are 10 languages
    for repeter in range(10):
      temp.append(f'{random.choice(["","A1","A2","B1","B2"])}')

    # Future language plans
    temp.append('[Some text]')
    
    ###AVAILABILITY###
    # [06:00] - [22:00], 33 half hours
    for repeter in range(33):
      temp.append(pickDays())
    
    # Internet access?
    temp.append('Yes, I do')
    # Anything more?
    temp.append('[Some text]')
    # Terms?
    temp.append('Yes')

    df_mentee_origin.loc[len(df_mentee_origin.index)] = temp
    #df_mentee_origin.loc[len(i+1)] = temp

def createDataMentors():
  # Mentor creation
  for i in range(10):
    temp = []
    # Chronological information
    temp.append('01/01/2022')
    # email
    temp.append(f'mentee{len(df_mentor_origin.index)}@mail.com')
    # name
    temp.append(f'mentor{len(df_mentor_origin.index)}')
    # social name
    temp.append('tor')
    # Birthday
    month = random.randint(1,12)
    if month in [1,3,5,7,8,10,12]:
      day = random.randint(1,31)
    elif month in [4,6,9,11]:
      day = random.randint(1,30)
    else:
      day = random.randint(1,28)
    if month < 10:
      month = f'0{month}'
    if day < 10:
      day = f'0{day}'
    temp.append(f'{day}/{month}/{random.randint(1995,2011)}')

    # Time Zone
    temp.append(f'{random.choice(["GMT +14","GMT +13:45","GMT +13","GMT +12","GMT +11","GMT +10:30","GMT +10","GMT +9:30","GMT +9","GMT +8:45","GMT +8","GMT +7","GMT +6:30","GMT +6","GMT +5:45","GMT +5:30","GMT +5","GMT +4:30","GMT +4","GMT +3:30","GMT +3","GMT +2","GMT +1","GMT +0","GMT -1","GMT -2","GMT -2:30","GMT -3","GMT -4","GMT -5","GMT -6","GMT -7","GMT -8","GMT -9","GMT -9:30","GMT -10","GMT -11","GMT -12"])}')

    # Link for social network
    temp.append('https://www.instagram.com/andreparedes06/')
    # WhatsApp Number
    temp.append(f'{random.randint(1111111111,9999999999)}')
    # Gender
    temp.append(f'{random.choice(["Female","Male","Female","Male","Female","Male","Female","Male","Female","Male","Female","Male","Female","Male","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Female","Non-binary","Non-binary","Prefer not to say","[Other]"])}')
    # Birth Location
    temp.append('Somewhere, Else')
    # Current Location
    temp.append('Not, Important')
    # English proficiency == B2
    temp.append(f'{random.choice(["Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","No"])}')
    # Race - color
    temp.append('bot')
    # Religion
    temp.append('ohn McCarthy')
    # How did you find the IPYP?
    temp.append('Instagram')
    # Importtance of languages
    temp.append('[Some text]')
    # Did not lead well
    temp.append('[Some text]')
    # Commitment and expectatives
    temp.append('[Some text]')

    ###LANGAUGE###
    # There are 11 languages
    for repeter in range(11):
      temp.append(f'{random.choice(["","","","Native Speaker","Language certificate","Language certificate","Language certificate","Self learning"])}')

    # Extra laguages
    temp.append('[Some text]')
    # Experience teaching?
    temp.append(f'{random.choice(["Yes","No"])}')
    # Experience teaching
    temp.append('[Some text]')
    # How did you learn?
    temp.append('[Some text]')
    # Certificade
    temp.append('[Some link]')

    ###AVAILABILITY###
    # [06:00] - [22:00], 33 half hours
    for repeter in range(33):
      temp.append(pickDays())
    
    # Internet access?
    temp.append('Yes, I do')
    # Anything more?
    temp.append('[Some text]')
    # Terms?
    temp.append('Yes')
    
    df_mentor_origin.loc[len(df_mentor_origin.index)] = temp
    #df_mentor_origin.loc[(i+1)] = temp

def createData():
  read()
  createDataMentees()
  createDataMentors()

  test_spreadsheet_id = '14m89nbA7ST_fLA5S20piFXRUwvSO-YJqbBcViLzt8E4'

  d2g.upload(df_mentee_origin, test_spreadsheet_id, 'Test_mentee', credentials=credentials, row_names = False)
  d2g.upload(df_mentor_origin, test_spreadsheet_id, 'Test_mentor', credentials=credentials, row_names = False)

  print('20 sec cooldown')
  time.sleep(20)