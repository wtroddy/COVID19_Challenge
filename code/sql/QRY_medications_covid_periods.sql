DROP TABLE IF EXISTS medications_covid_epochs;
CREATE TABLE medications_covid_epochs AS
SELECT medications.*,
    covid_patient_data.COVID_FLAG,
    --- Pre-Post-During COVID medications 
    (medications.START < covid_patient_data.COVID_START) AS pre_covid_medication,
    (medications.START > covid_patient_data.COVID_START) AS post_covid_medication,
    (medications.START BETWEEN covid_patient_data.COVID_START AND COALESCE(covid_patient_data.COVID_STOP,covid_patient_data.COVID_START)) AS during_covid_medication,
    --- Comorbid medications
    (MAX(START, COVID_START)<=MIN(COALESCE(STOP,COVID_STOP,DEATHDATE), COALESCE(COVID_STOP,covid_patient_data.DEATHDATE))) AS comorbid_medication_flag
FROM covid_patient_data
INNER JOIN medications ON covid_patient_data.Id = medications.PATIENT
;