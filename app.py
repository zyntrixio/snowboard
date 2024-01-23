from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from ext_data import fetch_data_from_snowflake
from datetime import datetime as dt
import pandas as pd

app = Dash(__name__)


db2: str = "SELECT * FROM output.ext.ext_dashboard_view_lc_txns"

df_usr = fetch_data_from_snowflake(db2)

df_usr = pd.DataFrame(df_usr)
# df_usr = df_usr["date"].to_datetime() 
# DO WE NEED TO INDEX AT DATE? MISSING DAYS ON CUMULATIVE SUMS ISSUE

# Define the layout of the app
app.layout = html.Div(
    [
        dcc.Graph(id="graph"),
        html.Label("Select a column for the X-axis:"),
        dcc.Dropdown(
            id="xaxis-column",
            options=[{"label": i, "value": i} for i in df_usr.columns],
            value="date",
        ),
        html.Label("Select a column for the Y-axis:"),
        dcc.Dropdown(
            id="yaxis-column",
            options=[{"label": i, "value": i} for i in df_usr.columns],
            value="period_joins",
        ),
    ]
)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Label("Select a date range:"),
                dcc.DatePickerRange(
                    id="date-picker-range",
                    start_date=df_usr["date"].min(),
                    end_date=df_usr["date"].max(),
                    display_format="YYYY-MM-DD",
                ),
                html.Label("Select a column for the X-axis:"),
                dcc.Dropdown(
                    id="xaxis-column",
                    options=[{"label": i, "value": i} for i in df_usr.columns],
                    value="date",
                ),
                html.Label("Select a column for the Y-axis:"),
                dcc.Dropdown(
                    id="yaxis-column",
                    options=[{"label": i, "value": i} for i in df_usr.columns],
                    value="period_joins",
                ),
            ]
        ),
        dcc.Graph(id="graph"),
    ]
)

# ... (callback and app run code)


# Callback for updating the graph
@app.callback(
    Output("graph", "figure"),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('xaxis-column','value'),
     Input('yaxis-column','value')],
)
def update_graph(start_date, end_date, xaxis_column_name, yaxis_column_name):
    filtered_df = df_usr[(df_usr['date'] >= start_date & (df_usr['date'] <= end_date))]
    return px.bar(filtered_df, x=xaxis_column_name,y=yaxis_column_name)


if __name__ == "__main__":
    app.run_server(debug=True)
