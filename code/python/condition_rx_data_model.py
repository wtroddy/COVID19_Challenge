"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
import os 
import sqlite3
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from xgboost_model import xgboost_model


# init class
xgm = xgboost_model()

# options
pd.set_option('display.max_columns', 10)

### dir management
# main dir
main_dir = "C:/Users/wtrod/Documents/precisionFDA/COVID19_Challenge/"
os.chdir(main_dir)
# sqlite
sqlite_dir = "./data/sqlite/"

### load train data
# set db object
train_db = sqlite3.connect(sqlite_dir+"covid_train.sqlite")
test_db = sqlite3.connect(sqlite_dir+"covid_test.sqlite")

# load training patient data
train_pts = pd.read_sql_query("SELECT * FROM covid_patient_data", train_db)

# load test data
test_pts = pd.read_sql_query("SELECT * FROM covid_patient_data", test_db)


# load conditions and medications
# qry = """SELECT PATIENT, CODE, DESCRIPTION, COUNT(*) AS num
#                  FROM conditions_covid_epochs
#                  WHERE (pre_covid_condition = 1 OR pre_covid_condition IS NULL) AND
#                        DESCRIPTION NOT LIKE '%COVID%'
#                  GROUP BY PATIENT, CODE, DESCRIPTION
#         UNION 
#         SELECT PATIENT, CODE, DESCRIPTION, COUNT(*) AS num
#                  FROM medications_covid_epochs_class
#                  WHERE pre_covid_medication = 1 OR pre_covid_medication IS NULL
#                  GROUP BY PATIENT, CODE, DESCRIPTION; """

qry = """SELECT PATIENT, CODE, DESCRIPTION, SUM(num) AS num
        FROM 
        (SELECT PATIENT, CODE, DESCRIPTION, COUNT(*) AS num
         FROM conditions_covid_epochs
         WHERE (pre_covid_condition = 1 OR COVID_FLAG = 0) AND
               DESCRIPTION NOT LIKE '%COVID%'
        GROUP BY PATIENT, CODE, DESCRIPTION
        UNION 
        SELECT PATIENT, 
                COALESCE(classId, CODE) AS CODE, 
                COALESCE(name, DESCRIPTION) AS DESCRIPTION, 
                COUNT(*) AS num
        FROM medications_covid_epochs_class
        WHERE pre_covid_medication = 1 OR COVID_FLAG = 0
        GROUP BY PATIENT, CODE, DESCRIPTION) as raw
        GROUP BY PATIENT, CODE, DESCRIPTION; """


pts_conditions = pd.read_sql_query(qry, train_db) 

pts_conditions['CODE'] = 'snomed_code_'+pts_conditions['CODE'].astype(str)
pts_conditions['DESCRIPTION'] = pts_conditions['DESCRIPTION'].replace('\W', '', regex=True)


# wide
#pts_conditions_wide = pts_conditions.pivot(index = "PATIENT", columns = "CODE", values = "num")
pts_conditions_wide = pts_conditions.pivot(index = "PATIENT", columns = "DESCRIPTION", values = "num")

m = pd.merge(train_pts, pts_conditions_wide, left_on = 'Id', right_on = 'PATIENT', how = 'left')


### recode variables as numeric values 
# gender
m.GENDER = m.GENDER.replace("F", 0)
m.GENDER = m.GENDER.replace("M", 1)
# race
m.RACE = m.RACE.replace("white", 0)
m.RACE = m.RACE.replace("asian", 1)
m.RACE = m.RACE.replace("black", 2)
m.RACE = m.RACE.replace("native", 3)
m.RACE = m.RACE.replace("other", 4)
# ethnicity
m.ETHNICITY = m.ETHNICITY.replace("nonhispanic", 0)
m.ETHNICITY = m.ETHNICITY.replace("hispanic", 1)


### model name 
mod_name = "ICUFLAG_BOOL_PreConditions_PreRxClass"

### select input columns 
x_columns = np.append(pts_conditions_wide.columns.values, ["GENDER", "RACE", "ETHNICITY"]) #, "AGE_AT_DX"])

### conditions model
#y = m.loc[:,'COVID_FLAG'].astype(bool)
y = m.loc[:, 'ICU_FLAG'].astype(bool)
#y = m.loc[:,'DECEASED'].astype(bool)
x = m.loc[:, x_columns]



### run model
model = xgm.TrainModel(x, y, mod_name)

### set output folder
xgm.setOutputFolder(main_dir+"./output/"+mod_name)

### print tree
xgm.PlotModelTree(model, mod_name)

# features
FeatureImportances = pd.DataFrame({'FeatureName':x_columns, 'FeatureImportance':model.feature_importances_})
    
