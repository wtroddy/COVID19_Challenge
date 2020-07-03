# libs
import os
import pandas as pd
import csv_to_sqlite
import sqlite3

### dir management
# main dir
main_dir = "C:/Users/wtrod/Documents/precisionFDA/COVID19_Challenge/"
os.chdir(main_dir)
# sqlite
sqlite_dir = "./data/sqlite/"
# rxnorm data
rxn_dir = "./data/rxnorm/RxClass_getVAClass/"
rxn_file = rxn_dir+"RxClass_getVAClass.xml"

# read in xml file
import xml.etree.ElementTree as ET
rxclass_tree = ET.parse(rxn_file)
rxclass_root = rxclass_tree.getroot()

# setup pd df
dfcols = ['input_id', 'relaSource', 'classId', 'name', 'classType']
rxclass_df = pd.DataFrame(columns = dfcols)

# fill in dataframe
for child in rxclass_root:
    for input_id in child.iter('input'):
        pass       
    for output in child.iter('output'):
        rxclass_df = rxclass_df.append(
            pd.Series([input_id.text,
                       output.find('relaSource').text,
                       output.find('classId').text,
                       output.find('name').text,
                       output.find('classType').text
                       ], index=dfcols), ignore_index=True)


rxclass_df = rxclass_df.drop_duplicates()

# output 
rxclass_df.to_csv(rxn_dir+"VACLASS.csv", index=False)

# write to sqlite db
options = csv_to_sqlite.CsvOptions(typing_style="full")
csv_to_sqlite.write_csv([rxn_dir+"VACLASS.csv"], sqlite_dir+"covid_train.sqlite", options)
csv_to_sqlite.write_csv([rxn_dir+"VACLASS.csv"], sqlite_dir+"covid_test.sqlite", options)


### update medications_covid_epochs tables 
# set vars
input_dict = {"test_db": ["./data/sqlite/covid_test.sqlite"],
              "train_db": ["./data/sqlite/covid_train.sqlite"]
              }


### sql
sql_text = open("./code/sql/TABLE_rxclass_statements.sql", "r").read()

### read in data
for db in input_dict:
    # connect to db
    db_con = sqlite3.connect(input_dict[db][0])
    
    # statement
    db_con.executescript(sql_text)
    
    
    
    