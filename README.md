# precisionFDA COVID19 Challenge 
This code was developed for the VHA Innovation Ecosystem and precisionFDA COVID-19 Risk Factor Modeling Challenge. The precisionFDA challenge is available at: https://precision.fda.gov/challenges/11

This model employs a gradient boosting framework with the use of XGBoost in python and focuses on the use of patients previous conditions and medications to predict the COVID-19 related conditions. 

# Data Preprocessing
Data preprocessing was conducted using SQLite. Combining python scripts and SQL statements, enhanced views and tables were used to generate an analytical dataset. With the exception of the medications file, all procesisng used data embedded in the datasets provided by the challenge organizers. 

Scripts used for this step:
* .\code\python\
	1. convert_data_sqlitedb.py: this script first creates sqlite dbs from the train and test csv files and then runs a series of sql statements
* .\code\sql\
	1. INDEX_statements.sql: *(optional)* use this script to add indexes to the tables with primary keys that are unique 
	2. UPDATE_statements.sql: this file makes some initial updates to tables that are artifacts from the ETL from csv files and prepares the tables for future steps
	3. TABLE_statements.sql: this file creates views and custom tables aggregating and manipulating data into a format that can easily be loaded into python. most variables are generated during this step.

## Medications Preprocessing
In order to leverage the historical medications used by patients while balancing the variety of prescribable content, the RxNorm CUIs were converted to their VA Class using RxMix (https://mor.nlm.nih.gov/RxMix/). In cases where there was no class the RxCUI CODE/DESCRIPTION were used.

Scripts used for this step:
* .\code\python\rxnorm_to_class
	1. export_RxNormIDs.py: this script will create a txt file with the unique rxcui between both testing and training dbs 
	2. convert_rxclass_sqlite.py: this script takes the xml file output from RxMix, converts it to a .csv, loads the drug class details into the sqlite db, and joins the tables.
* .\code\sql\
	1. TABLE_rxclass_statements.sql: referenced by convert_rxclass_sqlite.py to generate the new tables with the VA drug class data added 
	
## Excluded Conditions
The synthetic dataset had a non-realistic representation of pregnancies and miscarriages (confirmed with challenge sponsor) so these were excluded from models.	

# Analytical Dataset and Feature Encoding

## Case Definitions 
Case definitions and time periods are defined in the TABLE_statements.sql sql statements. Case definitions generally followed the guidance provided by the challenge sponsor. 

For the purposes of this model "Pre-COVID" events are defined as being 14 days prior to the START date of the patient's COVID diagnosis in the conditions table. This was done to remove bias from recent conditions such as fever, cough that pre-date the actual diagnoses of the disease and safely pick a window where the patient would have not contracted the virus resulting in a better indicator of their historical conditions and potential predictors.

## Feature Selection

## Feature Encoding 

## scripts 
* .\code\python\
	* covid_data_prep.py: this script loads data from the processed 


# Model Implementation

## testing

## final model 
