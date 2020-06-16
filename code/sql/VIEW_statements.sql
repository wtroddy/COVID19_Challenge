/* ventilated */
CREATE VIEW covid_pts_vent AS
SELECT DISTINCT PATIENT, '1' AS VENT_FLAG
FROM procedures
WHERE CODE = '26763009' AND PATIENT IN (SELECT PATIENT FROM conditions WHERE CODE = '840539006');

/* ICU */
CREATE VIEW covid_pts_icu AS
SELECT DISTINCT PATIENT, 
                '1' AS ICU_FLAG,
                 JulianDay(STOP)-JulianDay(START) AS ICU_DAYS
FROM encounters
WHERE CODE = '305351004' AND PATIENT IN (SELECT PATIENT FROM conditions WHERE CODE = '840539006');


/* create view of COVID patients
   expects:
    - covid_pts_icu
    - covid_pts_vent
    
   includes: 
    - condition details, demographics, vital status, age at dx and death
    - days sick, hospitalized flag, ventilator flag, icu flag, days in icu
    Expects 
*/
DROP VIEW IF EXISTS covid_pts;
CREATE VIEW covid_pts AS
SELECT conditions.*,
       --- patient data
       BIRTHDATE,
       DEATHDATE,
       RACE,
       ETHNICITY,
       GENDER,
       --- vital status flag
       CASE WHEN DEATHDATE IS NULL THEN 0 ELSE 1 END AS DECEASED,
       --- ages
       conditions.START - BIRTHDATE AS AGE_AT_DX,
       CASE WHEN DEATHDATE IS NOT NULL THEN (DEATHDATE - BIRTHDATE) ELSE NULL END AS AGE_AT_DEATH,
       --- days sick
       COALESCE(JulianDay(conditions.STOP), JulianDay(DEATHDATE) ) - JulianDay(conditions.START) AS DAYS_SICK,
       --- hospitalized
       CASE WHEN conditions.patient IN (
               SELECT DISTINCT PATIENT
                 FROM encounters
                WHERE REASONCODE = '840539006.0' AND 
                      CODE = '1505002'
           )
       THEN 1 ELSE 0 END AS HOSP_FLAG,
       --- Ventilator
       COALESCE(covid_pts_vent.VENT_FLAG, 0) AS VENT_FLAG,
       --- ICU 
       COALESCE(covid_pts_icu.ICU_FLAG, 0) AS ICU_FLAG,
       covid_pts_icu.ICU_DAYS
       --- icu_pts.ICU_FLAG
  FROM patients
       INNER JOIN
       conditions ON patients.Id = conditions.PATIENT
       LEFT JOIN covid_pts_vent ON patients.Id = covid_pts_vent.PATIENT
       LEFT JOIN covid_pts_icu ON patients.Id = covid_pts_icu.PATIENT
 WHERE conditions.CODE = '840539006'
 ;
 
