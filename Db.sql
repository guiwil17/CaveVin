DROP DATABASE IF EXISTS MyWine;
CREATE DATABASE MyWine;

USE MyWine;
ALTER DATABASE MyWine charset=utf8;

CREATE TABLE Personne(
   Id_Personne INT AUTO_INCREMENT,
   Nom VARCHAR(50),
   Prenom VARCHAR(45),
   Numero_telephone VARCHAR(12),
   Password CHAR(64),
   Pseudo VARCHAR(50) NOT NULL,
   PRIMARY KEY(Id_Personne),
   UNIQUE(Pseudo)
);

CREATE TABLE Administrateur(
   Id_Personne INT,
   PRIMARY KEY(Id_Personne),
   CONSTRAINT `FK_Admin_Personne`
        FOREIGN KEY (Id_Personne) REFERENCES Personne(Id_Personne)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE Utilisateur(
   Id_Personne INT,
   PRIMARY KEY(Id_Personne),
   CONSTRAINT `FK_User_Personne`
        FOREIGN KEY(Id_Personne) REFERENCES Personne(Id_Personne)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE Cave(
   Id_Cave INT AUTO_INCREMENT,
   label VARCHAR(50),
   Id_Personne INT NOT NULL,
   PRIMARY KEY(Id_Cave),
   CONSTRAINT `FK_Cave_Personne_`
        FOREIGN KEY(Id_Personne) REFERENCES Utilisateur(Id_Personne)
        ON DELETE CASCADE
        ON UPDATE NO ACTION
);

CREATE TABLE Vin(
   Id_Vin INT AUTO_INCREMENT,
   Nom VARCHAR(50),
   Type VARCHAR(50),
   Notation VARCHAR(200),
   Echangeable boolean,
   Annee INT,
   Quantite INT,
   Id_Cave INT NOT NULL,
   Image LONGTEXT,
   PRIMARY KEY(Id_Vin),
   CONSTRAINT FOREIGN KEY(Id_Cave) REFERENCES Cave(Id_Cave) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Echange(
   Id_Echange INT AUTO_INCREMENT,
   accept boolean NOT NULL,
   Id_Vin_Recepteur INT NOT NULL,
   Id_Vin_Emmetteur INT NOT NULL,
   Id_Emmetteur INT NOT NULL,
   Id_Recepteur INT NOT NULL,
   Date_demande DATE NOT NULL,
   Date_reponse DATE,
   reponse boolean NOT NULL,
   PRIMARY KEY(Id_Echange),
   CONSTRAINT FOREIGN KEY(Id_Vin_Recepteur) REFERENCES Vin(Id_Vin)ON DELETE CASCADE ON UPDATE CASCADE,
   CONSTRAINT FOREIGN KEY(Id_Vin_Emmetteur) REFERENCES Vin(Id_Vin) ON DELETE CASCADE ON UPDATE CASCADE,
   CONSTRAINT FOREIGN KEY(Id_Emmetteur) REFERENCES Utilisateur(Id_Personne) ON DELETE CASCADE ON UPDATE CASCADE,
   CONSTRAINT FOREIGN KEY(Id_Recepteur) REFERENCES Utilisateur(Id_Personne) ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO Personne VALUES(null, "Admin", "Admin", "0000000000", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", 'admin');


INSERT INTO Administrateur VALUES(1);

CREATE TRIGGER `Ajout_user` AFTER INSERT ON `Personne`
 FOR EACH ROW INSERT INTO Cave Values(null, "Maison Principale", NEW.Id_Personne);

CREATE TRIGGER `Ajout_utilisateur` AFTER INSERT ON `Personne`
 FOR EACH ROW INSERT INTO Utilisateur Values(NEW.Id_Personne);

INSERT INTO Personne VALUES(null, "Guillaume", "SOL", "0611223344", "274c8009224625d893a48ad78481d1130dc31b32c8500b335bfcf73168f6fa54", "guillaume");
INSERT INTO Personne VALUES(null, "Arthur", "LAMBOTTE", "0666666666", "befa156f0283eb0062beb9b86e16a413e1cf8c5135e5518d5c4fa321ce0c7b6b", "arthur");
INSERT INTO Personne VALUES(null, "Tim", "HAGINE", "0653232523", "aac09a648fc382b6f78897595486e691d00de9dfc742f3ba1930464b56eecda6", "Tim");
INSERT INTO Personne VALUES(null, "Jean", "REGISTRE", "0612142523", "56ec4fee9f20de343a99f2caa8793dadb6c8fbeebeed0f124e397d660112245c", "Jean");
INSERT INTO Personne VALUES(null, "Guy", "TAR", "0612142523", "55fb96bf33f19ca574d9616fd4bdeb4ed4840a2120aa63824e436bb35ca3176f", "Guy");
INSERT INTO Personne VALUES(null, "Olivier", "Flauzac", "0000000000", "c9d218a13c03291e89f9e8852e28025eec28f944af4d321c2bf98d29fee92328", "flauzac");

INSERT INTO Utilisateur VALUES(1);
INSERT INTO Utilisateur VALUES(2);



