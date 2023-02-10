ALTER TABLE bdd_test.names MODIFY COLUMN birthYear INT NULL; 
ALTER TABLE bdd_test.names MODIFY COLUMN deathYear INT NULL;
ALTER TABLE bdd_test.names MODIFY COLUMN nconst VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.names MODIFY COLUMN primaryName varchar(105) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.names MODIFY COLUMN primaryProfession varchar(66) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.knownForTitles MODIFY COLUMN knownForTitles varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.knownForTitles MODIFY COLUMN nconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_akas MODIFY COLUMN titleId varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_akas MODIFY COLUMN title varchar(656) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_akas MODIFY COLUMN region varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_akas MODIFY COLUMN `language` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_akas MODIFY COLUMN types varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_akas MODIFY COLUMN `attributes` varchar(62) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_basics MODIFY COLUMN tconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_basics MODIFY COLUMN titleType varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_basics MODIFY COLUMN primaryTitle varchar(421) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_basics MODIFY COLUMN originalTitle varchar(421) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_basics MODIFY COLUMN endYear INT NULL;
ALTER TABLE bdd_test.title_basics MODIFY COLUMN runtimeMinutes INT NULL;
ALTER TABLE bdd_test.title_basics MODIFY COLUMN genres varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.directors MODIFY COLUMN tconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.directors MODIFY COLUMN directors varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.writers MODIFY COLUMN tconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.writers MODIFY COLUMN writers varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_episode MODIFY COLUMN tconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_episode MODIFY COLUMN parentTconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_episode MODIFY COLUMN seasonNumber INT NULL;
ALTER TABLE bdd_test.title_episode MODIFY COLUMN episodeNumber INT NULL;
ALTER TABLE bdd_test.title_principals MODIFY COLUMN tconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_principals MODIFY COLUMN nconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_principals MODIFY COLUMN category varchar(19) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_principals MODIFY COLUMN job varchar(290) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_principals MODIFY COLUMN `characters` varchar(1308) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_ratings MODIFY COLUMN tconst varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;
ALTER TABLE bdd_test.title_ratings MODIFY COLUMN averageRating INT NULL;

DELETE FROM bdd_test.directors
WHERE directors IS NULL;

SELECT directors
FROM bdd_test.directors
WHERE directors IS NULL;

ALTER TABLE bdd_test.directors ADD CONSTRAINT directors_pk PRIMARY KEY (tconst,directors);


DELETE FROM bdd_test.knownForTitles
WHERE knownForTitles IS NULL;

SELECT knownForTitles
FROM bdd_test.knownForTitles
WHERE knownForTitles IS NULL;

ALTER TABLE bdd_test.knownfortitles ADD CONSTRAINT knownfortitles_pk PRIMARY KEY (nconst,knownForTitles);

ALTER TABLE bdd_test.names ADD CONSTRAINT names_pk PRIMARY KEY (nconst);

ALTER TABLE bdd_test.title_akas ADD CONSTRAINT title_akas_pk PRIMARY KEY (titleId,`ordering`);

ALTER TABLE bdd_test.title_basics ADD CONSTRAINT title_basics_pk PRIMARY KEY (tconst);

ALTER TABLE bdd_test.title_episode ADD CONSTRAINT title_episode_pk PRIMARY KEY (tconst);

ALTER TABLE bdd_test.title_principals ADD CONSTRAINT title_principals_pk PRIMARY KEY (tconst,`ordering`);

ALTER TABLE bdd_test.title_ratings ADD CONSTRAINT title_ratings_pk PRIMARY KEY (tconst);

ALTER TABLE bdd_test.writers ADD CONSTRAINT writers_pk PRIMARY KEY (tconst);

DELETE FROM bdd_test.writers WHERE writers  IS NULL;

ALTER TABLE bdd_test.writers ADD CONSTRAINT writers_pk PRIMARY KEY (tconst,writers);

ALTER TABLE bdd_test.names ADD CONSTRAINT names_FK FOREIGN KEY (nconst,nconst) REFERENCES bdd_test.title_principals(tconst,`ordering`);



ALTER TABLE bdd_test.title_principals ADD CONSTRAINT title_principals_un UNIQUE KEY (tconst,nconst);

