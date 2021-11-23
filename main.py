import time
from datetime import date

from createData import createData
from selective_process import evaluate
from clearData import clearData
#from keep_alive import keep_alive

#Keep the program running
#keep_alive()

#Simulation of the answers
#createData()

# Start timer
start_time = time.time()

# Dealine for the Applicantions
deadline = date(2022, 1, 26)
today = date.today()

last_mentee_index = 0
last_mentor_index = 0

# SELECTIVE PROCESS SECTION
# while (today != deadline):

clearData()
for i in range(1):
  createData()

  temp = evaluate(last_mentee_index, last_mentor_index)
  last_mentee_index = temp[0]
  last_mentor_index = temp[1]
  print(f'Mentees: {last_mentee_index}\tMentors: {last_mentor_index}')
  time.sleep(40)


print("--- %s seconds ---" % (time.time() - start_time))