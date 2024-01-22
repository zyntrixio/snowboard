import pandas as pd
import pytest
from ext_data import fetch_data_from_snowflake

def test_fetch_data_from_snowflake(mocker):

    # Mock the Snowflake connector
    mock_cursor = mocker.MagicMock()
    mock_cursor.execute.return_value = None
    mock_cursor.description = [("column1",), ("column2",)]
    mock_cursor.__iter__.return_value = iter([("value1", "value2")])

    mock_connection = mocker.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('your_module.snowflake.connector.connect',
                 return_value=mock_connection)

    # Call the function
    result_df = fetch_data_from_snowflake("SELECT * FROM SANDBOX.CM_SANDBOX.QA_DATA_TEST")

    # Assertions
    assert isinstance(result_df, pd.DataFrame)
    assert list(result_df.columns) == ["column1", "column2"]
    assert result_df.iloc[0].tolist() == ["value1", "value2"]