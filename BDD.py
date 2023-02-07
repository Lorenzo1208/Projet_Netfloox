from sqlalchemy import create_engine
import pandas as pd
import yaml

# ouvre le fichier yaml en mode lecture seule et le charge avec yaml.safe_load
with open('config.yaml', 'r') as file:
# la variable config contient le fichier yaml
    config = yaml.safe_load(file)

# la variable cfg contient la partie mysql du fichier yaml
cfg=config['mysql']
print(cfg)

# création de l'url de connexion à la base de données
url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)
print('URL', url)

#création de la base de données avec l'url et le fichier config.yaml
engine = create_engine(url)

# Permet de lire les fichiers tsv depuis l'url et les stockent dans des dataframes puis envoie les dataframes dans la base de données
def read_and_store_tsv(url, file_name, engine, nrows=1000):
    df = pd.read_csv(url, compression='gzip', sep='\t', nrows=nrows)
    df.to_sql(file_name, engine, if_exists='replace')
# liste des fichiers tsv à télécharger
files = [
    ('https://datasets.imdbws.com/name.basics.tsv.gz', 'names'),
    ('https://datasets.imdbws.com/title.akas.tsv.gz', 'title_akas'),
    ('https://datasets.imdbws.com/title.basics.tsv.gz', 'title_basics'),
    ('https://datasets.imdbws.com/title.crew.tsv.gz', 'title_crew'),
    ('https://datasets.imdbws.com/title.episode.tsv.gz', 'title_episode'),
    ('https://datasets.imdbws.com/title.principals.tsv.gz', 'title_principals'),
    ('https://datasets.imdbws.com/title.ratings.tsv.gz', 'title_ratings'),
]
# boucle pour lire et stocker les fichiers tsv dans la base de données
for url, file_name in files:
    read_and_store_tsv(url, file_name, engine)
