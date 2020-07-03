SELECT SOURCE, PATIENT, ALL_CODES, ALL_DESCRIPTIONS, SUM(num) AS num
FROM (/* raw query, doing it this way to handle null values in the rx class? or nulls? */
		/* conditions_covid_epochs */
		SELECT 'conditions' AS SOURCE, PATIENT, CODE AS ALL_CODES, DESCRIPTION AS ALL_DESCRIPTIONS, COUNT(*) AS num
		FROM conditions_covid_epochs
		WHERE pre_covid_condition = 1 OR COVID_FLAG = 0
		GROUP BY PATIENT, ALL_CODES, ALL_DESCRIPTIONS
		UNION 
		/* medications_covid_epochs_class */
		SELECT 'medications' AS SOURCE, PATIENT, COALESCE(classId, CODE) AS ALL_CODES, COALESCE(name, DESCRIPTION) AS ALL_DESCRIPTIONS, COUNT(*) AS num
		FROM medications_covid_epochs_class
		WHERE pre_covid_medication = 1 OR COVID_FLAG = 0
		GROUP BY PATIENT, ALL_CODES, ALL_DESCRIPTIONS
		/* UNION 
		 encounters_covid_epochs -- picking either reasoncode or code if reasoncode is null 
		SELECT 'encounters' AS SOURCE, PATIENT, COALESCE(REASONCODE, CODE) AS ALL_CODES, COALESCE(REASONDESCRIPTION, DESCRIPTION) AS ALL_DESCRIPTIONS, COUNT(*) AS num
		FROM encounters_covid_epochs
		WHERE pre_covid_condition = 1 OR COVID_FLAG = 0
		GROUP BY PATIENT, ALL_CODES, ALL_DESCRIPTIONS
		*/
	) as raw
GROUP BY SOURCE, PATIENT, ALL_CODES, ALL_DESCRIPTIONS; 