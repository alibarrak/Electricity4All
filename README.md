# Electricity4All
this solution was submitted for #Electricity4All challenge https://unite.un.org/ideas/content/electricity4all-python-challenge

### system used specs
* OS: Debian Linux (VirtualBox)
* Processor: AMD 2.7GHz X4
* RAM: 4GB

### sample timing
due to the late start, only small sample were tested (using **debug** variable in the code)
* **5k** lines input > **1m40.483s**
* **10k** lines input > **7m3.465s**
* **20k** lines input

### Usage
there are 2 input files names you need to specify within the code (**input data file** and **input scenario file**)
```
data_file = '40k_in.csv'                      # input data file name (assuming first row is header)
scenario_file = 'scenario1.csv'               # scenario file name (assuming first row is distance as INT and second row as #of people INT)
result_file = scenario_file+'_result.csv'     # result file name

debug = 0   # debug: to break on read data line number provided. 0 to ignore
```

to run, simply type command in terminal:
```
>time python3 h5.py
```

### Output data
at the end of the proccess, result data will be saved in CSV file. All sample tests have **100% match** with provided outputs xlsm file (see challege link for further information)

### notes
according to the challenge requirements, proccess time of the code seems to be slow! possible bug or wrong code interpretation; as never used either language before this time.
