# Projet_Netfloox
# Trello https://trello.com/invite/b/t30wOKVq/ATTI6a5db96a0e6037e53f916002fb10729dE46C7D33/projet-netfloox
# Diapo https://docs.google.com/presentation/d/1_EoeHIMV8HF1E5UTIEvuz9Iu-HZVaBbgyljHkBkBvPw/edit?usp=sharing

## Le dossier Netfloox contient toute la partie Django.

## Il y a beaucoup de CSV qui sont des extraits de la base de données.

## bdd_load.py est le script python qui nous as permis d'envoyer toutes les données des fichiers d'iMDB sur la machine virtuelle Azure dans une base de données.

## Script_all.sql permet de créer toute les clés primaires et de mettre les bons types dans la base de données.

## cosine_similarity.py nous permet avec l'input d'un film de ressortir 5 films les plus similaires. Il s'appuie sur le CSV cosine_features_no_date.csv qui contient l'ensemble des films et des features importantes.

## features.py nous permet de créer des CSV qui contiennent les éléments qui nous intéressent. On extrait les données avec une requête SQL sur la machine virtuelle qui contient la base de données.

## model.py permet d'entrainer différents modèles comme KNN ou randomForest, le tout dans un pipeline avec GridSearchCV et RandomizedSearchCV pour rechercher les meilleurs hyperparamètres. À la fin, une fonction enregistre le meilleur modèle avec les meilleurs hyperparamètres et une autre fonction permet de charger ce modèle et de le tester avec des inputs de test.

## query.py permet de faire des requêtes simples en SQL sur la VM.
