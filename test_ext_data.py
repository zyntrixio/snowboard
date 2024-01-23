import pandas as pd
from ext_data import fetch_data_from_snowflake

def test_fetch_data_from_snowflake(mocker):

    # Mock the Snowflake connector
    mock_cursor = mocker.MagicMock()
    mock_cursor.execute.return_value = None
    mock_cursor.description = [("COLUMN_1",), ("COLUMN_2",)]
    mock_cursor.__iter__.return_value = iter([("value1", "value2")])

    mock_connection = mocker.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch('env.snowflake.connector.connect',
                 return_value=mock_connection)

    # Call the function
    result_df = fetch_data_from_snowflake("SELECT * FROM sandbox.cm_sandbox.connection_test")  # noqa: E501

    # Assertions
    assert isinstance(result_df, pd.DataFrame)
    assert list(result_df.columns) == ["COLUMN_1", "COLUMN_2"]
    assert result_df.iloc[0].tolist() == [1, 1]