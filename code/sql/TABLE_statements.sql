/***** VIEWS *****/
/* COVID ventilated patients */
DROP VIEW IF EXISTS covid_pts_vent;
CREATE VIEW covid_pts_vent AS
SELECT DISTINCT PATIENT, '1' AS VENT_FLAG
FROM procedures
WHERE CODE = '26763009' AND PATIENT IN (SELECT PATIENT FROM conditions WHERE CODE = '840539006');

/* ICU patients and duration */
DROP VIEW IF EXISTS covid_pts_icu;
CREATE VIEW covid_pts_icu AS
SELECT DISTINCT PATIENT, '1' AS ICU_FLAG, 
				START, STOP,
                 JulianDay(STOP)-JulianDay(START) AS ICU_DAYS
FROM encounters
WHERE CODE = '305351004' AND PATIENT IN (SELECT PATIENT FROM conditions WHERE CODE = '840539006');

/* COVID Conditions Patients */
DROP VIEW IF EXISTS conditions_covid;
CREATE VIEW conditions_covid AS 
SELECT *, '1' AS COVID_FLAG FROM conditions WHERE conditions.CODE = '840539006';

/* COVID POS TEST */
DROP VIEW IF EXISTS covid_test_pos;
CREATE VIEW covid_test_pos AS 
SELECT DISTINCT PATIENT, '1' AS COVID_POS_TEST_FLAG FROM observations WHERE observations.CODE = '94531-1' AND observations.VALUE = 'Detected (qualifier value)';

/* COVID NEG TEST */
DROP VIEW IF EXISTS covid_test_neg;
CREATE VIEW covid_test_neg AS 
SELECT DISTINCT PATIENT, '1' AS COVID_NEG_TEST_FLAG FROM observations WHERE observations.CODE = '94531-1' AND observations.VALUE = 'Not detected (qualifier value)';

/* COVID HOSPITALIZATIONS */
DROP VIEW IF EXISTS covid_hosp;
CREATE VIEW covid_hosp AS
SELECT DISTINCT PATIENT, '1' AS HOSP_FLAG,
				START, STOP,
				JulianDay(STOP)-JulianDay(START) AS HOSP_DAYS
FROM encounters WHERE REASONCODE = '840539006.0' AND CODE = '1505002';

/***** TABLES *****/
/* Patients + COVID Data Flags */
DROP TABLE IF EXISTS covid_patient_data;
CREATE TABLE covid_patient_data AS
SELECT --- patient data
	Id,
	BIRTHDATE,
	DEATHDATE,
	RACE,
	ETHNICITY,
	GENDER,
	--- COVID+ Cases
	(conditions_covid.START-14) AS PRE_COVID_DATE,
	conditions_covid.START AS COVID_START,
	conditions_covid.STOP AS COVID_STOP,
	conditions_covid.ENCOUNTER AS COVID_ENCOUNTER,
	COALESCE(conditions_covid.COVID_FLAG, 0) AS COVID_FLAG,
	--- COVID Test POSITIVE Cases
	COALESCE(covid_test_pos.COVID_POS_TEST_FLAG, 0) AS COVID_POS_TEST_FLAG,
	--- COVID Test NEGATIVE Cases
	COALESCE(covid_test_neg.COVID_NEG_TEST_FLAG, 0) AS COVID_NEG_TEST_FLAG,
	--- vital status flag
	CASE WHEN DEATHDATE IS NULL THEN 0 ELSE 1 END AS DECEASED,
	CASE WHEN DEATHDATE IS NULL AND COVID_FLAG = '1' THEN 1 END AS COVID_DECEASED,
	--- ages
	conditions_covid.START - BIRTHDATE AS AGE_AT_DX,
	CASE WHEN DEATHDATE IS NOT NULL THEN (DEATHDATE - BIRTHDATE) ELSE NULL END AS AGE_AT_DEATH,
	COALESCE((DEATHDATE-BIRTHDATE), ('2020-06-01'-BIRTHDATE)) AS AGE_AT_2020_OR_DEATH,
	--- days sick
	COALESCE(JulianDay(conditions_covid.STOP), JulianDay(DEATHDATE) ) - JulianDay(conditions_covid.START) AS DAYS_SICK,
	--- hospitalized
	COALESCE(covid_hosp.HOSP_FLAG, 0) AS HOSP_FLAG,
	covid_hosp.START AS HOSP_START,
	covid_hosp.STOP AS HOSP_STOP,
	covid_hosp.HOSP_DAYS,
	--- Ventilator
	COALESCE(covid_pts_vent.VENT_FLAG, 0) AS VENT_FLAG,
	--- ICU 
	COALESCE(covid_pts_icu.ICU_FLAG, 0) AS ICU_FLAG,
	covid_pts_icu.START AS ICU_START,
	covid_pts_icu.STOP AS ICU_STOP,
	covid_pts_icu.ICU_DAYS
  FROM patients
	LEFT JOIN conditions_covid ON patients.Id = conditions_covid.PATIENT
	LEFT JOIN covid_test_pos ON patients.Id = covid_test_pos.PATIENT
	LEFT JOIN covid_test_neg ON patients.Id = covid_test_neg.PATIENT
	LEFT JOIN covid_hosp ON patients.Id = covid_hosp.PATIENT 
	LEFT JOIN covid_pts_vent ON patients.Id = covid_pts_vent.PATIENT
	LEFT JOIN covid_pts_icu ON patients.Id = covid_pts_icu.PATIENT
 ;

/* Conditions + COVID Epochs */
DROP TABLE IF EXISTS conditions_covid_epochs;
CREATE TABLE conditions_covid_epochs AS
 SELECT conditions.*,
    covid_patient_data.COVID_FLAG,
    --- Pre-Post-During COVID Conditions 
    (conditions.START < covid_patient_data.PRE_COVID_DATE) AS pre_covid_condition,
    (conditions.START > covid_patient_data.PRE_COVID_DATE) AS post_covid_condition,
    (conditions.START BETWEEN covid_patient_data.PRE_COVID_DATE AND COALESCE(covid_patient_data.COVID_STOP,covid_patient_data.PRE_COVID_DATE)) AS during_covid_condition,
    --- Pre-Post-During ICU Conditions 
    (conditions.START < covid_patient_data.ICU_START) AS pre_icu_condition,
    (conditions.START > covid_patient_data.ICU_STOP) AS post_icu_condition,
    (conditions.START BETWEEN covid_patient_data.ICU_START AND covid_patient_data.ICU_STOP) AS during_icu_condition,
    --- Comorbid Conditions
    (MAX(START, PRE_COVID_DATE)<=MIN(COALESCE(STOP,COVID_STOP,DEATHDATE), COALESCE(COVID_STOP,covid_patient_data.DEATHDATE))) AS comorbid_condition_flag
FROM covid_patient_data
LEFT JOIN conditions ON covid_patient_data.Id = conditions.PATIENT
;

/* Encounters + COVID Epochs */
DROP TABLE IF EXISTS encounters_covid_epochs;
CREATE TABLE encounters_covid_epochs AS
 SELECT encounters.*,
    covid_patient_data.COVID_FLAG,
    --- Pre-Post-During COVID Conditions 
    (JulianDay(encounters.START) < JulianDay(covid_patient_data.PRE_COVID_DATE)) AS pre_covid_condition,
    (JulianDay(encounters.START) > JulianDay(covid_patient_data.PRE_COVID_DATE)) AS post_covid_condition,
    (JulianDay(encounters.START) BETWEEN JulianDay(covid_patient_data.PRE_COVID_DATE) AND COALESCE(JulianDay(covid_patient_data.COVID_STOP),JulianDay(covid_patient_data.PRE_COVID_DATE))) AS during_covid_condition,
    --- Pre-Post-During ICU Conditions 
    (JulianDay(encounters.START) < JulianDay(covid_patient_data.ICU_START)) AS pre_icu_condition,
    (JulianDay(encounters.START) > JulianDay(covid_patient_data.ICU_STOP)) AS post_icu_condition,
    (JulianDay(encounters.START) BETWEEN JulianDay(covid_patient_data.ICU_START) AND covid_patient_data.ICU_STOP) AS during_icu_condition,
    --- Comorbid Conditions
    (MAX(JulianDay(encounters.START), JulianDay(covid_patient_data.PRE_COVID_DATE)) <= MIN(COALESCE(JulianDay(encounters.STOP), 
																								JulianDay(covid_patient_data.COVID_STOP), 
																								JulianDay(covid_patient_data.DEATHDATE)),
																					  COALESCE(JulianDay(covid_patient_data.COVID_STOP),
																								JulianDay(covid_patient_data.DEATHDATE))
																					   )
	) AS comorbid_condition_flag
FROM covid_patient_data
LEFT JOIN encounters ON covid_patient_data.Id = encounters.PATIENT
;

/* Medications + COVID epochs */
DROP TABLE IF EXISTS medications_covid_epochs;
CREATE TABLE medications_covid_epochs AS
SELECT medications.*,
    covid_patient_data.COVID_FLAG,
    --- Pre-Post-During COVID medications 
    (medications.START < covid_patient_data.PRE_COVID_DATE) AS pre_covid_medication,
    (medications.START > covid_patient_data.PRE_COVID_DATE) AS post_covid_medication,
    (medications.START BETWEEN covid_patient_data.PRE_COVID_DATE AND COALESCE(covid_patient_data.COVID_STOP,covid_patient_data.PRE_COVID_DATE)) AS during_covid_medication,
    --- Comorbid medications
    (MAX(START, PRE_COVID_DATE)<=MIN(COALESCE(STOP,COVID_STOP,DEATHDATE), COALESCE(COVID_STOP,covid_patient_data.DEATHDATE))) AS comorbid_medication_flag
FROM covid_patient_data
INNER JOIN medications ON covid_patient_data.Id = medications.PATIENT
;



