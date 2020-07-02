SELECT SOURCE, PATIENT, CODE, DESCRIPTION, SUM(num) AS num
FROM (/* raw query, doing it this way to handle null values in the rx class? or nulls? */
		/* conditions_covid_epochs */
		SELECT 'conditions' AS SOURCE, PATIENT, CODE, DESCRIPTION, COUNT(*) AS num
		FROM conditions_covid_epochs
		WHERE pre_covid_condition = 1 OR COVID_FLAG = 0
		GROUP BY PATIENT, CODE, DESCRIPTION
		UNION 
		/* medications_covid_epochs_class */
		SELECT 'medications' AS SOURCE, PATIENT, COALESCE(classId, CODE) AS CODE, COALESCE(name, DESCRIPTION) AS DESCRIPTION, COUNT(*) AS num
		FROM medications_covid_epochs_class
		WHERE pre_covid_medication = 1 OR COVID_FLAG = 0
		GROUP BY PATIENT, CODE, DESCRIPTION
		UNION 
		/* encounters_covid_epochs -- picking either reasoncode or code if reasoncode is null */
		SELECT 'encounters' AS SOURCE, PATIENT, COALESCE(REASONCODE, CODE) AS CODE, COALESCE(REASONDESCRIPTION, DESCRIPTION) AS DESCRIPTION, COUNT(*) AS num
		FROM encounters_covid_epochs
		WHERE pre_covid_condition = 1 OR COVID_FLAG = 0
		GROUP BY PATIENT, CODE, DESCRIPTION
	) as raw
GROUP BY SOURCE, PATIENT, CODE, DESCRIPTION; 