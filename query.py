from sqlalchemy import create_engine, text
import pandas as pd
import sqlalchemy
import yaml
import traceback

# Load the YAML configuration file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Get the MySQL configuration
cfg = config['mysql-datalab']

# Create the database connection URL
url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)

# Create the database engine
engine = create_engine(url)


query = text("""SELECT * FROM title_basics LIMIT 10
""")

# Execute the query using the engine
with engine.connect() as con:
    result = con.execute(query)
    for row in result:
        print(row)
