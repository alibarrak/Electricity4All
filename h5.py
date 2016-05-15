'''*********************************************************************
This code is written for #Electricity4All Python Challenge
https://unite.un.org/ideas/content/electricity4all-python-challenge
on May 13 2016 By Ali Aldowais (last edited May 15 2016)
licensed under a GNU General Public License Version 3

The code is based on VBA code
Created by Manuel Welsch based on 140704_TestElectrification.xlsm
Last Modified by Oliver Broad - 14 07 16
**********************************************************************'''
import csv

data_file = '40k_in.csv'                      # input data file name (assuming first row is header)
scenario_file = 'scenario1.csv'               # scenario file name (assuming first row is distance as INT and second row as #of people INT)
result_file = scenario_file+'_result.csv'     # result file name

debug = 0   # debug: to break on read data line number provided. 0 to ignore

# read scenario file (csv file contains row of distance and row of number of prople)
with open(scenario_file, 'rt') as file:
  reader = csv.reader(file, delimiter=',')
  Limits = []
  for row in reader:
    Limits.append(row)  # store scenario (distance & number of people)
  
# read data file
with open(data_file, 'rt') as file:
  reader = csv.reader(file, delimiter=',')
  
  header = []                  # used for output file
  header.append(['','','',''])
  header[0].extend(Limits[0])
  header.append(next(reader))  # Read first line and count columns (could use constant 4 as input columns are: X, Y, POP, ele)
  header[1].extend(Limits[1])
  
  InputW = len(header[0])  # store input file total column (should be constant of 4 ?)
  
  GISdata = []
  result = [] # store resulted output on each scenario loop then use to write result file
  ElecStatus = []
  CellPath = []
  CellPath.append([])  # init 2d array
  CellPath.append([])  #
  
  
  for line,row in enumerate(reader):
    if debug > 0 and line==debug:  # if debug is set, break reading on provided line number
      break
      
    GISdata.append(row)         # store input data as multipdimension array
    ElecStatus.append(row[3])   # store column 4 from input data (electrification status)
    CellPath[0].append(0)       # initilise array with 0 (store the km of line built prior to electrifying this cell)
    CellPath[1].append(0)       # initilise array with 0 (stores the added km of line built specifically on the iteration that electrified the cell)
  
  InputL = len(GISdata)         # input data length
      
  ''' Iterate on each set of constraints formed by a given distance and a given number of people '''
  for l in range(0, len(Limits[0])):
    cntIteration = 0

    # initilise arrays
    Unelectrified = []
    ElecInput = []
    ElecChanges = []
    
    for i in range(1, InputL):
      if int(ElecStatus[i-1]) == 0:
        Unelectrified.append(i) # store index of ele=0
      else:
        ElecInput.append(i) # store index of ele=1
    
    cnt2 = True
    while cnt2:
      cntIteration += 1
      print("While Loop Start - Column: ",l,", Iteration: ",cntIteration)
      cnt2 = False
      
      for i in range(0, len(ElecInput)): # number of electrified fields
        print("itteration of electrified cell no ",i,", Elec line ",ElecInput[i])
        
        for j in range(0, len(Unelectrified)): # number of Unelectrified fields
          ExistingGrid = int(CellPath[0][ElecInput[i]]) + int(CellPath[1][ElecInput[i]])

          OkToExtend = ExistingGrid < 50000
          if OkToExtend != True: # next iteration if false
            continue

          el = int(ElecStatus[Unelectrified[j]]) == 0
          if el != True: # next iteration if false
            continue
          
          dx = abs(float(GISdata[ElecInput[i]][0]) - float(GISdata[Unelectrified[j]][0])) < int(Limits[0][l])
          if dx != True: # next iteration if false
            continue
          
          dy = abs(float(GISdata[ElecInput[i]][1]) - float(GISdata[Unelectrified[j]][1])) < int(Limits[0][l])
          if dy != True: # next iteration if false
            continue
          
          NotTheSame = (abs(float(GISdata[ElecInput[i]][0]) - float(GISdata[Unelectrified[j]][0])) > 0) or (abs(float(GISdata[ElecInput[i]][1]) - float(GISdata[Unelectrified[j]][1])) > 0)
          if NotTheSame != True: # next iteration if false
            continue

          pop = float(GISdata[Unelectrified[j]][2]) > int(Limits[1][l]) + int(Limits[0][l]) * (15.702 * (ExistingGrid + 7006) / 1000 - 110) / 4400 # note that the "+7006" ensures that we are not removing people on iteration 1
          if pop != True:
            continue
        
          ''' Electrification decision: if the cell is not already changed and the conditions apply, then electrify '''
          if el and dx and dy and pop and NotTheSame and OkToExtend == True:
            FindValue = False
            for k in range(0, len(ElecChanges)):  # Checks if this change has already been registered, if so, leaves if
              if ElecChanges[k] == Unelectrified[j]:
                FindValue = True

            if FindValue == False:
              print("Row added to ElecStatus: ",Unelectrified[j]," Based on ref cell line ",ElecInput[i])
              # Collects rows j for which electricity status changes and writes it into ElecChanges plus changes value in Electrified
              cnt2 = True
              ElecChanges.append(Unelectrified[j])
              ElecStatus[Unelectrified[j]] = 1
              
              CellPath[0][Unelectrified[j]] = ExistingGrid
              CellPath[1][Unelectrified[j]] = int(Limits[0][l])
        #end Unelectrified loop
      #end ElecInput loop
      
      # new electrified cell as a potential starting point for new iteration
      if cnt2:
        ElecInput = []
        ElecInput = ElecChanges
        ElecChanges = []
 
    #end while
    result.append(ElecStatus) # store current loop ElecStatus
  #end for
  
# write result
#with open(result_file, 'w', newline='') as out_file: #newline fix for
with open(result_file, 'w') as out_file:
  out = csv.writer(out_file, delimiter=',')
  for i in range(0, len(GISdata)):
    for l in range(0, len(Limits[1])):
      GISdata[i].append(result[l][i])

  out.writerows(header+GISdata)
