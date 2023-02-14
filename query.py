import yaml
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

def get_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

def create_engine_from_config(config):
    cfg = config['mysql2']
    return create_engine("{driver}://{user}:{password}@{host}/{database}".format(**cfg))

def get_data(engine, query):
    with engine.connect() as conn:
        df = conn.execute(query)
        df = pd.DataFrame(df.fetchall())
        df.columns = df.columns = df.keys()
    return df

def plot_data(df):
    plt.figure(figsize=(20,10))
    sns.barplot(data=df, x="birthYear", y="N")
    plt.xlabel("Birth Year")
    plt.ylabel("Count")
    plt.title("Count of Names by Birth Year")
    plt.show()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
def main():
    
    config = get_config()
    engine = create_engine_from_config(config)
    
    query = text("""SELECT tconst, writers
                    FROM bdd.writers
                    WHERE writers = 'None' LIMIT 10;""")
    
    query2 = text("""SELECT birthYear, count(*) AS N FROM names GROUP BY birthYear;""")
    
    query3 = text("""SELECT tconst, writers
                    FROM bdd.writers
                    WHERE tconst IS NOT NULL AND writers IS NULL;
                    """)
    
    query4 = text("""SELECT title_ratings.tconst, title_ratings.averageRating, title_ratings.numVotes,
                 title_principals.tconst, title_principals.nconst, title_principals.category,
                 title_basics.titleType, title_basics.isAdult, title_basics.startYear, title_basics.runtimeMinutes, title_basics.genres,
                 title_akas.title, title_akas.titleId,
                 names.primaryName, names.primaryProfession, names.nconst,
                 directors.directors, directors.tconst,
                 writers.writers, writers.tconst
                 
                 FROM title_basics
                 
                 INNER JOIN title_ratings
                 ON title_basics.tconst = title_ratings.tconst
                 
                 INNER JOIN title_principals
                 ON title_basics.tconst = title_principals.tconst
                 
                 INNER JOIN title_akas
                 ON title_basics.tconst = title_akas.titleId
                 
                 INNER JOIN names
                 ON title_principals.nconst = names.nconst
                 
                 INNER JOIN directors
                 ON title_basics.tconst = directors.tconst
                 
                 INNER JOIN writers
                 ON title_basics.tconst = writers.tconst 
                 
                 WHERE title_basics.titleType = 'movie' AND title_basics.startYear > 2000
                
                 ;
                    """)
    
    #634638 movies
    query5 = text("""SELECT COUNT(*) FROM title_basics WHERE titleType = 'movie';""")

    df = get_data(engine, query4)
    # df_movies = df[df['titleType'] == 'movie']

    # df2 = get_data(engine, query3)
    # plot_data(df)
    
    print(df.head(10))
    print(df.columns)
    df.to_csv('data.csv')
    # print(df2.head(10))
    
if __name__ == '__main__':
    main()
