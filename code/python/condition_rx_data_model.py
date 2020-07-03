"""
Script to load precisionFDA COVID 19
    https://precision.fda.gov/challenges/11

"""

# libs
import os
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from xgboost_model import xgboost_model

# change dir
main_dir = "C:/Users/wtrod/Documents/precisionFDA/COVID19_Challenge/"
os.chdir(main_dir)

# set vars
input_dict = {"test_db": ["./data/sqlite/covid_test.sqlite", 
                          "./data/flat_files/test_data.csv",
                          "./data/flat_files/test_feature_names.csv"
                          ],
              "train_db": ["./data/sqlite/covid_train.sqlite",
                           "./data/flat_files/train_data.csv",
                          "./data/flat_files/train_feature_names.csv"]
              }

### load train data
train_pt_data = pd.read_csv(input_dict["train_db"][1])
train_feature_names = pd.read_csv(input_dict["train_db"][2])
# select input columns 
train_x_columns = np.append(train_feature_names.values, ["GENDER", "RACE", "ETHNICITY", "AGE_AT_2020_OR_DEATH"])

### load test data
test_pt_data = pd.read_csv(input_dict["test_db"][1])
test_feature_names = pd.read_csv(input_dict["test_db"][2])
# select input columns 
test_x_columns = np.append(test_feature_names.values, ["GENDER", "RACE", "ETHNICITY", "AGE_AT_2020_OR_DEATH"])

### get common features
x_columns = np.intersect1d(train_x_columns, test_x_columns)

# features
train_x = train_pt_data.loc[:, x_columns]
#test_x = test_pt_data.loc[:, x_columns]

### outcomes
y_outcomes = [['COVID_FLAG', bool], 
              ['HOSP_DAYS', int], 
              ['ICU_DAYS', int], 
              ['VENT_FLAG', bool], 
              ['COVID_DECEASED', bool]]

# init class
xgm = xgboost_model()

for i in y_outcomes:    
    ### select data
    # outcomes 
    if i[1] == int:
        train_y = train_pt_data.loc[:,i[0]].fillna(0).astype(i[1])
    else:
        train_y = train_pt_data.loc[:,i[0]].astype(i[1])
           
    # model name 
    mod_name = (i[0])
    
    # set output folder
    xgm.setOutputFolder(main_dir+"./output/"+mod_name)
    
    # run model
    model = xgm.TrainEvalModel(train_x, train_y, mod_name)
    
    # print tree
    xgm.PlotModelTree(model, mod_name)
    
    # features
    FeatureImportances = pd.DataFrame({'FeatureName':x_columns, 'FeatureImportance':model.feature_importances_})
