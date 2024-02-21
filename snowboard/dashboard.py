"""Root Module for the Dashboard Application."""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from snowboard.pages import ext_loyaltycards, ext_transactions

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
)

app.layout = dash.html.Div(
    [
        dash.dcc.Location(id="url", refresh=False),
        dash.html.Div(
            dbc.Nav(
                [
                    dbc.NavLink("Transactions", active=True, href="/pages/ext_txns"),
                    dbc.NavLink("Payment Cards", href="/pages/pc_graphs"),
                    dbc.NavLink("Loyalty Cards", href="/pages/ext_lc"),
                ],
            ),
        ),
        dash.html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dash.html.H1(
                            "Performance Dashboard",
                            className="text-center text-primary, mb-4",
                            style={"text-align": "center"},
                        ),
                        width=12,
                    ),
                ],
            ),
        ),
        dash.html.Div(id="page-content", children=[]),
        dash.dcc.Store(id="store-dropdown-value", data=None),
    ],
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname: str) -> dbc.Container | str:
    """Return a page layout based on the URL pathname."""
    if pathname == "/pages/ext_txns":
        return ext_transactions.layout
    if pathname == "/pages/ext_lc":
        return ext_loyaltycards.layout
    return "404 Page Error! Please choose a link"


server = app.server
