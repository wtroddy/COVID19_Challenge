"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
import os 
import sqlite3
import pandas as pd

# options
pd.set_option('display.max_columns', 10)

### set vars
input_dict = {"test_db": ["./data/sqlite/covid_test.sqlite", 
                          "./data/flat_files/test_data.csv",
                          "./data/flat_files/test_feature_names.csv"
                          ],
              "train_db": ["./data/sqlite/covid_train.sqlite",
                           "./data/flat_files/train_data.csv",
                          "./data/flat_files/train_feature_names.csv"]
              }


### input query
feature_qry_sql = "./code/sql/QRY_PythonInput_statement.sql"
feature_qry = open(feature_qry_sql, "r").read()

#### TO DO: 
    ### change this into a function so that it's not so clunky as a loop 
    ### maybe make this a class with multiple method for loading, cleaning, output
    
for db in input_dict:
    # connect to db
    db_con = sqlite3.connect(input_dict[db][0])
    
    # get patient data 
    pts = pd.read_sql_query("SELECT * FROM covid_patient_data", db_con)
    
    # get feature data
    features = pd.read_sql_query(feature_qry, db_con)
    
    # clean descriptions and codes
    features['ALL_CODES'] = features['SOURCE']+features['ALL_CODES'].astype(str)
    features['ALL_DESCRIPTIONS'] = features['ALL_DESCRIPTIONS'].replace('\W', '', regex=True)
    features['ALL_DESCRIPTIONS'] = features['SOURCE']+features['ALL_DESCRIPTIONS']
    
    # aggregate to remove duplicates
    features_grouped = features.groupby(['PATIENT', 'ALL_DESCRIPTIONS']).sum().reset_index()
    
    # pivot data 
    features_wide = features_grouped.pivot(index = "PATIENT", columns = "ALL_DESCRIPTIONS", values = "num")
    
    # merge with the patient data
    pts_features = pd.merge(pts, features_wide, left_on = 'Id', right_on = 'PATIENT', how = 'left')
    
    ### recode variables as numeric values 
    # gender
    pts_features.GENDER = pts_features.GENDER.replace("F", 0)
    pts_features.GENDER = pts_features.GENDER.replace("M", 1)
    # race
    pts_features.RACE = pts_features.RACE.replace("white", 0)
    pts_features.RACE = pts_features.RACE.replace("asian", 1)
    pts_features.RACE = pts_features.RACE.replace("black", 2)
    pts_features.RACE = pts_features.RACE.replace("native", 3)
    pts_features.RACE = pts_features.RACE.replace("other", 4)
    # ethnicity
    pts_features.ETHNICITY = pts_features.ETHNICITY.replace("nonhispanic", 0)
    pts_features.ETHNICITY = pts_features.ETHNICITY.replace("hispanic", 1) 
    
    # write data 
    pts_features.to_csv(input_dict[db][1], index = False)
    
    # write the feature column names 
    pd.DataFrame(features_wide.columns.values).to_csv(input_dict[db][2], index = False, header=['FeatureNames'])


