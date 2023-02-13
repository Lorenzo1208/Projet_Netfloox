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
    cfg = config['mysql']
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
    query = text("""SELECT * FROM title_basics;""")
    query2 = text("""SELECT birthYear, count(*) AS N FROM names GROUP BY birthYear;""")
    df = get_data(engine, query2)
    plot_data(df)

if __name__ == '__main__':
    main()
