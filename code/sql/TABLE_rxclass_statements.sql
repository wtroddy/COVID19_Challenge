DROP TABLE IF EXISTS medications_covid_epochs_class;
CREATE TABLE medications_covid_epochs_class AS 
SELECT *
FROM medications_covid_epochs
LEFT JOIN VACLASS ON medications_covid_epochs.CODE = VACLASS.input_id;