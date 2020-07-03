# precisionFDA COVID19 Challenge 
This code was developed for the VHA Innovation Ecosystem and precisionFDA COVID-19 Risk Factor Modeling Challenge. 

The precisionFDA challenge is available at: https://precision.fda.gov/challenges/11

# Data Preprocessing
Data preprocessing was conducted using SQLite. Combining python scripts and SQL statements, enhanced views and tables were used to generate an analytical dataset. With the exception of the medications file, all procesisng used data embedded in the datasets provided by the challenge organizers. 

Scripts used for this step:
	* .\code\python\
		* convert_data_sqlitedb.py: this script first creates sqlite dbs from the train and test csv files and then runs a series of sql statements
	* .\code\sql\

## Medications Preprocessing
In order to leverage the historical medications used by patients while balancing the variety of prescribable content, the RxNorm CUIs were converted to their VA Class using RxMix (https://mor.nlm.nih.gov/RxMix/). In cases where there was no class the RxCUI CODE/DESCRIPTION were used.