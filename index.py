from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from pages import ext_transactions


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        dbc.Nav([
            dbc.NavLink("Transactions", active=True, href="/pages/ext_txns"),
            dbc.NavLink("Payment Cards", href="/pages/pc_graphs"),
            dbc.NavLink("Loyalty Cards", href="/pages/txn_graphs")
        ])
    ),
    html.Div(dbc.Row([
        dbc.Col(
            html.H1("Performance Dashboard",
            className='text-center text-primary, mb-4', style={'text-align': 'center'}),
            width = 12

            )
    ])),

    html.Div(id='page-content', children=[]),

    dcc.Store(id="store-dropdown-value", data=None)

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/ext_txns':
        return ext_transactions.layout      
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)
