CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    requirements TEXT,
    salary VARCHAR(100),
    work_format VARCHAR(100)
);