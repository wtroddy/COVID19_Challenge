SELECT conditions.*,
    covid_patient_data.COVID_START,
    covid_patient_data.COVID_STOP,
    covid_patient_data.ICU_START,
    covid_patient_data.ICU_STOP,
    --- Pre-Post-During COVID Conditions 
    (conditions.START < covid_patient_data.COVID_START) AS pre_covid_condition,
    (conditions.START > covid_patient_data.COVID_START) AS post_covid_condition,
    (conditions.START BETWEEN covid_patient_data.COVID_START AND COALESCE(covid_patient_data.COVID_STOP,covid_patient_data.COVID_START)) AS during_covid_condition,
	--- Pre-Post-During ICU Conditions 
    (conditions.START < covid_patient_data.ICU_START) AS pre_icu_condition,
    (conditions.START > covid_patient_data.ICU_STOP) AS post_icu_condition,
    (conditions.START BETWEEN covid_patient_data.ICU_START AND covid_patient_data.ICU_STOP) AS during_icu_condition	
FROM covid_patient_data
LEFT JOIN conditions ON covid_patient_data.Id = conditions.PATIENT
WHERE covid_patient_data.COVID_FLAG = '1'
---GROUP BY CODE, DESCRIPTION
LIMIT 25
;