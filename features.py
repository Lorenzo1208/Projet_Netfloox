import yaml
import pandas as pd
from sqlalchemy import create_engine, text
import time

def read_config():
    with open("config.yaml", 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return config['mysql2']

def connect_to_database(config):
    engine = create_engine("{driver}://{user}:{password}@{host}/{database}".format(**config))
    conn = engine.connect()
    return conn

def get_data(conn):
    query = text('''SELECT tb.tconst, tb.genres, tp.nconst, tp.category, tb.runtimeMinutes, tb.startYear, tb.originalTitle, tr.averageRating, tp.nconst, n.nconst, n.primaryName
                    FROM title_basics tb
                    LEFT JOIN title_principals tp ON tb.tconst = tp.tconst
                    LEFT JOIN title_ratings tr ON tb.tconst = tr.tconst
                    LEFT JOIN names n ON tp.nconst = n.nconst
                    WHERE tb.titleType = 'movie' AND tb.genres IS NOT NULL AND tp.category IN ('director', 'actor')''')
    
    # query = text('''SELECT tb.tconst, tb.genres, tp.nconst, tp.category, tb.runtimeMinutes, tb.startYear, tb.originalTitle, tr.averageRating, tr.numVotes
    #                 FROM title_basics tb
    #                 LEFT JOIN title_principals tp ON tb.tconst = tp.tconst
    #                 LEFT JOIN title_ratings tr ON tb.tconst = tr.tconst
    #                 WHERE tb.titleType = 'movie' AND tb.genres IS NOT NULL AND tp.category IN ('director', 'actor')
    #                 AND tr.averageRating IS NOT NULL AND tr.numVotes >= 1000
    #                 ORDER BY tr.averageRating DESC, tr.numVotes DESC
    #                 ''')
    
    df = pd.read_sql(query, conn)
    return df

# def concat_names(group):
#     actor_name = group.loc[group['category'] == 'actor', 'nconst']
#     director_name = group.loc[group['category'] == 'director', 'nconst']
#     if not actor_name.empty and not director_name.empty:
#         return f"{actor_name.iloc[0]}, {director_name.iloc[0]}"
#     elif not actor_name.empty:
#         return f"{actor_name.iloc[0]}"
#     elif not director_name.empty:
#         return f"{director_name.iloc[0]}"
#     else:
#         return ''

def concat_names(group):
    actor_names = group.loc[group['category'] == 'actor', 'primaryName'].unique()
    actress_names = group.loc[group['category'] == 'actress', 'primaryName'].unique()
    director_names = group.loc[group['category'] == 'director', 'primaryName'].unique()
    names = list(actor_names) + list(actress_names) + list(director_names) 
    return ', '.join(names)


def primaryName(group):
    actor_name = group.loc[group['category'] == 'actor', 'primaryName']
    director_name = group.loc[group['category'] == 'director', 'primaryName']
    if not actor_name.empty and not director_name.empty:
        return f"{actor_name.iloc[0]}, {director_name.iloc[0]}"
    elif not actor_name.empty:
        return f"{actor_name.iloc[0]}"
    elif not director_name.empty:
        return f"{director_name.iloc[0]}"
    else:
        return ''

def create_features_cosine(df):
    df = df[['tconst', 'originalTitle', 'category', 'genres', 'nconst', 'runtimeMinutes', 'startYear', 'averageRating', 'primaryName']]
    df = df.dropna()

    # Regrouper les lignes avec les mêmes valeurs de colonnes
    grouped = df.groupby(['originalTitle'])

    # Concaténer les genres, runtimeMinutes, startYear et averageRating en une seule chaîne unique
    features = grouped.apply(lambda x: f"{x['genres'].iloc[0]},{x['averageRating'].iloc[0]},{concat_names(x)}").reset_index(name='features')

    # Fusionner la colonne "features" avec la colonne "originalTitle"
    result = pd.merge(df[['originalTitle']], features, on='originalTitle').drop_duplicates()
    result['features'] = result['features'].replace(' ', '', regex=True)
    # Enregistrer le résultat dans un fichier CSV
    result.to_csv('cosine_features_no_date.csv', index=False)

    return result

# def create_features_cosine(df):
#     df = df[['tconst', 'originalTitle', 'genres', 'category', 'nconst', 'runtimeMinutes', 'startYear', 'averageRating']]
#     df = df.dropna()
#     result = df.groupby(['originalTitle', 'genres', 'runtimeMinutes', 'startYear', 'averageRating']).apply(concat_names)
#     result = result.reset_index()
#     result['features'] = result.apply(lambda x: f"{x['genres']}, {x[0]}" if x[0] else '', axis=1)
#     result = result[result['features'] != '']
#     result = result[['originalTitle', 'features']]
#     result = result.set_index('originalTitle')
#     result['originalTitle'] = result.index
#     result = result.dropna(subset=['features'])
#     result = result.reindex(columns=['originalTitle', 'features'])
#     result = result.dropna(subset=['features'])
#     result.to_csv('cosine_features.csv', index=False)
#     return result

# def create_features_knn(df):
#     df = df[['tconst','originalTitle', 'genres', 'category', 'nconst', 'runtimeMinutes', 'startYear', 'averageRating','primaryName']]
#     print(df.head())
#     df = df.dropna()
#     df_agg = df.groupby(['originalTitle', 'genres','runtimeMinutes', 'startYear','averageRating','primaryName']).apply(concat_names).reset_index(name='actor_director')
#     df_agg[['actor', 'director']] = df_agg['actor_director'].str.split(',', expand=True)
#     df_agg = df_agg[['originalTitle', 'genres', 'actor', 'director', 'runtimeMinutes', 'startYear','averageRating','primaryName']]
#     df_agg = df_agg.dropna()
#     print(df_agg.head())
#     df_agg.to_csv('knn_feature.csv', index=False)
    
#     return df_agg

def create_features_knn(df):
    df = df[['tconst','originalTitle', 'genres', 'category', 'nconst', 'runtimeMinutes', 'startYear', 'averageRating','primaryName']]
    print(df.head())
    df = df.dropna()
    df_agg = df.groupby(['originalTitle', 'genres','runtimeMinutes', 'startYear','averageRating']).apply(primaryName).reset_index(name='actor_director')
    df_agg[['actor', 'director']] = df_agg['actor_director'].str.split(',', expand=True)
    df_agg = df_agg[['originalTitle', 'genres', 'actor', 'director', 'runtimeMinutes', 'startYear','averageRating']]
    df_agg = df_agg.dropna()
    print(df_agg.head())
    df_agg.to_csv('knn_features_names.csv', index=False)
    return df_agg

def write_output(result):
    result.to_csv('1kbest.csv', index=False)

def main():
    start_time = time.time()
    config = read_config()
    conn = connect_to_database(config)
    df = get_data(conn)
    if not df.empty:
        result = create_features_cosine(df)
        # result = create_features_knn(df)
    #     for row in result.itertuples():
    #         print(row.features)
    #     write_output(result)
    # else:
    #     print("No results found")
    elapsed_time = time.time() - start_time
    print(f"Temps d'exécution : {elapsed_time:.2f} secondes.")

if __name__ == "__main__":
    main()
