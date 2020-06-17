"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
import sqlite3
import pandas as pd
import numpy as np
import matplotlib as plt

### dir management
train_data_dir = "../data/csv/train/"
test_data_dir = "../data/csv/test/"
# sqlite
sqlite_dir = "../data/sqlite/"


### load train data
# db
train_db = sqlite3.connect(sqlite_dir+"covid_train.sqlite")

"""
# tables 
conditions = pd.read_sql_query("SELECT * FROM conditions;", train_db)
medications = pd.read_sql_query("SELECT * FROM medications;", train_db)

pd.read_sql

# qrys
pd.read_sql_query("SELECT CODE, DESCRIPTION, COUNT(*) AS num_dx FROM conditions GROUP BY CODE, DESCRIPTION ORDER BY num_dx DESC;", train_db)

# covid patients
covid_pids = conditions[conditions.CODE == 840539006].PATIENT.unique()
"""

pts = pd.read_sql_query("SELECT * FROM patients_covid_data", train_db)
