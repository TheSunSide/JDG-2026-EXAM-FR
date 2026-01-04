-- ============================================================================
-- SCHÉMA SQL - SOMNIA DATA
-- ============================================================================

DROP DATABASE IF EXISTS  somnia_core;
CREATE DATABASE somnia_core;
USE somnia_core;

DROP TABLE IF EXISTS
    users,
    mattress_type,
    mattress_softness,
    sleeping_position,

    user_sleep_profiles,
    sleep_profiles_transactions_audits,

    intervention_plans,
    intervention_plans_transactions_audits,

    intervention_plan_recommendations,
    intervention_plan_recommendations_transactions_audits;

-- ============================================================================
-- TABLES PRINCIPALES
-- ============================================================================
CREATE TABLE users
(
    id             INT PRIMARY KEY AUTO_INCREMENT,

    first_name     varchar(255) NOT NULL,
    last_name      varchar(255) NOT NULL,

    address_line_1 varchar(255) NOT NULL,
    city           varchar(255) NOT NULL,
    state          varchar(255) NOT NULL,
    postal_code    varchar(15)  NOT NULL,
    country        varchar(255) NOT NULL,
    creation_date  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date    TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE mattress_type
(
    id            INT PRIMARY KEY AUTO_INCREMENT,

    name     varchar(255) NOT NULL,
    description     TEXT,

    creation_date TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date   TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE mattress_softness
(
    id             INT PRIMARY KEY AUTO_INCREMENT,

    softness_level INT       NOT NULL,
    CHECK (softness_level > 0 AND softness_level <= 10),

    creation_date  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date    TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE sleeping_position
(
    id            INT PRIMARY KEY AUTO_INCREMENT,

    name varchar(255) NOT NULL,
    description TEXT,

    creation_date TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date   TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_sleep_profiles
(
    id                   INT PRIMARY KEY AUTO_INCREMENT,

    user_id              INT       NOT NULL,
    mattress_type_id     INT       NOT NULL,
    mattress_softness_id INT       NOT NULL,
    sleeping_position_id INT       NOT NULL,

    night_habit          varchar(255),

    creation_date        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date          TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (mattress_type_id) REFERENCES mattress_type (id),
    FOREIGN KEY (mattress_softness_id) REFERENCES mattress_type (id),
    FOREIGN KEY (sleeping_position_id) REFERENCES sleeping_position (id)
);

CREATE TABLE sleep_profiles_transactions_audits
(
       id                         INT PRIMARY KEY AUTO_INCREMENT,
    transaction_type       ENUM ('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    transaction_desc       TEXT,
    transaction_timestamp  TIMESTAMP                           NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_created_by VARCHAR(255)                        NOT NULL
);

CREATE TABLE intervention_plans
(
    id            INT PRIMARY KEY AUTO_INCREMENT,
    number        INT UNIQUE,
    user_sleep_profile_id INT NOT NULL,
    description   TEXT,
    status       ENUM ('ACTIVE', 'COMPLETED', 'AWAITING') NOT NULL,

    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date   TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (user_sleep_profile_id) REFERENCES user_sleep_profiles (id)

);

CREATE TABLE intervention_plans_transactions_audits
(
       id                         INT PRIMARY KEY AUTO_INCREMENT,
    transaction_type       ENUM ('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    transaction_desc       TEXT,
    transaction_timestamp  TIMESTAMP                           NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_created_by VARCHAR(255)                        NOT NULL
);

CREATE TABLE intervention_plan_recommendations
(
    id                         INT PRIMARY KEY AUTO_INCREMENT,
    intervention_plan_id       INT UNIQUE,
    recommendation_name        varchar(255) NOT NULL,
    recommendation_description TEXT,
    status       ENUM ('ACTIVE', 'COMPLETED', 'AWAITING') NOT NULL,

    creation_date              TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_date                TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (intervention_plan_id) REFERENCES intervention_plans (id)
);

CREATE TABLE intervention_plan_recommendations_transactions_audits
(
    id                         INT PRIMARY KEY AUTO_INCREMENT,
    transaction_type       ENUM ('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    transaction_desc       TEXT,
    transaction_timestamp  TIMESTAMP                           NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_created_by VARCHAR(255)                        NOT NULL
);
