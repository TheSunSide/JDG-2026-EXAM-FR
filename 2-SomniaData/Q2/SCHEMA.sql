-- ============================================================================
-- SCHÉMA SQL - SOMNIA DATA
-- ============================================================================

-- Création de la base de données
-- TODO

-- ============================================================================
-- TABLES PRINCIPALES
-- ============================================================================

-- Création des tables
-- TODO

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    address_line_1 varchar(255) NOT NULL,
    city varchar(255) NOT NULL,
    state varchar(255) NOT NULL,
    postal_code varchar(15) NOT NULL,
    country varchar(255) NOT NULL
);

CREATE TABLE mattress_type (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_name varchar(255) NOT NULL,
    type_desc TEXT
);

CREATE TABLE mattress_softness (
    id INT PRIMARY KEY AUTO_INCREMENT,
    softness_level INT NOT NULL,
    CHECK(softness_level>0 AND softness_level<=10)
);

CREATE TABLE sleeping_position (
    id INT PRIMARY KEY AUTO_INCREMENT,
    position_name varchar(255) NOT NULL,
    position_desc TEXT
);


CREATE TABLE user_sleep_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    mattress_type_id INT NOT NULL,
    mattress_softness_id INT NOT NULL,
    sleeping_position_id INT NOT NULL,

    night_habit varchar(255),

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (mattress_type_id) REFERENCES mattress_type(id),
    FOREIGN KEY (mattress_softness_id) REFERENCES mattress_type(id),
    FOREIGN KEY (sleeping_position_id) REFERENCES sleeping_position(id)

);

CREATE TABLE intervention_plan_status (
  id INT PRIMARY KEY AUTO_INCREMENT,
  status_name varchar(255) NOT NULL,
  status_desc TEXT
);

CREATE TABLE intervention_plans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    number INT UNIQUE,
    description TEXT,
    status_id INT NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (status_id) REFERENCES intervention_plan_status(id)

);

CREATE TABLE intervention_plan_recommendations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    intervention_plan_id INT UNIQUE,
    recommendation_name varchar(255) NOT NULL,
    recommendation_description TEXT,
    FOREIGN KEY (intervention_plan_id) REFERENCES intervention_plans(id)
);

