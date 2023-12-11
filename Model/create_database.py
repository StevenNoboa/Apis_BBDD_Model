import sqlite3
import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

def create_database(csv_file, db_file, table_name):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(csv_file, index_col=0)
    df.rename(columns={"newpaper": "newspaper"},inplace=True)
    df.at[0, 'newspaper'] = 69.2

    # Create a SQLite connection and a cursor
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Create a table in the database
    df.to_sql(table_name, connection, if_exists='replace', index_label= None, index=False)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    csv_file = ".\\ejercicio\\data\\Advertising.csv"
    db_file = ".\\ejercicio\\data\\Advertising.db"
    table_name = "advertising"


    create_database(csv_file, db_file, table_name)
    print(f"Database '{db_file}' created and table '{table_name}' populated with data from '{csv_file}'.")