CREATE DATABASE bonking_data;

\c bonking_data;

CREATE TABLE last_bonks (
    creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    bonked TEXT NOT NULL,
    bonker TEXT NOT NULL
);