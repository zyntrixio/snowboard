from dash import Dash, html, dash_table
from ext_data import fetch_data_from_snowflake

app = Dash(__name__)

db1: str = "SELECT * FROM output.ext.ext_dashboard_view_usr"

df = fetch_data_from_snowflake(db1)

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
])


if __name__ == "__main__":
    app.run_server(debug=True)
