from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy
import yaml
import numpy as np
import warnings

warnings.filterwarnings("ignore")

def split_and_explode(x):
    
    x = str(x) if not isinstance(x, str) else x
    return x.split(",") if x else None

def split(df):
    if not df :
        df = df
    else:
        df = df.split(",")[0]
    return df

if __name__ == "__main__":
    
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        #print(config)

    cfg=config['mysql2']
    print(cfg)

    url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)
    print('URL', url)

    engine = create_engine(url)

    files=['name.basics', 'title.akas', 'title.basics', 'title.crew', 'title.episode', 'title.principals', 'title.ratings']
    
    for name in files:
        print(f"Loading {name}")
        df = pd.read_csv(f"{name}.tsv.gz", sep='\t', compression='gzip', nrows=100, quoting=3, low_memory=False)
        # df = df.where((pd.notnull(df)), None)
        df = df.applymap(lambda x: None if x == r'\N' else x)
        table_name = name.replace('.', '_')
        df.to_sql(table_name, engine, if_exists='append', index=False)
        # df.to_sql(table_name, engine, if_exists='append', index=False)
        # if table_name == "title_crew":
        #     title_crew_df = df[['tconst', 'writers', 'directors']]
        #     if "writers" in title_crew_df.columns:
        #         title_crew_df["writers"] = df["writers"].apply(split)
        #     if "directors" in title_crew_df.columns:
        #         title_crew_df["directors"] = df["directors"].apply(split)
        #     title_crew_df.to_sql("title_crew", engine, if_exists='append', index=False)
            # if "writers" in df.columns:
                # print(df.shape)
            #     writers_df = df[['tconst', 'writers']]
            #     writers_df["writers"] = df["writers"].apply(split_and_explode)
            #     writers_df = writers_df.explode("writers")
            #     writers_df.to_sql("writers", engine, if_exists='append', index=False)
            # if "directors" in df.columns:
            #     directors_df = df[['tconst', 'directors']]
            #     directors_df["directors"] = df["directors"].apply(split_and_explode)
            #     directors_df = directors_df.explode("directors")
            #     directors_df.to_sql("directors", engine, if_exists='append', index=False)
        # elif table_name == "name_basics":
        #     name_df = df[['nconst','knownForTitles']]
        #     if "knownForTitles" in name_df.columns:
        #         name_df["knownForTitles"] = df["knownForTitles"].apply(split)
        #     name_df.to_sql("name_basics", engine, if_exists='append', index=False)
                # knownfortitles_df = df[['nconst', 'knownForTitles']]
                # knownfortitles_df["knownForTitles"] = df["knownForTitles"].apply(split_and_explode)
                # knownfortitles_df = knownfortitles_df.explode("knownForTitles")
                # knownfortitles_df.to_sql("knownfortitles", engine, if_exists='append', index=False)
            # if "primaryProfession" in df.columns:
            #     primaryprofession_df = df[['nconst','primaryName','birthYear','deathYear','primaryProfession']]
            #     primaryprofession_df["nconst"] = df["nconst"].apply(split_and_explode)
            #     primaryprofession_df = primaryprofession_df.explode("nconst")
            #     primaryprofession_df.to_sql("names", engine, if_exists='append', index=False)
        # else:
        #     df.to_sql(table_name, engine, if_exists='append', index=False)
