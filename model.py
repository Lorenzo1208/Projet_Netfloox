import yaml
import pandas as pd
from sqlalchemy import create_engine, text

def read_config():
    with open("config.yaml", 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return config['mysql2']

def connect_to_database(config):
    engine = create_engine("{driver}://{user}:{password}@{host}/{database}".format(**config))
    conn = engine.connect()
    return conn

def get_data(conn):
    query = text('''SELECT tb.tconst, tb.genres, tp.nconst, tp.category, tb.runtimeMinutes, tb.startYear
                    FROM title_basics tb
                    LEFT JOIN title_principals tp ON tb.tconst = tp.tconst
                    WHERE tb.titleType = 'movie' AND tb.genres IS NOT NULL AND tp.category IN ('director', 'actor') LIMIT 100000;''')
    df = pd.read_sql(query, conn)
    return df

def concat_names(group):
    actor_name = group.loc[group['category'] == 'actor', 'nconst']
    director_name = group.loc[group['category'] == 'director', 'nconst']
    if not actor_name.empty and not director_name.empty:
        return f"{actor_name.iloc[0]}, {director_name.iloc[0]}"
    elif not actor_name.empty:
        return f"{actor_name.iloc[0]},"
    elif not director_name.empty:
        return f"{director_name.iloc[0]},"
    else:
        return ''

def create_features(df):
    result = df.groupby(['tconst', 'genres', 'runtimeMinutes', 'startYear']).apply(concat_names)
    result = result.reset_index()
    result['features'] = result.apply(lambda x: f"{x['tconst']}, {x['genres']}, {x['runtimeMinutes']}, {x['startYear']}, {x[0]}", axis=1)
    result = result[['features']]
    return result

def write_output(result):
    result.to_csv('output.csv', index=False)

def main():
    config = read_config()
    conn = connect_to_database(config)
    df = get_data(conn)
    if not df.empty:
        result = create_features(df)
        for row in result.itertuples():
            print(row.features)
        write_output(result)
    else:
        print("No results found")

if __name__ == "__main__":
    main()
