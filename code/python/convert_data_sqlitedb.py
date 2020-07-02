"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
from glob import glob
import csv_to_sqlite
import sqlite3

###################### Functions ##########################
### create covid database functions
def CreateCovidDB(input_directory, db_directory, db_name):
    """ doc string
    """
    # get a list of input csv files 
    input_files = glob(input_directory+"*.csv")
    # create database 
    options = csv_to_sqlite.CsvOptions(typing_style="full")
    csv_to_sqlite.write_csv(input_files, (db_directory+db_name), options)
    
### execute sql statements on database 
def ExecSQLStatement(db_directory, db_name, sql_statement):
    """doc string
    """
    # read in text
    sql_text = open(sql_statement, "r").read()
    # connect to db 
    db_con = sqlite3.connect(db_directory+db_name)
    # execute statement
    db_con.executescript(sql_text)
############################################################

###################### ScriptBody ##########################
### set vars
input_dict = {"test_db": ["./data/csv/test/", "./data/sqlite/", "covid_test.sqlite"],
              "train_db": ["./data/csv/train/", "./data/sqlite/", "covid_train.sqlite"]
              }

sql_files = ["./code/sql/INDEX_statements.sql",
             "./code/sql/UPDATE_statements.sql",
             "./code/sql/TABLE_statements.sql"
             ]

### loop to create dbs 
print("Creating Databases!")
for i in input_dict:
    # print starting
    print("prepararing: ", i, "\n")
    
    ### create dbs 
    # create train db
    CreateCovidDB(input_dict[i][0], input_dict[i][1], input_dict[i][2])

    # print confirmation
    print("finished creating: ", i, "\n\n\n")


### loop to run sql
print("Running SQL Statements!")
for i in input_dict:    
    # print starting 
    print("running sql statements for: ", i, "\n")
    
    ### sql statements
    for s in sql_files:
        # print start notice
        print("about to run sql statement: ", s)
        # run statement
        ExecSQLStatement(input_dict[i][1], input_dict[i][2], s)
        # print confimration
        print("finished running statement!")
        print("***************************\n")
    
    # print confirmation
    print("finished running sql statements for: ", i, "\n\n\n")
############################################################