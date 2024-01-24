from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from ext_data import fetch_data_from_snowflake
from datetime import datetime as dt
import pandas as pd

app = Dash(__name__)


db2: str = "SELECT * FROM output.ext.ext_dashboard_view_lc_txns"

df_usr = pd.DataFrame(fetch_data_from_snowflake(db2))


# App layout
app.layout = html.Div(
    [
        html.H1("Ext Dashboard"),
        # Table at the top
        html.Table(
            [
                html.Tr([html.Th(col) for col in df.columns]),
                *[
                    html.Tr([html.Td(df_usr.iloc[i][col]) for col in df_usr.columns])
                    for i in range(len(df))
                ],
            ]
        ),
        # Graph showing a bar chart and a line graph
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df["Date"],
                        "y": df["Period_Joins"],
                        "type": "bar",
                        "name": "Period_Joins",
                    },
                    {
                        "x": df["Date"],
                        "y": df["Cumulative_Joins"],
                        "type": "line",
                        "name": "Cumulative_Joins",
                    },
                ],
                "layout": {"title": "Bar Chart and Line Graph"},
            }
        ),
        # Two tables at the bottom
        html.Table(
            [
                html.Tr([html.Th(col) for col in df.columns]),
                *[
                    html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                    for i in range(len(df))
                ],
            ]
        ),
        html.Table(
            [
                html.Tr([html.Th(col) for col in df.columns]),
                *[
                    html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                    for i in range(len(df))
                ],
            ]
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
