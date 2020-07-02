### script to export the unique rxnorm ids from the dbs


# libs
import os
import pandas as pd
import sqlite3


### setup 
# setup pd df
unq_medications = pd.DataFrame(columns = ["CODE"])

### set vars
input_dict = {"test_db": ["./data/sqlite/covid_test.sqlite"],
              "train_db": ["./data/sqlite/covid_train.sqlite"]
              }


### read in data
for db in input_dict:
    # connect to db
    db_con = sqlite3.connect(input_dict[db][0])
    
    # read data 
    rxnorm_codes = pd.read_sql_query("SELECT DISTINCT CODE FROM medications;", db_con)
    
    # add to df 
    unq_medications = unq_medications.append(rxnorm_codes)

### drop duplicate values 
unq_medications = unq_medications.drop_duplicates()

###
unq_medications.to_csv("./data/rxnorm/rxnorm_codes.txt", header=None, index=None, sep = ' ')