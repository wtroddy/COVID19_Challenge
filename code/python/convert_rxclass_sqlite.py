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
rxn_dir = "./data/products/Rx/RxNorm_Codes/RxNorm_getClass_VA-VAExtended_xml/"
rxn_file = rxn_dir+"VA_Class.xml"

# read in xml file
import xml.etree.ElementTree as ET
rxclass_tree = ET.parse(rxn_file)
rxclass_root = rxclass_tree.getroot()

# setup pd df
#dfcols = ['input_id', 'relaSource', 'term_type', 'drugName', 'RXCUI', 'rela', 'classId', 'name', 'classType']
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
                       #output.find('term_type').text,
                       #output.find('drugName').text,
                       #output.find('RXCUI').text,
                       #output.find('rela').text,
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