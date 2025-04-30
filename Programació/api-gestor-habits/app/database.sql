CREATE DATABASE GESTOR_TASQUES;
USE GESTOR_TASQUES;

CREATE TABLE usuaris (
    id_usuari INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50),
    llinatges VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    sexe ENUM('home', 'dona', 'altre'),
    contrasenya VARCHAR(255), -- encriptada!
    telefon VARCHAR(20),
    altura DECIMAL(5,2), -- en cm (p. ex. 175.50)
    pes DECIMAL(5,2), -- en kg (p. ex. 70.25)
    imc DECIMAL(5,2) -- (calculat com pes / (altura/100)^2)
);

CREATE TABLE tasques (
    id_tasca INT PRIMARY KEY AUTO_INCREMENT,
    id_usuari INT,
    data_objectiu DATE,
    titol VARCHAR(100),
    descripcio TEXT,
    estat ENUM('pendent', 'completat'),
    FOREIGN KEY (id_usuari) REFERENCES usuaris(id_usuari) ON DELETE CASCADE
);