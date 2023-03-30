CREATE TABLE IF NOT EXISTS profiles (
    profile_val  INTEGER PRIMARY KEY,
    profile_name VARCHAR(32) UNIQUE
);

CREATE TABLE IF NOT EXISTS cities (
    city VARCHAR(64) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS statuses (
    status_val   INTEGER    PRIMARY KEY,
    status_name  VARCHAR(64) UNIQUE
);

CREATE SEQUENCE IF NOT EXISTS user_id_seq START 1;

CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    profile     INTEGER REFERENCES profiles(profile_val),
    is_company  BOOLEAN NOT NULL,
    email       VARCHAR(128) NOT NULL,
    name        VARCHAR(128) NOT NULL,
    birthdate   DATE NOT NULL,
    city        VARCHAR(64) REFERENCES cities(city),
    phone       VARCHAR(16) NOT NULL,
    job         VARCHAR(64)
);

CREATE SEQUENCE IF NOT EXISTS case_id_seq START 1;

CREATE TABLE IF NOT EXISTS cases (
    case_id     INTEGER PRIMARY KEY,
    name        VARCHAR(128) NOT NULL,
    status      INTEGER REFERENCES statuses(status_val),
    claim       INTEGER NOT NULL,
    description TEXT
);

CREATE SEQUENCE IF NOT EXISTS doc_id_seq START 1;

CREATE TABLE IF NOT EXISTS documents (
    doc_id      INTEGER PRIMARY KEY,
    case_id     INTEGER REFERENCES cases(case_id),
    name        VARCHAR(128) NOT NULL,
    link        TEXT UNIQUE
);
