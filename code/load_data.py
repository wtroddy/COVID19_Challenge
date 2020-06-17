"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
import sqlite3
import pandas as pd
import numpy as np

### dir management
# sqlite
sqlite_dir = "../data/sqlite/"

### load train data
# set db object
train_db = sqlite3.connect(sqlite_dir+"covid_train.sqlite")
# load training patient data
train_pts = pd.read_sql_query("SELECT * FROM covid_patient_data", train_db)

### example model
# predictor variables
x = train_pts.loc[:,['COVID_FLAG','AGE_AT_DX','AGE_AT_DEATH','DAYS_SICK','VENT_FLAG']]
# fix column types
x.loc[:,'COVID_FLAG'] = x.loc[:,'COVID_FLAG'].astype('int')
x.loc[:,'VENT_FLAG'] = x.loc[:,'VENT_FLAG'].astype('int')

# outcome variable 
y = train_pts['DECEASED']

### xgboost training 
from xgboost import XGBClassifier 
model = XGBClassifier()
model.fit(x,y)

### xgboost testing
y_pred = model.predict(x)
predictions = [round(value) for value in y_pred]
# evaluate predictions
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))