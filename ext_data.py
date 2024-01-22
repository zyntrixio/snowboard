import pandas as pd
from typing import Optional
from env import cnn

def fetch_data_from_snowflake(sql_command: str) -> Optional[pd.DataFrame]:
    """Executes a SQL command on a Snowflake data warehouse
       and returns the results as a Pandas DataFrame.

    :param sql_command: SQL query to execute
    :return: Pandas DataFrame containing the query results or None if an error occurs
    """

    try:
        cursor = cnn.cursor()
        cursor.execute(sql_command)

        df = pd.DataFrame.from_records(iter(cursor),
                                       columns=[x[0] for x in cursor.description])
        return df
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        cnn.close()

