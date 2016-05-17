'''*********************************************************************
This code is written for #Electricity4All Python Challenge
https://unite.un.org/ideas/content/electricity4all-python-challenge
on May 13 2016 By Ali Aldowais (last edited May 17 2016)
licensed under a GNU General Public License Version 3

The code is based on VBA code
Created by Manuel Welsch based on 140704_TestElectrification.xlsm
Last Modified by Oliver Broad - 14 07 16
**********************************************************************'''
import csv

data_file = '40k_in.csv'                      # input data file name (assuming first row is header)
scenario_file = 'scenario1.csv'               # scenario file name (assuming first row is distance as INT and second row as #of people INT)
result_file = scenario_file+'_result.csv'     # result file name

debug = 0                                     # debug: to break on read data line number provided. 0 to ignore

# read scenario file (csv file contains row of distance and row of number of prople)
with open(scenario_file, 'rt') as file:
  reader = csv.reader(file, delimiter=',')
  Limits = []
  for row in reader:
    Limits.append(row)  # store scenario (distance & number of people)

for i in range(0, len(Limits)):  # convert to int (faster calculation)
  for j in range(0, len(Limits[0])):  
    Limits[i][j] = int(Limits[i][j])
    
# read data file
with open(data_file, 'rt') as file:
  reader = csv.reader(file, delimiter=',')
  
  header = []                  # used for output file
  header.append(['','','',''])
  header[0].extend(Limits[0])
  header.append(next(reader))  # Read first line and count columns (could use constant 4 as input columns are: X, Y, POP, ele)
  header[1].extend(Limits[1])
  
  GISdata = []         # store inputs as float
  GISdataStr = []      # store inputs as string
  result = []          # store resulted output on each scenario loop then use to write result file
  ElecStatus = []
  CellPath = []
  CellPath.append([])  # init 2d array
  CellPath.append([])  #
  
  
  for line,row in enumerate(reader):
    if debug > 0 and line==debug:    # if debug is set, break reading on provided line number
      break
    GISdata.append([float(row[0]), float(row[1]), float(row[2]), int(row[3])])         # store input data as multipdimension array (converting to float and int here makes calculation faster)
    GISdataStr.append(row)           # store input data as string (to avoid extra .0 floating point in output if GISdata[] used)
  
  InputL = len(GISdata)              # input data length
    
  for i in range(1, InputL):         # index starts here from 1 not 0
    ElecStatus.append(GISdata[i][3]) # store column 4 from input data (electrification status)
    CellPath[0].append(0)            # initilise array with 0 (store the km of line built prior to electrifying this cell)
    CellPath[1].append(0)            # initilise array with 0 (stores the added km of line built specifically on the iteration that electrified the cell)

  ''' Iterate on each set of constraints formed by a given distance and a given number of people '''
  for l in range(0, len(Limits[0])):
    cntIteration = 0

    lim0 = Limits[0][l]  # short name for variable that's used multiple times
    lim1 = Limits[1][l]  # short name
    
    result.append([])    # empty array, to store each limit result in
    
    # initilise arrays
    Unelectrified = []
    ElecInput = []
    ElecChanges = []
    
    for i in range(1, InputL):  # index sstarts at 1
      if ElecStatus[i-1] == 0:
        Unelectrified.append(i) # store index of ele=0
      else:
        ElecInput.append(i)     # store index of ele=1
    
    cnt2 = True
    while cnt2:
      cntIteration += 1
      print("While Loop Start - Column: ",l,", Iteration: ",cntIteration)
      cnt2 = False
      
      for i in range(0, len(ElecInput)): # number of electrified fields
        #print("itteration of electrified cell no ",i,", Elec line ",ElecInput[i])
        
        ''' optomization: to exit the loop early '''
        ei = ElecInput[i]
        ExistingGrid = (CellPath[0][ei - 1]) + (CellPath[1][ei - 1])
        OkToExtend = ExistingGrid < 50000
        if OkToExtend != True: # next iteration
          continue
          
        for j in range(0, len(Unelectrified)): # number of Unelectrified fields
          
          uj = Unelectrified[j]
          el = ElecStatus[uj - 1] < 1
          if el != True: # next iteration
            continue
          
          gE0 = GISdata[ei][0]
          gU0 = GISdata[uj][0]
          dx = abs(gE0 - gU0) < lim0
          if dx != True: # next iteration
            continue
            
          gE1 = GISdata[ei][1]
          gU1 = GISdata[uj][1]
          dy = abs(gE1 - gU1) < lim0
          if dy != True: # next iteration
            continue
            
          NotTheSame = (abs(gE0 - gU0) > 0) or (abs(gE1 - gU1) > 0)
          if NotTheSame != True:
            continue
            
          pop = GISdata[uj][2] > lim1 + lim0 * (15.702 * (ExistingGrid + 7006) / 1000 - 110) / 4400 # note that the "+7006" ensures that we are not removing people on iteration 1
          if pop != True: # next iteration
            continue
        
          #''' Electrification decision: if the cell is not already changed and the conditions apply, then electrify '''
          #if el and dx and dy and pop and NotTheSame and OkToExtend == True:
          # no need for previous line as loop will exit on previous conditions mismatch
          
          FindValue = False
          for k in range(0, len(ElecChanges)):  # Checks if this change has already been registered, if so, leaves if
            if ElecChanges[k] == uj:
              FindValue = True
              break

          if FindValue == False:
            print("Row added to ElecStatus: ",uj," Based on ref cell line ",ei)
            cnt2 = True
            # Collects rows j for which electricity status changes and writes it into ElecChanges plus changes value in Electrified
            ElecChanges.append(uj)
            ElecStatus[uj - 1] = 1
            CellPath[0][uj - 1] = ExistingGrid
            CellPath[1][uj - 1] = lim0
        #end Unelectrified loop
      #end ElecInput loop
      
      # new electrified cell as a potential starting point for new iteration
      if cnt2:
        ElecInput = []  # clear
        ElecInput.extend(ElecChanges)  # append
        ElecChanges = []  # clear
         
    #end while
    result[l].extend(ElecStatus) # store current loop ElecStatus
  #end for
  
# write result
with open(result_file, 'w') as out_file:
  out = csv.writer(out_file, delimiter=',')
  for i in range(0, len(GISdataStr)-1):
    for l in range(0, len(Limits[1])):
      GISdataStr[i+1].append(result[l][i])

  for l in range(0, len(Limits[1])):
      GISdataStr[0].append(GISdataStr[0][3])

  out.writerows(header+GISdataStr)
