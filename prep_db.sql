-- apply indices to improve lookup speed
CREATE INDEX idx_name_version ON projects (name, version);
CREATE INDEX idx_name_project_id ON urls (project_id);