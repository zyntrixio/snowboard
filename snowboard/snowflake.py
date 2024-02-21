"""Snowflake Module."""

from __future__ import annotations

import json

import pandas as pd
import snowflake.connector

from snowboard.settings import keyvault_client

credentials = json.loads(keyvault_client.get_secret("snowflake").value)

conn = snowflake.connector.connect(
    user=credentials["user"],
    password=credentials["password"],
    account=credentials["account"],
    warehouse=credentials["warehouse"],
    database=credentials["database"],
    schema=credentials["schema"],
)


def fetch_data_from_snowflake(sql_command: str) -> pd.DataFrame:
    """Get data from snowflake.

    Args:
        sql_command (str): takes SQL statement as string

    Returns:
        pd.DataFrame: Returns a pandas dataframe
    """
    cursor = conn.cursor()
    cursor.execute(sql_command)

    return pd.DataFrame.from_records(iter(cursor), columns=[x[0] for x in cursor.description])
