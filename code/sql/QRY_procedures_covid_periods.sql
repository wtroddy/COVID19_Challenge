DROP TABLE IF EXISTS procedures_covid_epochs;
CREATE TABLE procedures_covid_epochs AS
SELECT procedures.*,
    covid_patient_data.COVID_FLAG,
    --- Pre-Post-During COVID procedures 
    (procedures.DATE < covid_patient_data.COVID_START) AS pre_covid_procedure,
    (procedures.DATE > covid_patient_data.COVID_START) AS post_covid_procedure,
    (procedures.DATE BETWEEN covid_patient_data.COVID_START AND COALESCE(covid_patient_data.COVID_STOP,covid_patient_data.COVID_START)) AS during_covid_procedure
FROM covid_patient_data
INNER JOIN procedures ON covid_patient_data.Id = procedures.PATIENT
;