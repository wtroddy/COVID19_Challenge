/* ventilated */
DROP TABLE IF EXISTS covid_pts_vent;
CREATE TABLE covid_pts_vent AS
SELECT DISTINCT PATIENT, '1' AS VENT_FLAG
FROM procedures
WHERE CODE = '26763009' AND PATIENT IN (SELECT PATIENT FROM conditions WHERE CODE = '840539006');

/* ICU */
DROP TABLE IF EXISTS covid_pts_icu;
CREATE TABLE covid_pts_icu AS
SELECT DISTINCT PATIENT, '1' AS ICU_FLAG, 
				START, STOP,
                 JulianDay(STOP)-JulianDay(START) AS ICU_DAYS
FROM encounters
WHERE CODE = '305351004' AND PATIENT IN (SELECT PATIENT FROM conditions WHERE CODE = '840539006');

/* COVID Conditions Patients */
DROP TABLE IF EXISTS conditions_covid;
CREATE TABLE conditions_covid AS 
SELECT *, '1' AS COVID_FLAG FROM conditions WHERE conditions.CODE = '840539006';

/* COVID POS TEST */
DROP TABLE IF EXISTS covid_test_pos;
CREATE TABLE covid_test_pos AS 
SELECT DISTINCT PATIENT, '1' AS COVID_POS_TEST_FLAG FROM observations WHERE observations.CODE = '94531-1' AND observations.VALUE = 'Detected (qualifier value)';

/* COVID NEG TEST */
DROP TABLE IF EXISTS covid_test_neg;
CREATE TABLE covid_test_neg AS 
SELECT DISTINCT PATIENT, '1' AS COVID_NEG_TEST_FLAG FROM observations WHERE observations.CODE = '94531-1' AND observations.VALUE = 'Not detected (qualifier value)';

/* COVID HOSPITALIZATIONS */
DROP TABLE IF EXISTS covid_hosp;
CREATE TABLE covid_hosp AS
SELECT DISTINCT PATIENT, '1' AS HOSP_FLAG FROM encounters WHERE REASONCODE = '840539006.0' AND CODE = '1505002';

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
	conditions_covid.START AS COVID_START,
	conditions_covid.STOP AS COVID_STOP,
	conditions_covid.ENCOUNTER AS COVID_ENCOUNTER,
	COALESCE(conditions_covid.COVID_FLAG, 0) AS COVID_FLAG,
	--- COVID Test POSITIVE Cases
	-- covid_test_pos.DATE AS POS_TEST_DATE,
	-- covid_test_pos.ENCOUNTER AS POS_TEST_ENCOUNTER,
	COALESCE(covid_test_pos.COVID_POS_TEST_FLAG, 0) AS COVID_POS_TEST_FLAG,
	--- COVID Test NEGATIVE Cases
	-- covid_test_neg.DATE AS NEG_TEST_DATE,
	-- covid_test_neg.ENCOUNTER AS NEG_TEST_ENCOUNTER,
	COALESCE(covid_test_neg.COVID_NEG_TEST_FLAG, 0) AS COVID_NEG_TEST_FLAG,
	--- vital status flag
	CASE WHEN DEATHDATE IS NULL THEN 0 ELSE 1 END AS DECEASED,
	--- ages
	conditions_covid.START - BIRTHDATE AS AGE_AT_DX,
	CASE WHEN DEATHDATE IS NOT NULL THEN (DEATHDATE - BIRTHDATE) ELSE NULL END AS AGE_AT_DEATH,
	--- days sick
	COALESCE(JulianDay(conditions_covid.STOP), JulianDay(DEATHDATE) ) - JulianDay(conditions_covid.START) AS DAYS_SICK,
	--- hospitalized
	COALESCE(covid_hosp.HOSP_FLAG, 0) AS HOSP_FLAG,
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