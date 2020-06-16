/* Zero Legnth Dth Dates to NULL */
UPDATE patients
SET DEATHDATE = NULL 
WHERE length(patients.DEATHDATE) = 0
;

/* Add COVID+ flag to patients table */
--- add column
ALTER TABLE patients 
ADD COVID_PT_FLAG VARCHAR
;

--- flag COVID + patients 
UPDATE patients
SET COVID_PT_FLAG = '1' 
WHERE Id IN (SELECT PATIENT from conditions WHERE conditions.CODE = '840539006')
;

--- flag COVID - patients
UPDATE patients
SET COVID_PT_FLAG = '0'
WHERE COVID_PT_FLAG IS NULL
;

