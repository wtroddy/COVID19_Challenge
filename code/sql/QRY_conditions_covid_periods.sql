SELECT conditions.*,
    covid_patient_data.COVID_FLAG,
    --- Pre-Post-During COVID Conditions 
    (conditions.START < covid_patient_data.COVID_START) AS pre_covid_condition,
    (conditions.START > covid_patient_data.COVID_START) AS post_covid_condition,
    (conditions.START BETWEEN covid_patient_data.COVID_START AND COALESCE(covid_patient_data.COVID_STOP,covid_patient_data.COVID_START)) AS during_covid_condition,
    --- Pre-Post-During ICU Conditions 
    (conditions.START < covid_patient_data.ICU_START) AS pre_icu_condition,
    (conditions.START > covid_patient_data.ICU_STOP) AS post_icu_condition,
    (conditions.START BETWEEN covid_patient_data.ICU_START AND covid_patient_data.ICU_STOP) AS during_icu_condition,
    --- Comorbid Conditions
    (MAX(START, COVID_START)<=MIN(COALESCE(STOP,COVID_STOP,DEATHDATE), COALESCE(COVID_STOP,covid_patient_data.DEATHDATE))) AS comorbid_condition_flag
FROM covid_patient_data
INNER JOIN conditions ON covid_patient_data.Id = conditions.PATIENT
;

