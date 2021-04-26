DROP DATABASE IF EXISTS MyWine;
CREATE DATABASE MyWine;

USE MyWine;

CREATE TABLE Personne(
   Id_Personne INT AUTO_INCREMENT,
   Nom VARCHAR(50),
   Prénom VARCHAR(45),
   Numéro_téléphone VARCHAR(12),
   Password CHAR(64),
   Pseudo VARCHAR(50) NOT NULL,
   PRIMARY KEY(Id_Personne),
   UNIQUE(Pseudo)
);

CREATE TABLE Administrateur(
   Id_Personne INT,
   PRIMARY KEY(Id_Personne),
   FOREIGN KEY(Id_Personne) REFERENCES Personne(Id_Personne)
);

CREATE TABLE Utilisateur(
   Id_Personne INT,
   PRIMARY KEY(Id_Personne),
   FOREIGN KEY(Id_Personne) REFERENCES Personne(Id_Personne)
);

CREATE TABLE Cave(
   Id_Cave INT AUTO_INCREMENT,
   label VARCHAR(50),
   Id_Personne INT NOT NULL,
   PRIMARY KEY(Id_Cave),
   FOREIGN KEY(Id_Personne) REFERENCES Utilisateur(Id_Personne)
);

CREATE TABLE Vin(
   Id_Vin INT AUTO_INCREMENT,
   Nom VARCHAR(50),
   Type VARCHAR(50),
   Notation VARCHAR(200),
   Echangeable boolean,
   Année INT,
   Quantité INT,
   Id_Cave INT NOT NULL,
   Image LONGTEXT,
   PRIMARY KEY(Id_Vin),
   FOREIGN KEY(Id_Cave) REFERENCES Cave(Id_Cave)
);

CREATE TABLE Echange(
   Id_Echange INT AUTO_INCREMENT,
   accept boolean,
   Id_Vin_Recepteur INT NOT NULL,
   Id_Vin_Emmetteur INT NOT NULL,
   Id_Emmetteur INT NOT NULL,
   Id_Recepteur INT NOT NULL,
   Date_demande DATE NOT NULL,
   Date_reponse DATE,
   PRIMARY KEY(Id_Echange),
   FOREIGN KEY(Id_Vin_Recepteur) REFERENCES Vin(Id_Vin),
   FOREIGN KEY(Id_Vin_Emmetteur) REFERENCES Vin(Id_Vin),
   FOREIGN KEY(Id_Emmetteur) REFERENCES Utilisateur(Id_Personne),
   FOREIGN KEY(Id_Recepteur) REFERENCES Utilisateur(Id_Personne)
);

START TRANSACTION;

INSERT INTO Personne VALUES(null, "Admin", "Admin", "0000000000", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", 'admin');
INSERT INTO Personne VALUES(null, "Guillaume", "SOL", "0611223344", "274c8009224625d893a48ad78481d1130dc31b32c8500b335bfcf73168f6fa54", "guillaume");
INSERT INTO Personne VALUES(null, "Arthur", "LAMBOTTE", "0666666666", "befa156f0283eb0062beb9b86e16a413e1cf8c5135e5518d5c4fa321ce0c7b6b", "arthur");

INSERT INTO Administrateur VALUES(1);


INSERT INTO Utilisateur VALUES(2);
INSERT INTO Utilisateur VALUES(3);


INSERT INTO Cave Values(null, "Maison Principale", 2);
INSERT INTO Cave Values(null, "Maison Secondaire", 2);
INSERT INTO Cave Values(null, "Maison Principale", 3);



INSERT INTO Vin(Id_Vin,Nom,Type,Notation,Echangeable,Année,Quantité,Id_Cave)  VALUES(null, 'Château Mouton Rothschild Pauillac', 'Bordeaux Rouge amer', 'très bon, assez amer', FALSE, 2002, 5, 1);
INSERT INTO Vin(Id_Vin,Nom,Type,Notation,Echangeable,Année,Quantité,Id_Cave)  VALUES(null, 'Château Lafite Rothschild Pauillac', 'Bordeaux Rouge sucré', 'bon vin de table', FALSE, 2012, 1, 1);
INSERT INTO Vin(Id_Vin,Nom,Type,Notation,Echangeable,Année,Quantité,Id_Cave)  VALUES(null, 'Château Margaux', 'Bordeaux Rouge amer', 'moyen, trop amer', FALSE, 2005, 12, 1);
INSERT INTO Vin(Id_Vin,Nom,Type,Notation,Echangeable,Année,Quantité,Id_Cave)  VALUES(null, 'Château Haut-Brion Pessac-Léognan', 'Bordeaux Rouge amer', 'bonne odeur mais bouchoné', FALSE, 2005, 3, 2);
INSERT INTO Vin(Id_Vin,Nom,Type,Notation,Echangeable,Année,Quantité,Id_Cave)  VALUES(null, 'Château Haut-Brion Pessac-Léognan', 'Bordeaux Rouge amer', 'bonne odeur mais bouchoné', FALSE, 2005, 6, 1);
INSERT INTO Vin(Id_Vin,Nom,Type,Notation,Echangeable,Année,Quantité,Id_Cave)  VALUES(null, 'Beauséjour (Duffau Lagarosse), Saint Emilion', 'Bordeaux Rouge', '18/20', FALSE, 2002, 2, 3);
INSERT INTO Vin(Id_Vin,Nom,Type,Notation,Echangeable,Année,Quantité,Id_Cave)  VALUES(null, 'Bastor la Montagne, Sauternes', 'Bordeaux Blanc', '16/20', TRUE, 2012, 8, 3);

CREATE TRIGGER `Ajout_user` AFTER INSERT ON `personne`
 FOR EACH ROW INSERT INTO Cave Values(null, "Maison Principale", NEW.Id_Personne);

COMMIT;


