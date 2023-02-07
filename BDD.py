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

# lit les fichiers tsv depuis l'url et les stockent dans des dataframes
names = pd.read_csv('https://datasets.imdbws.com/name.basics.tsv.gz', compression='gzip', sep='\t', nrows=1000)
title = pd.read_csv('https://datasets.imdbws.com/title.akas.tsv.gz', compression='gzip', sep='\t', nrows=1000)
basics = pd.read_csv('https://datasets.imdbws.com/title.basics.tsv.gz', compression='gzip', sep='\t', nrows=1000)
crew = pd.read_csv('https://datasets.imdbws.com/title.crew.tsv.gz', compression='gzip', sep='\t', nrows=1000)
episode = pd.read_csv('https://datasets.imdbws.com/title.episode.tsv.gz', compression='gzip', sep='\t', nrows=1000)
principals = pd.read_csv('https://datasets.imdbws.com/title.principals.tsv.gz', compression='gzip', sep='\t', nrows=1000)
ratings = pd.read_csv('https://datasets.imdbws.com/title.ratings.tsv.gz', compression='gzip', sep='\t', nrows=1000)

# envoie les dataframes dans la base de données
names.to_sql('names', engine, if_exists='replace')
title.to_sql('title_akas', engine, if_exists='replace')
basics.to_sql('title_basics', engine, if_exists='replace')
crew.to_sql('title_crew', engine, if_exists='replace')
principals.to_sql('title_principals', engine, if_exists='replace')
ratings.to_sql('title_ratings', engine, if_exists='replace')
episode.to_sql('title_episode', engine, if_exists='replace')