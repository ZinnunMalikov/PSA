#Upload Data File
from google.colab import files
uploaded = files.upload()
#Select 2015data.csv

import copy
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

#Math Function Definitions - - - - - - - - - - - - - - - - - - -
#Create Standard Dev
def stan_dev(inp):
  mean = sum(inp)/len(inp)
  vari = 0
  for a in range(len(inp)):
    vari = vari + (1/(len(inp)-1))*(inp[a]-mean)*(inp[a]-mean)
  return(vari**0.5)

#Five Number Summary
def five_sum(inp_li1):
  inp_li = copy.deepcopy(inp_li1)
  inp_li.sort()
  dnum = len(inp_li)

  if len(inp_li) % 2 == 1:
      median = inp_li[int((dnum + 1)/2 - 1)]
      lh = inp_li[0:int((dnum + 1)/2 - 1)]
      uh = inp_li[int((dnum+1)/2):]
  else:
      median = (inp_li[int(dnum/2) - 1] + inp_li[int(dnum/2)])/2
      lh = inp_li[0: int(dnum/2)]
      uh = inp_li[int(dnum/2):]


  if len(lh) % 2 == 1:
      q1 = lh[int((len(lh) + 1)/2 - 1)]
  else:
      q1 = (lh[int(len(lh)/2 - 1)] + lh[int(len(lh)/2)])/2

  if len(uh) % 2 == 1:
      q3 = uh[int((len(uh) + 1)/2 - 1)]
  else:
      q3 = (uh[int(len(uh)/2 - 1)] + uh[int(len(uh)/2)])/2

  iqr = q3 - q1
  return([min(inp_li), q1, median, q3, max(inp_li)])

#Percentile
def percentile(value_list, value):
  accumulation = 0
  for k in range(len(value_list)):
    if value_list[k] <= value:
      accumulation += 1
  return(accumulation/len(value_list))

#data fixing
def isNaN(ni):
  return ni != ni

#Datafram - - - - - - - - - - - - - - -

#Convert raw data to a usable dataframe array
df_sleep = pd.read_csv(io.BytesIO(uploaded['2015data.csv']))
array_sleep = df_sleep.to_numpy()

#Create a list of average sleep
avg_weekdays = array_sleep[:, 39]
avg_weekends = array_sleep[:, 40]

for a in range(len(avg_weekdays)):
  if isNaN(avg_weekdays[a]) == True:
    avg_weekdays[a] = 411.45
  if isNaN(avg_weekends[a]) == True:
    avg_weekends[a] = 449.9
    
avg_total = list(np.add(avg_weekdays*5/(60*7), avg_weekends*2/(60*7)))
#print(avg_total)

#PSA Intro - - - - - - - - - - - - - - - - - - - - - - - - -

print('Sleep deprivation is a prevalent issue in the United States. With data showing that lower sleep \nquality scores are associated with shorter sleep times, action must be taken to combat this issue. \n')
choice = input('Select from the choices below to learn more! \n 1- Average Sleep Times in the US \n 2- Pie Chart of Sleep Times in the US \n 3- Effects of Light Exposure on Sleep Quality \n')

if choice == '1':
  sleep_amount_inp = float(input('\nHow many hours do you sleep each night?'))
  print("You are in the " + str(round(100*percentile(avg_total, sleep_amount_inp), 2)) + "th percentile!")

  #Make data
  x = avg_total

  #Limits
  xlow = min(avg_total)
  xhigh = max(avg_total)

  #Plot:
  fig, ax = plt.subplots()

  ax.hist(x, bins=32, linewidth=0.5, edgecolor="white")

  ax.set(xlim=(0, xhigh))

  plt.title("Distrbution of the Average Sleep Times of 1029 Individuals (2015)")
  plt.xlabel("Hours")
  plt.ylabel("Frequency")
  print('\n[Minimum, Q1, Median, Q3, Maximum]:' + str(five_sum(avg_total)))
  print("Standard Deviation: " + str(stan_dev(avg_total)))
  plt.show()
  
if choice == '2':
  sleep_amount_inp = float(input('\nHow many hours do you sleep each night?'))
  if sleep_amount_inp < 7:
    print('You are among the 40% of Americans that do not get enough sleep. Try to sleep more!')
  else:
    print('Great! Continue getting enough sleep!')
  #Proportion of those who slept: (<6), (6-7), (7, 8), (8+) hours
  p1 = 0
  p2 = 0
  p3 = 0
  p4 = 0
  for num in avg_total:
    if num < 6:
      p1 += 1
    elif num < 7:
      p2 += 1
    elif num < 8:
      p3 += 1
    else:
      p4 += 1
  #Broad Pie Chart
  labels = ["<7 hours", "7+ hours"]
  sizes = [p1+p2, p3+p4]
  explode=[0,0]

  plt.pie(sizes, autopct='%1.0f%%', explode=explode,labels=labels,shadow=True,startangle=90, )
  plt.axis("equal")
  plt.legend(title="Categorical Distribution of Sleep Times from 2015 Survey", loc = 'best')
  plt.subplots_adjust(left=0.2, bottom=0.1, right=2.5)
  plt.show()
  
if choice == '3':
  light_input_qa = input('\nOn a scale of 1-5, how often are you exposed to artificial light while trying to sleep?')
  if light_input_qa == '1' or light_input_qa == '2':
    print('Exposure to artificial light is not likely to affect your quality of sleep!')
  elif light_input_qa == '3' or light_input_qa == '4' or light_input_qa == '5':
    print('Exposure to artificial light is likely to negatively affect your quality of sleep!')

  #Relationship Between Light Exposure and Sleep Quality
  sleep_quality = array_sleep[:, 61]
  sleep_quality = list(sleep_quality)
  light_exp = array_sleep[:, 98]
  light_exp = list(light_exp)

  mlig1 = []
  mlig2 = []
  mlig3 = []
  mlig4 = []
  mlig5 = []

  for a in range(len(light_exp)):
    if light_exp[a] == 1:
      mlig1.append(sleep_quality[a])
    if light_exp[a] == 2:
      mlig2.append(sleep_quality[a])
    if light_exp[a] == 3:
      mlig3.append(sleep_quality[a])
    if light_exp[a] == 4:
      mlig4.append(sleep_quality[a])
    if light_exp[a] == 5:
      mlig5.append(sleep_quality[a])

  mlig1_summary = []
  mlig2_summary = []
  mlig3_summary = []
  mlig4_summary = []
  mlig5_summary = []

  ml1s1, ml2s1, ml3s1, ml4s1, ml5s1 = 0, 0, 0, 0, 0
  ml1s2, ml2s2, ml3s2, ml4s2, ml5s2 = 0, 0, 0, 0, 0
  ml1s3, ml2s3, ml3s3, ml4s3, ml5s3 = 0, 0, 0, 0, 0
  ml1s4, ml2s4, ml3s4, ml4s4, ml5s4 = 0, 0, 0, 0, 0
  ml1s5, ml2s5, ml3s5, ml4s5, ml5s5 = 0, 0, 0, 0, 0

  for a in range(len(mlig1)):
    if mlig1[a] == 1:
      ml1s1 += 1/len(mlig1)
    elif mlig1[a] == 2:
      ml2s1 += 1/len(mlig1)
    elif mlig1[a] == 3:
      ml3s1 += 1/len(mlig1)
    elif mlig1[a] == 4:
      ml4s1 += 1/len(mlig1)
    elif mlig1[a] == 5:
      ml5s1 += 1/len(mlig1)

  for a in range(len(mlig2)):
    if mlig2[a] == 1:
      ml1s2 += 1/len(mlig2)
    elif mlig2[a] == 2:
      ml2s2 += 1/len(mlig2)
    elif mlig2[a] == 3:
      ml3s2 += 1/len(mlig2)
    elif mlig2[a] == 4:
      ml4s2 += 1/len(mlig2)
    elif mlig2[a] == 5:
      ml5s2 += 1/len(mlig2)

  for a in range(len(mlig3)):
    if mlig3[a] == 1:
      ml1s3 += 1/len(mlig3)
    elif mlig3[a] == 2:
      ml2s3 += 1/len(mlig3)
    elif mlig3[a] == 3:
      ml3s3 += 1/len(mlig3)
    elif mlig3[a] == 4:
      ml4s3 += 1/len(mlig3)
    elif mlig3[a] == 5:
      ml5s3 += 1/len(mlig3)

  for a in range(len(mlig4)):
    if mlig4[a] == 1:
      ml1s4 += 1/len(mlig4)
    elif mlig4[a] == 2:
      ml2s4 += 1/len(mlig4)
    elif mlig4[a] == 3:
      ml3s4 += 1/len(mlig4)
    elif mlig4[a] == 4:
      ml4s4 += 1/len(mlig4)
    elif mlig4[a] == 5:
      ml5s4 += 1/len(mlig4)

  for a in range(len(mlig5)):
    if mlig5[a] == 1:
      ml1s5 += 1/len(mlig5)
    elif mlig5[a] == 2:
      ml2s5 += 1/len(mlig5)
    elif mlig5[a] == 3:
      ml3s5 += 1/len(mlig5)
    elif mlig5[a] == 4:
      ml4s5 += 1/len(mlig5)
    elif mlig5[a] == 5:
      ml5s5 += 1/len(mlig5)

  #Categorical v. Categorical
  labels = ['1', '2', '3', '4', '5']

  g1 = [ml1s1, ml1s2, ml1s3, ml1s4, ml1s5]
  g2 = [ml2s1, ml2s2, ml2s3, ml2s4, ml2s5]
  g3 = [ml3s1, ml3s2, ml3s3, ml3s4, ml3s5]
  g4 = [ml4s1, ml4s2, ml4s3, ml4s4, ml4s5]
  g5 = [ml5s1, ml5s2, ml5s3, ml5s4, ml5s5]

  width = 0.35       # the width of the bars: can also be len(x) sequence

  fig, ax = plt.subplots()

  ax.bar(labels, g1, width)
  ax.bar(labels, g2, width, bottom = g1)
  ax.bar(labels, g3, width, bottom = list(np.array(g1)+np.array(g2)))
  ax.bar(labels, g4, width, bottom = list(np.array(g1)+np.array(g2)+np.array(g3)))
  ax.bar(labels, g5, width, bottom = list(np.array(g1)+np.array(g2)+np.array(g3)+np.array(g4)))

  ax.set_ylabel('Distribution of Sleep Quality Responses (1-5)')
  ax.set_xlabel('External Light Exposure (1-5)')
  ax.set_title('Distributions of Sleep Quality Responses (1-5) for Varying Levels of External Light Exposure (1-5)')

  print("\nBlue: Frequency of '1' responses") 
  print("Orange: Frequency of '2' responses")
  print("Green: Frequency of '3' responses") 
  print("Red: Frequency of '4' responses")
  print("Purple: Frequency of '5' responses") 
  print('')
  plt.show()




