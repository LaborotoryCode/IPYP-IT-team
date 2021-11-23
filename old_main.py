import time
import random
import pandas as pd
import numpy as np
from mentee import mentee
from mentor import mentor
from match import match

def getStats():
  global nMentors, nMentees, nLevels
  nMentors = len(df_list.loc[df_list["role"] == "mentor"].index)
  nMentees = len(df_list.loc[df_list["role"] == "mentee"].index)
  nLevels = df_list.nunique()['level']

def printStats():
  print('\n-----------------------------')
  print('#Mentors: ' + str(nMentors))
  print('#Mentees: ' + str(nMentees))
  print('#Levels: ' + str(nLevels))
  print('-----------------------------\n')

def getParameters():
  global a, b, c
  a = nLevels > nMentors
  b = nMentees > 4 * nMentors
  c = nMentors > nMentees

manuals = 0

# Start timer
start_time = time.time()

# First, we import all the applicants info into
df_list = pd.read_csv("list.csv", sep = ";")
#We filter out all the languages
Language = ["Language1"]

#And itinerate for every language
for k in range(1):

  #Reboot the conditions   
  a = False
  b = False
  c = False
  manualRev = False

  #We extract all the people from a single language
  # Data simulation
  for i  in range(5):
    df_list.loc[df_list.shape[0]] = {}
    
    if random.randint(1,100) > 80:
      #For mentees
      #name
      df_list.iloc[i,0] = "mentee" + str(i)
      #role
      df_list.iloc[i,1] = "mentee"
      #level
      df_list.iloc[i,2] = random.choice(["A1", "A2", "B1","B2"])
      #gender
      df_list.iloc[i,3] = random.choice(['Female','Male','Non-binary','Prefer not to say'])
    else:
      #For mentors
      #name
      df_list.iloc[i,0] = "mentor" + str(i)
      #role
      df_list.iloc[i,1] = "mentor"
      #Prefered gender
      df_list.iloc[i,3] = random.choice(['Female','Male','Non-binary','Prefer not to say'])
      df_list.iloc[i,4] = random.choice(['females/girls','males/boys','No preference'])
      #Prefered level
      df_list.iloc[i,5] = random.choice(['basic','intermediate','any'])
      #If they are native speakers
      df_list.iloc[i,6] = random.choice(['False','True'])

  print(Language[0])
  print(df_list)

  # Object array creation
  mentorList = []
  menteeList = []

  # Object array fill
  for i in range(len(df_list.index)):
    #level;gender;prefGender;prefLevel
    oName = df_list.iloc[i,0]
    oLevel = df_list.iloc[i,2]
    ans = ['Female','Male','Non-binary','Prefer not to say']
    oGender = ans.index(df_list.iloc[i,3])
    oLanguage = Language
    oSchedule = "NaN"
    if df_list.iloc[i,1] == "mentor":
      ans = ['females/girls','males/boys','No preference']
      oprefGender = ans.index(df_list.iloc[i,4])
      ans = ['basic','intermediate','any']
      oprefLevel = ans.index(df_list.iloc[i,5])
      ans = ['False','True']
      onaSpeaker= bool(ans.index(df_list.iloc[i,6]))
      mentorList.append(mentor(oName, oGender, onaSpeaker, oprefGender, oLanguage, oLevel, oSchedule))
    else:
      menteeList.append(mentee(oName, oGender, oLanguage, oLevel, oSchedule))
    
  # Matchinig simulation
  cols = ['level']
  ind = []
  for i in range(len(df_list.index)):
    if df_list.iloc[i, df_list.columns.get_loc('role')] == 'mentor':
      cols.append(df_list.iloc[i, df_list.columns.get_loc('name')])
    else:
      ind.append(df_list.iloc[i, df_list.columns.get_loc('name')])

  df_matches = pd.DataFrame(columns = cols)
  for i in range(len(ind)):
    tempLevel = menteeList[i].level
    temp = [tempLevel]
    for j in range(len(df_matches.columns) - 1):
      ran = random.randint(0,10)
      tempObject = match(ran, ind[i], cols[j+1])
      temp.append(tempObject)
    df_matches.loc[str(ind[i])] = temp

  df_matches = df_matches.sort_values(by=['level'], axis=0)
  print('\nCheckpoint 1\n')
  print(df_matches)

  #Stadistics and Errs
  getStats()
  printStats()

  # General Err List
  getParameters()
  
  if nMentors == 0 or nMentees == 0:
    print('No possible matches')
    continue

  #Too many levels!
  while a:
    print('Too many levels!\n')
    #getting levels, removing np.nan and sorting
    levelList = df_list.level.unique()
    levelList = [x for x in levelList if str(x) != 'nan']
    levelList.sort()
    levelList = levelList[::-1]
    levelDf = pd.DataFrame(columns = ['amount'])
    
    for level in levelList:
      temp = []
      temp.append(len(df_list.loc[df_list['level'] == str(level)].index))
      levelDf.loc[str(level)] = temp
    
    print(levelDf)
    #Pick the levels with the fewewst amount of mentees
    min = levelDf.iloc[0,0]
    delLevel = []
    for level in levelList:
      if min > int(levelDf.iloc[levelList.index(level),0]):
        min = int(levelDf.iloc[levelList.index(level),0])
    for level in levelList:
      if int(levelDf.iloc[levelList.index(level),0]) == min:
        delLevel.append(level)

    #If there's more than one level, choose the one with the least total matches
    delLevelDf = pd.DataFrame(columns = ['matches'])
    if len(delLevel) > 1:
      delLevelMatches = []
      for level in delLevel:
        tempSum = 0
        for i in range(len(df_matches.index)):
          for j in range(1,len(df_matches.columns)):
            if df_matches.iloc[i,0] == level:
              tempSum += (df_matches.iloc[i,j]).value
        delLevelMatches.append(tempSum)
        delLevelDf.loc[level] = tempSum
      print(delLevelMatches)
      min = delLevelMatches[0]
      delLevelValue = delLevel[0]
      for i in range(1,len(delLevelMatches)):
        if min > delLevelMatches[i]:
          min = delLevelMatches[i]
          delLevelValue = delLevel[i]
      delLevel[0] = delLevelValue

    #Removing the mentees from the levels in both dfs
    i = len(df_matches.index) - 1
    while i >= 0:
      if df_matches.iloc[i,0] == delLevel[0]:
        df_matches  = df_matches.drop([df_matches.index[i]])
      i -= 1
    i = len(df_list.index) - 1
    while i >= 0:
      if df_list.iloc[i,2] == delLevel[0]:
        df_list  = df_list.drop([df_list.index[i]])
      i -= 1
    
    getStats()
    getParameters()
    printStats()
  
  print(df_matches.dtypes)

  #Too many mentors!
  while c:
    print('Too many mentors!')

    #calculate the total matches for mentor
    torTotalMatches = [10000]
    for j in range(1, len(df_matches.columns)):
      tempSum = 0
      for i in range(len(df_matches.index)):
        print(type(df_matches.iloc[i,j]), df_matches.iloc[i,j].value)
        temp = (df_matches.iloc[i,j]).value
        print(temp)
        tempSum += temp
        print(temp, tempSum)
      torTotalMatches.append(tempSum)
    df_matches.loc['Total'] = torTotalMatches
    df_matches = df_matches.sort_values(by = ['Total'], axis = 1, ascending = False)

    lastIndex = len(df_matches.columns) - 1
    cont = 0
    tors = nMentors - nMentees

    #Compare if the mentors who are in the border between the ones who are going to be deleted and the ones who are not don't have the same availability
    print(type((df_matches.iloc[(len(df_matches.index) - 1), (lastIndex - tors)])),df_matches.iloc[(len(df_matches.index) - 1), (lastIndex - tors)].__class__)
    midDel = (df_matches.iloc[(len(df_matches.index) - 1), (lastIndex - tors)])
    midNoDel = (df_matches.iloc[(len(df_matches.index) - 1), (lastIndex - tors + 1)])

    print('We got', midDel, midNoDel)

    if midNoDel == midDel:
      print('and',(mentorList[mentorList.index(midDel.mentor)]).naSpeaker, [mentorList.index(midNoDel.mentor)].naSpeaker)
      if mentorList[mentorList.index(midDel.mentor)].naSpeaker == mentorList[mentorList.index(midNoDel.mentor)].naSpeaker:
        df_matches = df_matches.drop(columns = 'Total')
        manualRev = True
        manuals += 1
        break
      elif mentorList[mentorList.index(midDel.mentor)].naSpeaker:
        print("Natives changed")
        b, c = df_matches.iloc[:,(lastIndex - tors)].copy(), df_matches.iloc[:,(lastIndex - tors+1)].copy()
        df_matches.iloc[:,(lastIndex - tors)],a.iloc[:,(lastIndex - tors+1)] = c,b
        
    while cont < tors:
      df_matches = df_matches.drop(df_matches.columns[[lastIndex - cont]], axis = 1)
      cont += 1
    
    df_matches = df_matches.drop(index = 'Total')
    #print(df_matches)
    getStats()
    getParameters()
    printStats()  
  
  # Assigning levels
  # First get the best mentor for every person
  mentorList = list(df_matches.columns)
  for i in range(len(df_matches.index)):
    tempArr = df_matches.iloc[i].to_numpy()
    tempLevel = tempArr[0]
    tempArr = np.delete(tempArr, 0)
    print(tempArr)

  print(df_matches)
  print()

  #Making the groups

  #Asign mentors to the levels
  levelList = df_list.level.unique()
  levelList = [x for x in levelList if str(x) != 'nan']
  levelList.sort()
  print(levelList)

  indexList = list(df_matches.columns)

  df_temp = pd.DataFrame(columns = list(df_list.columns))
  for i in range(len(df_list.index)):
    if (df_list.iloc[i,0] in indexList) or (df_list.iloc[i,1] == 'mentee'):
      df_temp.loc[str(df_list.iloc[i,0])] = df_list.iloc[i]
  df_list = df_temp

  #Too many mentees!
  while b:
    print('Too many mentees!')
    
    teeTotalMatches = []
    for i in range(len(df_matches.index)):
      tempSum = 0
      for j in range(1, len(df_matches.columns)):
        tempSum += df_matches.iloc[i,j].value
      teeTotalMatches.append(tempSum)
    df_matches['Total'] = teeTotalMatches
    df_matches = df_matches.sort_values(by = ['Total'], ascending = False)
    print(df_matches)
    
    lastIndex = len(df_matches.index) - 1
    cont = 0
    tees = nMentees - 4 * nMentors

    #Compare if the mentees who are in the border between the ones who are going to be deleted and the ones who are not don't have the same availability
    midDel = df_matches.iloc[(lastIndex - tees), (len(df_matches.columns) - 1)]
    midNoDel = df_matches.iloc[(lastIndex - tees + 1), (len(df_matches.columns) - 1)]

    if midNoDel == midDel:
      df_matches = df_matches.drop(columns = 'Total')
      manualRev = True
      manuals += 1
      break

    while cont < tees:
      df_matches = df_matches.drop([df_matches.index[lastIndex - cont]])
      cont += 1

    indexList = list(df_matches.index)

    df_temp = pd.DataFrame(columns = list(df_list.columns))
    for i in range(len(df_list.index)):
      if (df_list.iloc[i,0] in indexList) or (df_list.iloc[i,1] == 'mentor'):
        df_temp.loc[str(df_list.iloc[i,0])] = df_list.iloc[i]
    df_list = df_temp

    df_matches = df_matches.drop(columns = 'Total')

    #print(df_matches)
    getStats()
    getParameters()
  
  if manualRev:
    print('\n\nManual revision requiered!')
#print('Out of 500 simulations, ' + str(manuals) + ' requiered manual revision')

  


df_list.to_csv("list2.csv", index = False , sep = ";")
df_matches.to_csv("matches.csv", index = False , sep = ";")

print("--- %s seconds ---" % (time.time() - start_time))
