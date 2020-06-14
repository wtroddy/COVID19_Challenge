"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
from glob import glob
import pandas as pd
import numpy as np
import csv_to_sqlite


### dir management
train_data_dir = "../data/csv/train/"
test_data_dir = "../data/csv/test/"

# sqlite
sqlite_dir = "../data/sqlite/"

### list files 
# train files
train_files = glob(train_data_dir+"*.csv")
# test files
test_files = glob(train_data_dir+"*.csv")

### convert csv files to sqlite 
options = csv_to_sqlite.CsvOptions(typing_style="full", encoding="windows-1250") 
csv_to_sqlite.write_csv(train_files, sqlite_dir+"covid_train.sqlite", options)
csv_to_sqlite.write_csv(test_files, sqlite_dir+"covid_test.sqlite", options)

### load train data
## as a loop
# train_df = {}
# for f in train_files[0:2]:
#     train_df[f.split("\\")[1].split(".csv")[0]] = pd.read_csv(f)
    
#train_conditions = pd.read_csv(train_data_dir + "conditions.csv")
