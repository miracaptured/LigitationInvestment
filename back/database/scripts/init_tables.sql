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
    email       VARCHAR(128) UNIQUE NOT NULL,
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

CREATE TABLE IF NOT EXISTS cases_by_users (
    case_id        INTEGER REFERENCES cases(case_id),
    user_id       INTEGER REFERENCES users(user_id),
    PRIMARY KEY (case_id, user_id)
);


INSERT INTO profiles VALUES
(1, 'истец'), (2, 'ответчик'), (3, 'адвокат'), (4, 'юрист');

INSERT INTO cities VALUES
('Москва');

INSERT INTO statuses VALUES
(1, 'на диагностике'), (2, 'на инвестировании');



CREATE OR REPLACE FUNCTION get_cases_by_user(user_id    INTEGER)
RETURNS TABLE (
    case_id     INTEGER,
    name        VARCHAR(128),
    status      INTEGER,
    claim       INTEGER,
    description TEXT
) AS
$$
SELECT
    cs.case_id,
    cs.name,
    cs.status,
    cs.claim,
    cs.description
FROM cases AS cs
JOIN cases_by_users AS cu
    ON cs.case_id = cu.case_id
    AND cu.user_id = user_id;
$$
LANGUAGE SQL;

CREATE OR REPLACE PROCEDURE link_user_and_case (
    p_user_id     INTEGER,
    p_case_id     INTEGER
) AS
$$
INSERT INTO cases_by_users (case_id, user_id)
VALUES (p_case_id, p_user_id);
$$
LANGUAGE SQL;

CREATE OR REPLACE PROCEDURE unlink_user_and_case (
    p_user_id   INTEGER,
    p_case_id   INTEGER
) AS
$$
DELETE FROM cases_by_users
WHERE user_id = p_user_id
AND case_id = p_case_id;
$$
LANGUAGE SQL;