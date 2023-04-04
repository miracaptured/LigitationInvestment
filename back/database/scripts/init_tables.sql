CREATE TABLE IF NOT EXISTS profiles (
    profile_name CHAR(8) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS roles (
    role_name CHAR(8) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS cities (
    city VARCHAR(64) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS case_statuses (
    status_name  VARCHAR(32) PRIMARY KEY
);

CREATE SEQUENCE IF NOT EXISTS user_id_seq START 1;

CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    profile     CHAR(8) REFERENCES profiles(profile_name),
    is_company  BOOLEAN NOT NULL,
    email       VARCHAR(128) UNIQUE NOT NULL,
    name        VARCHAR(128) NOT NULL,
    birthdate   DATE NOT NULL,
    city        VARCHAR(64) REFERENCES cities(city),
    phone       CHAR(16) NOT NULL,
    job         VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS users_passwords (
    user_id     INTEGER UNIQUE NOT NULL,
    user_pswd   VARCHAR(128) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE SEQUENCE IF NOT EXISTS case_id_seq START 1;

CREATE TABLE IF NOT EXISTS cases (
    case_id     INTEGER PRIMARY KEY,
    name        VARCHAR(128) NOT NULL,
    status      VARCHAR(32) REFERENCES case_statuses(status_name),
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
    user_id        INTEGER REFERENCES users(user_id),
    user_role      CHAR(8) REFERENCES roles(role_name),
    PRIMARY KEY (case_id, user_id)
);


INSERT INTO profiles VALUES
('инвестор'), ('фигурант');

INSERT INTO case_statuses VALUES
('на диагностике'), ('отклонено'), ('поиск инвестиций'), ('найдены инвестиции');

INSERT INTO cities VALUES
('Москва');

INSERT INTO roles VALUES
('истец'), ('ответчик'), ('инвестор');


CREATE OR REPLACE FUNCTION get_cases_by_user(user_id    INTEGER)
RETURNS TABLE (
    case_id     INTEGER,
    name        VARCHAR(128),
    status      VARCHAR(32),
    claim       INTEGER,
    description TEXT,
    user_role   CHAR(8)
) AS
$$
SELECT
    cs.case_id,
    cs.name,
    cs.status,
    cs.claim,
    cs.description,
    cu.user_role
FROM cases AS cs
JOIN cases_by_users AS cu
    ON cs.case_id = cu.case_id
    AND cu.user_id = user_id;
$$
LANGUAGE SQL;

CREATE OR REPLACE PROCEDURE link_user_and_case (
    p_user_id     INTEGER,
    p_case_id     INTEGER,
    p_user_role   CHAR(8)
) AS
$$
INSERT INTO cases_by_users (case_id, user_id, user_role)
VALUES (p_case_id, p_user_id, p_user_role);
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

CREATE OR REPLACE FUNCTION user_owns_case (
    p_user_id   INTEGER,
    p_case_id   INTEGER
)
RETURNS BOOLEAN AS
$$
SELECT EXISTS (
    SELECT user_role
    FROM cases_by_users AS cu
    WHERE cu.user_id = p_user_id
    AND cu.case_id = p_case_id
    AND cu.user_role != 'инвестор'
);
$$
LANGUAGE SQL;

CREATE OR REPLACE PROCEDURE link_user_pswd (
    p_user_id   INTEGER,
    p_password  VARCHAR(128)
) AS
$$
INSERT INTO users_passwords (user_id, user_pswd)
VALUES (p_user_id, p_password);
$$
LANGUAGE SQL;
