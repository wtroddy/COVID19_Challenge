# Predicting COVID-19 health outcomes from patient’s historical conditions and medications with XGBoost

## Description: 
In this present work, patient demographics, historical conditions, and the drug classes of historically prescribed medications are used to predict COVID-19 related health outcomes. Data preprocessing and cleaning was conducted in SQLite and the modeling was conducted in python leveraging the XGBoost package. Model features were extracted from the provided synthetic dataset and additional details on drug class were extracted from RxMix. This work is submitted by an individual. 

## Methods:
### Case Definition:
COVID-19 cases were identified from the challenge description. For the purposes of this model "Pre-COVID" events are defined as being 14 days prior to the START date of the patient's COVID diagnosis in the conditions table. This was done to remove bias from recent conditions such as fever, cough that pre-date the actual diagnoses of the disease and safely pick a window where the patient would have not contracted the virus resulting in a better indicator of their historical conditions and potential predictors.

### Model:
The python XGBoost package function “XGBClassifier” was used for this modelling. Default settings were used except for max depth which was set to 10 and the learning rate was set to 0.05. Under initial testing scenarios with a 30% testing size the models performed reasonably well and reach an apparent threshold of performance without risking overtraining. 

### Feature Selection:
Preliminary models explored the use of several input features, but ultimately final models included all previously diagnosed conditions and VA drug classes that appeared in both the training and testing datasets. Conditions for pregnancy and miscarriage were excluded due to not being representative of the true data. Additional demographic variables for gender, race, ethnicity, and age were also included. Age was defined as being the patient’s age at death or their age in June 2020. Although, some features were ranked of little to no importance during training these were still included in the final model in order to best capture the diversity of the dataset. 
### Feature Encoding:
Features were encoded by using a simple frequency approach, e.g. each condition or medication was converted into a count of instances that this historically had been associated with the patient. Demographic variables were coded as numbers or “dummy variables”. Outcome measures that were binary in nature (such as COVID and ventilator status) were representing as boolean values. Outcome measures with days counts were represented as continuous integers rounded to whole numbers where NULL values were assumed to be zero days. 

## Links:
The code for this project is available at: https://github.com/wtroddy/COVID19_Challenge
