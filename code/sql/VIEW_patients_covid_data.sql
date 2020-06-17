DROP TABLE IF EXISTS patients_covid_data;
CREATE TABLE patients_covid_data AS
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
	-- test_covid_pos.DATE AS POS_TEST_DATE,
	-- test_covid_pos.ENCOUNTER AS POS_TEST_ENCOUNTER,
	COALESCE(test_covid_pos.COVID_POS_TEST_FLAG, 0) AS COVID_POS_TEST_FLAG,
	--- COVID Test NEGATIVE Cases
	-- test_covid_neg.DATE AS NEG_TEST_DATE,
	-- test_covid_neg.ENCOUNTER AS NEG_TEST_ENCOUNTER,
	COALESCE(test_covid_neg.COVID_NEG_TEST_FLAG, 0) AS COVID_NEG_TEST_FLAG,
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
	covid_pts_icu.ICU_DAYS
  FROM patients
	LEFT JOIN conditions_covid ON patients.Id = conditions_covid.PATIENT
	LEFT JOIN test_covid_pos ON patients.Id = test_covid_pos.PATIENT
	LEFT JOIN test_covid_neg ON patients.Id = test_covid_neg.PATIENT
	LEFT JOIN covid_hosp ON patients.Id = covid_hosp.PATIENT 
	LEFT JOIN covid_pts_vent ON patients.Id = covid_pts_vent.PATIENT
	LEFT JOIN covid_pts_icu ON patients.Id = covid_pts_icu.PATIENT
 ;