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



### model name 
mod_name = "COVID_FLAG_BOOL_PreConditions_PreRxClass_Age"

### select input columns 
x_columns = np.append(pts_conditions_wide.columns.values, ["GENDER", "RACE", "ETHNICITY", "AGE_AT_2020_OR_DEATH"])

### conditions model
y = m.loc[:,'COVID_FLAG'].astype(bool)
#y = m.loc[:, 'ICU_FLAG'].astype(bool)
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
    
