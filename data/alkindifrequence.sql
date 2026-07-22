CREATE DATABASE alkindifrequence;

CREATE TABLE lettres_lower (
    lettre CHAR(1) PRIMARY KEY,
    frequence DOUBLE PRECISION DEFAULT 0
);

CREATE TABLE lettres_upper (
    lettre CHAR(1) PRIMARY KEY,
    frequence DOUBLE PRECISION DEFAULT 0
);

CREATE TABLE nombres (
    chiffre CHAR(1) PRIMARY KEY,
    frequence DOUBLE PRECISION DEFAULT 0
);