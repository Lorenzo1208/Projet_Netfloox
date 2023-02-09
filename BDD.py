from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy
import yaml
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# ouvre le fichier yaml en mode lecture seule et le charge avec yaml.safe_load
with open('config.yaml', 'r') as file:
# la variable config contient le fichier yaml
    config = yaml.safe_load(file)

# la variable cfg contient la partie mysql du fichier yaml
cfg=config['mysql-datalab']
print(cfg)

# création de l'url de connexion à la base de données
url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)
print('URL', url)

#création de la base de données avec l'url et le fichier config.yaml
engine = create_engine(url)

def split_et_explode(x):
    return x.split(",") if x else None

def read_and_store_tsv(url, file_name, engine, nrows=1000, chunksize=1000):
    chunks = pd.read_csv(url, compression='gzip', sep='\t', nrows=nrows, chunksize=chunksize, low_memory=False)
    for chunk in chunks:
        chunk = chunk.applymap(lambda x: None if x == r'\N' else x)
        if file_name == "title_crew":
            if "writers" in chunk.columns:
                writers_df = chunk[['tconst', 'writers']]
                writers_df["writers"] = chunk["writers"].apply(split_et_explode)
                writers_df = writers_df.explode("writers")
                writers_df.to_sql("writers", engine, if_exists='replace', index=False)
            if "directors" in chunk.columns:
                directors_df = chunk[['tconst', 'directors']]
                directors_df["directors"] = chunk["directors"].apply(split_et_explode)
                directors_df = directors_df.explode("directors")
                directors_df.to_sql("directors", engine, if_exists='replace', index=False)
        else:
            chunk.to_sql(file_name, engine, if_exists='replace', index=False)


# liste des fichiers tsv à télécharger
files = [
    ('name.basics.tsv.gz', 'names'),
    ('title.basics.tsv.gz', 'title_basics'),
    ('title.principals.tsv.gz', 'title_principals'),
    ('title.ratings.tsv.gz', 'title_ratings'),
    ('title.episode.tsv.gz', 'title_episode'),
    ('title.crew.tsv.gz', 'title_crew'),
    ('title.akas.tsv.gz', 'title_akas')
    # ('https://datasets.imdbws.com/title.akas.tsv.gz', 'title_akas'),
    # ('https://datasets.imdbws.com/title.basics.tsv.gz', 'title_basics'),
    # ('https://datasets.imdbws.com/title.crew.tsv.gz', 'title_crew'),
    # ('https://datasets.imdbws.com/title.episode.tsv.gz', 'title_episode'),
    # ('https://datasets.imdbws.com/title.principals.tsv.gz', 'title_principals'),
    # ('https://datasets.imdbws.com/title.ratings.tsv.gz', 'title_ratings'),
]
# boucle pour lire et stocker les fichiers tsv dans la base de données
for url, file_name in files:
    read_and_store_tsv(url, file_name, engine)
