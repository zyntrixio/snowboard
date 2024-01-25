import pandas as pd
from typing import Optional
from env import cnn

def fetch_data_from_snowflake(sql_command: str) -> Optional[pd.DataFrame]:
    """A function to get data from snowflake

    Args:
        sql_command (str): takes SQL statement as string

    Returns:
        Optional[pd.DataFrame]: Returns a pandas dataframe
    """

    try:
        cursor = cnn.cursor()
        cursor.execute(sql_command)

        df = pd.DataFrame.from_records(iter(cursor),
                                       columns=[x[0] for x in cursor.description])
        return df
    except Exception as e:
        print(f"An error occured: {e}")
