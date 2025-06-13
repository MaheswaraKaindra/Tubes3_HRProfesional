-- src/data/schema.sql

DROP TABLE IF EXISTS ApplicationDetail;
DROP TABLE IF EXISTS ApplicantProfile;

CREATE TABLE ApplicantProfile (
    applicant_id INT NOT NULL,
    first_name VARCHAR(50) DEFAULT NULL,
    last_name VARCHAR(50) DEFAULT NULL,
    date_of_birth DATE DEFAULT NULL,
    address VARCHAR(255) DEFAULT NULL,
    phone_number VARCHAR(20) DEFAULT NULL,

    PRIMARY KEY (applicant_id)
);

CREATE TABLE ApplicationDetail (
    detail_id INT NOT NULL,
    applicant_id INT NOT NULL,
    application_role VARCHAR(100) DEFAULT NULL,
    cv_path TEXT,

    FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id),
    PRIMARY KEY (detail_id)
);