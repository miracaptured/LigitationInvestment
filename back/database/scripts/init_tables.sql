CREATE TABLE IF NOT EXISTS profiles (
    profile_name CHAR(8) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS roles (
    role_name CHAR(8) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS case_statuses (
    status_name  VARCHAR(32) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS application_statuses (
    status_name VARCHAR(32) PRIMARY KEY
);

CREATE SEQUENCE IF NOT EXISTS user_id_seq START 1;

CREATE TABLE IF NOT EXISTS users (
    user_id     BIGINT PRIMARY KEY,
    profile     CHAR(8) REFERENCES profiles(profile_name),
    is_company  BOOLEAN NOT NULL,
    email       VARCHAR(128) UNIQUE NOT NULL,
    name        VARCHAR(128) NOT NULL,
    birthdate   DATE NOT NULL,
    city        VARCHAR(64),
    phone       CHAR(16) NOT NULL,
    job         VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS users_passwords (
    user_id     BIGINT UNIQUE NOT NULL,
    user_pswd   VARCHAR(128) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE SEQUENCE IF NOT EXISTS application_id_seq START 1;

CREATE TABLE IF NOT EXISTS applications (
    application_id  BIGINT PRIMARY KEY,
    initiator_id    BIGINT REFERENCES users(user_id),
    name            VARCHAR(128) NOT NULL,
    status          VARCHAR(32) REFERENCES application_statuses(status_name),
    claim           BIGINT NOT NULL,
    initiator_role  VARCHAR(8) REFERENCES roles(role_name),
    description     TEXT
);

CREATE SEQUENCE IF NOT EXISTS case_id_seq START 1;

CREATE TABLE IF NOT EXISTS cases (
    case_id         BIGINT PRIMARY KEY,
    initiator_id    BIGINT REFERENCES users(user_id),
    name            VARCHAR(128) NOT NULL,
    status          VARCHAR(32) REFERENCES case_statuses(status_name),
    claim           BIGINT NOT NULL,
    initiator_role  VARCHAR(8) REFERENCES roles(role_name),
    description     TEXT
);

CREATE SEQUENCE IF NOT EXISTS doc_id_seq START 1;

CREATE TABLE IF NOT EXISTS documents (
    doc_id      BIGINT PRIMARY KEY,
    case_id     BIGINT REFERENCES cases(case_id),
    name        VARCHAR(128) NOT NULL,
    link        TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS applications_by_users (
    application_id  BIGINT REFERENCES applications(application_id),
    user_id         BIGINT REFERENCES users(user_id),
    user_role       CHAR(8) REFERENCES roles(role_name),
    PRIMARY KEY (application_id, user_id)
);

CREATE TABLE IF NOT EXISTS cases_by_users (
    case_id        BIGINT REFERENCES cases(case_id),
    user_id        BIGINT REFERENCES users(user_id),
    user_role      CHAR(8) REFERENCES roles(role_name),
    investment     BIGINT,
    PRIMARY KEY (case_id, user_id)
);


INSERT INTO profiles VALUES
('инвестор'), ('фигурант');

INSERT INTO application_statuses VALUES
('на рассмотрении'), ('отклонено'), ('принято');

INSERT INTO case_statuses VALUES
('на диагностике'), ('поиск инвестиций'), ('найдены инвестиции'), ('закрыто');

INSERT INTO roles VALUES
('истец'), ('ответчик'), ('инвестор');

CREATE OR REPLACE FUNCTION get_applications_by_user(p_user_id BIGINT)
RETURNS TABLE (
    application_id BIGINT,
    name           VARCHAR(128),
    status         VARCHAR(32),
    claim          BIGINT,
    description    TEXT,
    user_role      CHAR(8)
) AS
$$
SELECT
    ap.application_id,
    ap.name,
    ap.status,
    ap.claim,
    ap.description,
    au.user_role
FROM applications AS ap
JOIN applications_by_users AS au
    ON ap.application_id = au.application_id
WHERE au.user_id = p_user_id;
$$
LANGUAGE SQL;

CREATE OR REPLACE FUNCTION get_cases_by_user(p_user_id    BIGINT)
RETURNS TABLE (
    case_id     BIGINT,
    name        VARCHAR(128),
    status      VARCHAR(32),
    claim       BIGINT,
    description TEXT,
    user_role   CHAR(8),
    investment  BIGINT
) AS
$$
SELECT DISTINCT
    cs.case_id,
    cs.name,
    cs.status,
    cs.claim,
    cs.description,
    cu.user_role,
    cu.investment
FROM cases AS cs
JOIN cases_by_users AS cu
    ON cs.case_id = cu.case_id
WHERE cu.user_id = p_user_id;
$$
LANGUAGE SQL;

CREATE OR REPLACE PROCEDURE link_user_and_case (
    p_user_id     BIGINT,
    p_case_id     BIGINT,
    p_user_role   CHAR(8),
    p_investment  BIGINT
) AS
$$
BEGIN
IF EXISTS(
    SELECT investment
    FROM cases_by_users AS cu
    WHERE cu.user_id = p_user_id
    AND cu.case_id = p_case_id
    ) THEN
        UPDATE cases_by_users
        SET investment = investment + p_investment
        WHERE case_id = p_case_id
        AND user_id = p_user_id;
    ELSE
        INSERT INTO cases_by_users (case_id, user_id, user_role, investment)
        VALUES (p_case_id, p_user_id, p_user_role, p_investment);
END IF;
END;
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE PROCEDURE unlink_user_and_case (
    p_user_id   BIGINT,
    p_case_id   BIGINT
) AS
$$
DELETE FROM cases_by_users
WHERE user_id = p_user_id
AND case_id = p_case_id;
$$
LANGUAGE SQL;

CREATE OR REPLACE FUNCTION user_owns_case (
    p_user_id   BIGINT,
    p_case_id   BIGINT
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
    p_user_id   BIGINT,
    p_password  VARCHAR(128)
) AS
$$
INSERT INTO users_passwords (user_id, user_pswd)
VALUES (p_user_id, p_password);
$$
LANGUAGE SQL;

CREATE OR REPLACE FUNCTION check_pswd (
    p_user_email    VARCHAR(128),
    p_password      VARCHAR(128)
)
RETURNS BOOLEAN AS
$$
SELECT
    CASE
        WHEN up.user_pswd = p_password THEN TRUE
        ELSE FALSE
    END
FROM users_passwords AS up
JOIN users AS us
    ON us.user_id = up.user_id
WHERE us.email = p_user_email;
$$
LANGUAGE SQL;

CREATE OR REPLACE FUNCTION get_investments_by_case (
    p_case_id   BIGINT
)
RETURNS BIGINT AS
$$
SELECT
    CASE WHEN SUM(cu.investment) IS NULL
    THEN 0
    ELSE SUM(cu.investment) END AS summ
    FROM cases_by_users AS cu
    WHERE cu.case_id = p_case_id
    GROUP BY cu.case_id, cu.user_role
    HAVING cu.user_role = 'инвестор';
$$
LANGUAGE SQL;


-- example data
INSERT INTO users VALUES
(1, 'фигурант', FALSE, 'figurant1@email.com', 'Иванов Иван Иванович', '2002-07-10', 'Москва', '+11111111111', 'ООО Рога и Копыта'),
(2, 'инвестор', TRUE, 'investor1@email.com', 'Дмитриев Дмитрий Дмитриевич', '2003-02-03', 'Самара', '+00000000000', 'АО Предприятие'),
(3, 'фигурант', TRUE, 'figurant2@email.com', 'Антонова Антонина Антоновна', '2000-01-01', 'Москва', '+22222222222', 'ПАО Некий Банк'),
(4, 'инвестор', FALSE, 'investor2@email.com', 'Михайлов Михаил Михаилович', '1999-12-31', 'Калининград', '+33333333333', 'ИП Михайлов М. М.'),
(5, 'фигурант', TRUE, 'figurant3@email.com', 'Алексеев Алексей Алексеевич', '1989-01-01', 'Санкт-Петербург', '+44444444444', 'ООО Алексеев и Co.'),
(6, 'фигурант', TRUE, 'figurant4@email.com', 'Романов Роман Романович', '1993-10-03', 'Иркутск', '+55555555555', 'АО Тепло и Снабжение'),
(7, 'фигурант', TRUE, 'figurant5@email.com', 'Александрова Александра Александровна', '1998-08-23', 'Сочи', '+66666666666', 'ООО Бнал'),
(8, 'фигурант', FALSE, 'figurant6@email.com', 'Борисов Борис Борисович', '1961-04-12', 'Владимир', '+77777777777', 'ООО Паньки');

INSERT INTO users_passwords VALUES
(1, '123'),
(2, '123'),
(3, '123'),
(4, '123'),
(5, '123'),
(6, '123'),
(7, '123'),
(8, '123');

INSERT INTO applications VALUES
(1, 1, 'Кредитная организация vs Заемщики', 'принято', 990000000, 'истец', 'Иск о взыскании денежных средств по кредитным договорам.'),
(2, 3, 'Завод (РФ) vs Поставщик (КНР)', 'принято', 469000000, 'истец', 'Иск о взыскании убытков.'),
(3, 1, 'Подрядчик (РФ) vs Заказчик (Нидерланды)', 'отклонено', 1800000000, 'истец', 'Иск о взыскании убытков.'),
(4, 3, 'Производитель (РФ) vs Поставщик (UK)', 'на рассмотрении', 70000000, 'истец', 'Иск о взыскании суммы уплаченных денежных средств за товар ненадлежащего качества и возмещении убытков'),
(5, 5, 'Владелец бренда vs Юридические лица', 'принято', 10000000, 'истец', 'Дело о незаконном использовании товарного знака'),
(6, 5, 'Нарушение положений акционерного соглашения в отношении реализации прав на опцион', 'принято', 203000000, 'истец', 'Иск о взыскании убытков'),
(7, 6, 'Теплоснабжающая организация vs Субъект РФ как публично-правовое образование', 'принято', 76900000, 'истец', 'Взыскание убытков, вызванных утверждением для истца экономически необоснованного тарифа'),
(8, 6, 'Теплоснабжающая организация vs Тепломагистральная компания', 'на рассмотрении', 68000000, 'истец', 'Дело о взыскании задолженности по оплате коммунальных услуг'),
(9, 6, 'Теплоснабжающая организация vs Теплосетевая компания', 'принято', 64000000, 'истец', 'Дело о взыскании задолженности по оплате тепловой энергии и процентов за пользование чужими денежными средствами'),
(10, 7, 'Кредитор vs Крупный ресторанный холдинг', 'принято', 420000000, 'истец', 'Дело о взыскании денежных средств'),
(11, 7, 'Юридическое лицо РФ vs физические лица РФ', 'принято', 70000000, 'истец', 'Дело о взыскании денежных средств по кредитным договорам'),
(12, 8, 'Физическое лицо РФ vs Частная клиника', 'принято', 50000000, 'истец', 'Дело о взыскании денежных средств'),
(13, 8, 'Физическое лицо vs Юридическое лицо/контролирующие должника лица', 'принято', 4200000000, 'ответчик', 'Дело о взыскании денежных средств');

INSERT INTO cases VALUES
(1, 1, 'Кредитная организация vs заемщики', 'поиск инвестиций', 990000000, 'истец', 'Иск о взыскании денежных средств по кредитным договорам.'),
(2, 3, 'ЗАВОД РФ vs поставщик', 'на диагностике', 469000000, 'истец', 'Иск о взыскании убытков.'),
(3, 5, 'Владелец бренда vs Юридические лица', 'поиск инвестиций', 10000000, 'истец', 'Дело о незаконном использовании товарного знака'),
(4, 5, 'Нарушение положений акционерного соглашения в отношении реализации прав на опцион', 'закрыто', 203000000, 'истец', 'Место рассмотрения спора - Нью-Йорк. Инвестор - физ. лицо, гражданин РФ. Дело завершилось взысканием неустойки в пользу истца. Инвестор заработал 150%'),
(5, 6, 'Теплоснабжающая организация vs Субъект РФ как публично-правовое образование', 'поиск инвестиций', 76900000, 'истец', 'Взыскание убытков, вызванных утверждением для истца экономически необоснованного тарифа'),
(6, 6, 'Теплоснабжающая организация vs Теплосетевая компания', 'поиск инвестиций', 64000000, 'истец', 'Дело о взыскании задолженности по оплате тепловой энергии и процентов за пользование чужими денежными средствами'),
(7, 7, 'Кредитор vs Крупный ресторанный холдинг', 'поиск инвестиций', 420000000, 'истец', 'Дело о взыскании денежных средств'),
(8, 7, 'Юридическое лицо РФ vs физические лица РФ', 'поиск инвестиций', 50000000, 'истец', 'Дело о взыскании денежных средств по кредитным договорам'),
(9, 8, 'Физическое лицо РФ vs Частная клиника', 'поиск инвестиций', 50000000, 'истец', 'Дело о взыскании денежных средств'),
(10, 8, 'Физическое лицо vs Юридическое лицо/контролирующие должника лица', 'поиск инвестиций', 4200000000, 'ответчик', 'Дело о взыскании денежных средств');

INSERT INTO cases_by_users VALUES
(1, 1, 'истец', 0),
(5, 4, 'истец', 0),
(2, 3, 'истец', 0),
(3, 5, 'истец', 0),
(4, 5, 'истец', 0),
(5, 6, 'истец', 0),
(6, 6, 'истец', 0),
(7, 7, 'истец', 0),
(8, 7, 'истец', 0),
(9, 8, 'истец', 0),
(10, 8, 'ответчик', 0);
