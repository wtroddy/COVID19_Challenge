"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
from glob import glob
import csv_to_sqlite
import sqlite3

### dir management
train_data_dir = "../data/csv/train/"
test_data_dir = "../data/csv/test/"

# sqlite
sqlite_dir = "../data/sqlite/"

### list files 
# train files
train_files = glob(train_data_dir+"*.csv")
# test files
test_files = glob(test_data_dir+"*.csv")

### load in sql statements for cleaning 
sql_statements = open("./sql/Py_SQL_Statements_COVID_DB.sql", "r").read()

### convert csv files to sqlite 
options = csv_to_sqlite.CsvOptions(typing_style="full")
# test db
csv_to_sqlite.write_csv(test_files, sqlite_dir+"covid_test.sqlite", options)
test_db = sqlite3.connect(sqlite_dir+"covid_test.sqlite")
test_db.execute(sql_statements)

# train db
csv_to_sqlite.write_csv(train_files, sqlite_dir+"covid_train.sqlite", options)
train_db = sqlite3.connect(sqlite_dir+"covid_train.sqlite")
train_db.execute(sql_statements)
