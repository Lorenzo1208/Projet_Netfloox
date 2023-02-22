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

def load_csv():
    df = pd.read_csv('data_movie_2000.csv')
    unique_tconst = df['tconst'].nunique()
    print(f" {unique_tconst} : Films")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
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
                Limit 1000000;
                """)
    
    #634638 movies
    query5 = text("""SELECT COUNT(*) FROM title_basics WHERE titleType = 'movie';""")
    
    query6 = text("""SELECT t1.nconst, t1.tconst, t1.category,
                t3.writers, t3.directors, t4.nconst, t4.knownForTitles,
                
                FROM title_principals AS t1
                INNER JOIN title_crew AS t3
                
                ON t1.tconst = t3.tconst
                INNER JOIN title_basics AS t2
                
                ON t1.tconst = t2.tconst
                INNER JOIN name_basics AS t4
                
                ON t1.tconst = t4.tconst
                WHERE t2.startYear > 2000
                LIMIT 50;""")

    query7 = text("""SELECT tb.primaryTitle, tr.averageRating
                    FROM title_basics tb
                    JOIN title_ratings tr ON tb.tconst = tr.tconst
                    WHERE tb.titleType = 'movie' AND tb.startYear = 2021 AND tr.numVotes > 100000
                    ORDER BY tr.averageRating DESC
                    LIMIT 10;
                    """)
    
    query8 = text("""DESCRIBE SELECT COUNT(*) FROM title_basics WHERE titleType = 'movie' AND startYear = 2022;""")
    
    query9 = text("""DESCRIBE SELECT names.primaryName, COUNT(*) AS num_films
                    FROM title_principals
                    JOIN names ON title_principals.nconst = names.nconst
                    WHERE title_principals.category = 'actor'
                    GROUP BY title_principals.nconst
                    ORDER BY num_films DESC
                    LIMIT 10;""")
    
    query10 = text("""SELECT titleType, COUNT(*) as count
                        FROM title_basics
                        GROUP BY titleType;""")
    
    query11 = text("""SELECT COUNT(*) as count
FROM title_basics;""")

    #def concat_features(row):
    #    return row['genres'].replace(',','') + ' ' + row['directors'].replace(' ','')
    # df['features'] = df.apply(concat_features, axis=1)
    
    df = get_data(engine, query11)
    # df_movies = df[df['titleType'] == 'movie']
    # regrouper par tconst et sélectionner la première valeur non-nulle de writers et directors
    # df_grouped = df.groupby('tconst').agg({'knownForTitles': lambda x: next((i for i in x if i is not None), None),
    #                                     'directors': lambda x: next((i for i in x if i is not None), None)})

    # # renommer les colonnes
    # df_grouped = df_grouped.rename(columns={'writers': 'writers1', 'directors': 'directors1'})
    print(df.head(10))
    # df2 = get_data(engine, query3)
    # plot_data(df)

    # print the resulting dataframe
    # print(df.head(10))
    # print(df.columns)
    # df.to_csv('data_movie_2000.csv')
    # print(df2.head(10))
    # load_csv()
    
    # # pivot the table to create new columns for each category and the corresponding nconst values
    # df_pivoted = df.pivot_table(index='tconst', columns='category', values='nconst', aggfunc='first')

    # # reset the index to keep tconst as a regular column
    # df_pivoted = df_pivoted.reset_index()

    # # add a prefix to the column names to indicate the category
    # df_pivoted = df_pivoted.add_prefix('category_')

    # # rename the 'tconst' column to match the original DataFrame
    # df_pivoted = df_pivoted.rename(columns={'category_tconst': 'tconst'})
    
    # print(df_pivoted.head(20))
    # df_pivoted.to_csv('data_pivoted.csv')
    
if __name__ == '__main__':
    main()
