CREATE DATABASE IF NOT EXISTS autochess;
CREATE TABLE IF NOT EXISTS autochess.board(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), spot INT, bonus INT);
CREATE TABLE IF NOT EXISTS autochess.heroes(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), health INT, money INT, level INT);
CREATE TABLE IF NOT EXISTS autochess.user(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, bool_ia boolean);
CREATE TABLE IF NOT EXISTS autochess.champions(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), health INT, attack INT, price INT, description VARCHAR(255), rarity INT, level INT);
INSERT INTO autochess.champions VALUES(1,"salameche", 50, 5, 1, "Pokemon de type feu", 1, 1)
INSERT INTO autochess.champions VALUES(2,"hericendre", 50, 5, 1, "Pokemon de type feu", 1, 1)
INSERT INTO autochess.champions VALUES(3,"carapuce", 50, 5, 1, "Pokemon de type eau", 1, 1)
INSERT INTO autochess.champions VALUES(4,"kaiminus", 50, 5, 1, "Pokemon de type eau", 1, 1)
INSERT INTO autochess.champions VALUES(5,"bulbizar", 50, 5, 1, "Pokemon de type plante", 1, 1)
INSERT INTO autochess.champions VALUES(6,"germinion", 50, 5, 1, "Pokemon de type plante", 1, 1)
INSERT INTO autochess.champions VALUES(7,"mini_draco", 50, 5, 1, "Pokemon de type dragon", 1, 1)
INSERT INTO autochess.champions VALUES(8,"chetiflor", 50, 5, 1, "Pokemon de type plante", 1, 1)
INSERT INTO autochess.champions VALUES(9,"mystherbe", 50, 5, 1, "Pokemon de type plante", 1, 1)
INSERT INTO autochess.champions VALUES(10,"wattwatt", 50, 5, 1, "Pokemon de type electrique", 1, 1)
INSERT INTO autochess.champions VALUES(11,"miaous", 50, 5, 1, "Pokemon de type normal", 1, 1)
INSERT INTO autochess.champions VALUES(12,"evoli", 50, 5, 1, "Pokemon de type normal", 1, 1)
INSERT INTO autochess.champions VALUES(13,"pyroli", 75, 10, 2, "Pokemon de type feu", 2, 1)
INSERT INTO autochess.champions VALUES(14,"voltali", 75, 10, 2, "Pokemon de type electrique", 2, 1)
INSERT INTO autochess.champions VALUES(15,"aquali", 75, 10, 2, "Pokemon de type eau", 2, 1)
INSERT INTO autochess.champions VALUES(16,"mentali", 75, 10, 1, "Pokemon de type psy", 1, 1)
INSERT INTO autochess.champions VALUES(17,"noctalie", 75, 10, 1, "Pokemon de type tenebre", 1, 1)
CREATE TABLE IF NOT EXISTS autochess.type(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), number INT, bonus_percent INT, modified_stats VARCHAR(255));
INSERT INTO autochess.type VALUES(1, "feu", 3, 10, "attack")
INSERT INTO autochess.type VALUES(2, "eau", 3, 25, "health")
INSERT INTO autochess.type VALUES(3, "plante", 2, 7, "attack, health")
INSERT INTO autochess.type VALUES(4, "electrique", 2, 20, "attack")
INSERT INTO autochess.type VALUES(5, "normal", 2, 15, "attack")
INSERT INTO autochess.type VALUES(6, "psy", 1, 30, "attack")
INSERT INTO autochess.type VALUES(7, "ténebre", 1, 30, "attack")