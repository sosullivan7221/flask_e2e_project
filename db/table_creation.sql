CREATE DATABASE final;

USE final;

CREATE TABLE patient_info (
	patient_id int NOT NULL AUTO_INCREMENT,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    date_of_birth date NOT NULL,
    PRIMARY KEY (patient_id)
		);