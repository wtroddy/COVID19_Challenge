"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from xgboost_model import TrainModel

# options
pd.set_option('display.max_columns', 10)

### dir management
# sqlite
sqlite_dir = "../data/sqlite/"

### load train data
# set db object
train_db = sqlite3.connect(sqlite_dir+"covid_train.sqlite")
test_db = sqlite3.connect(sqlite_dir+"covid_test.sqlite")

# load training patient data
train_pts = pd.read_sql_query("SELECT * FROM covid_patient_data", train_db)

# load test data
test_pts = pd.read_sql_query("SELECT * FROM covid_patient_data", test_db)


# load conditions 
qry = """SELECT PATIENT, CODE, DESCRIPTION, COUNT(*) AS num
         FROM conditions_covid_epochs
         WHERE pre_covid_condition = 1 OR pre_covid_condition IS NULL
         GROUP BY PATIENT, CODE, DESCRIPTION;"""

pts_conditions = pd.read_sql_query(qry, train_db) 

pts_conditions['CODE'] = 'snomed_code_'+pts_conditions['CODE'].astype(str)
pts_conditions['DESCRIPTION'] = pts_conditions['DESCRIPTION'].replace('\W', '', regex=True)
# pts_conditions['DESCRIPTION'].replace('\s', '_', regex=True).replace('\\(', '', regex=True).replace('\\)', '', regex=True)

# wide
#pts_conditions_wide = pts_conditions.pivot(index = "PATIENT", columns = "CODE", values = "num")
pts_conditions_wide = pts_conditions.pivot(index = "PATIENT", columns = "DESCRIPTION", values = "num")

m = pd.merge(train_pts, pts_conditions_wide, left_on = 'Id', right_on = 'PATIENT', how = 'left')
m = m.fillna(0)

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

### select input columns 
x_columns = np.append(pts_conditions_wide.columns.values, ["GENDER", "RACE", "ETHNICITY", "AGE_AT_DX"])

### conditions model
#y = m.loc[:,'COVID_FLAG']
y = m.loc[:, 'ICU_FLAG']
x = m.loc[:, x_columns]

# change type
x = x.astype(int)
y = y.astype(int)

# split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

### xgboost training 
from xgboost import XGBClassifier 
model = XGBClassifier()
model.fit(X_train,y_train)

### features
FeatureImportances = pd.DataFrame({'FeatureName':x_columns, 'FeatureImportance':model.feature_importances_})

### xgboost testing
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]
# evaluate predictions
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))


### plot tree
from xgboost import plot_tree
plot_tree(model, rankdir='LR')
fig = plt.gcf()
fig.set_size_inches(150, 100)
fig.savefig('tree_GenderEthnicRace.png')