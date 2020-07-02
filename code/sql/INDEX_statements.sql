/* PK Indexes */ 
CREATE UNIQUE INDEX idx_careplans_id ON careplans (Id);
CREATE UNIQUE INDEX idx_encounters_id ON encounters (Id);
CREATE UNIQUE INDEX idx_imaging_studies_id ON imaging_studies (Id);
CREATE UNIQUE INDEX idx_organizations_id ON organizations (Id);
CREATE UNIQUE INDEX idx_patients_id ON patients (Id);
CREATE UNIQUE INDEX idx_payers_id ON payers (Id);
CREATE UNIQUE INDEX idx_providers_id ON providers (Id);

