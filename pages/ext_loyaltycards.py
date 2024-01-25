import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from loguru import logger
from datetime import datetime, timedelta
from ext_data import fetch_data_from_snowflake
from app import app

loyalty_card_query: str = """SELECT * FROM output.ext.ext_dashboard_view_lc_txns 
                            where DATE > '2023-02-01' and CATEGORY = 'LOYALTY CARD';"""

df_loyalty_card = pd.DataFrame(fetch_data_from_snowflake(loyalty_card_query))

df_loyalty_card.rename(
    columns={
        "DATE": "Date",
        "LOYALTY_PLAN_COMPANY": "Retailer",
        "CHANNEL": "Channel",
        "BRAND": "Brand",
        "LC013__SUCCESSFUL_LOYALTY_CARD_JOINS__DAILY_CHANNEL_BRAND_RETAILER__COUNT": "Period Joins",  # noqa: E501
        "LC009__SUCCESSFUL_LOYALTY_CARD_LINKS__DAILY_CHANNEL_BRAND_RETAILER__COUNT": "Period Links",  # noqa: E501
        "LC021__SUCCESSFUL_LOYALTY_CARD_JOINS__DAILY_CHANNEL_BRAND_RETAILER__DCOUNT_USER": "Distinct Joins",  # noqa: E501
        "LC017__SUCCESSFUL_LOYALTY_CARD_LINKS__DAILY_CHANNEL_BRAND_RETAILER__DCOUNT_USER": "Distinct Links",  # noqa: E501
        "LC075__SUCCESSFUL_LOYALTY_CARD_JOINS__DAILY_CHANNEL_BRAND_RETAILER__CSUM": "Cumulative Joins",  # noqa: E501
        "LC079__SUCCESSFUL_LOYALTY_CARD_LINKS__DAILY_CHANNEL_BRAND_RETAILER__CSUM": "Cumulative Links",  # noqa: E501
    },
    inplace=True,
)


df_lc__tab = df_loyalty_card.pivot_table(
    values="Period Joins",
    index=["Retailer"],
    columns=["Brand"],
    aggfunc="sum",
    fill_value=0,
)
df_lc__tab = df_lc__tab.reset_index()
df_lc__tab.columns = df_lc__tab.columns.astype("str")

df_lc__lbg_graph = df_loyalty_card[df_loyalty_card["Channel"] == "LLOYDS"]
df_lc__mixr_graph = df_loyalty_card[df_loyalty_card["Channel"] == "MIXR"]

last_14 = datetime.today().date() - timedelta(days=14)
df_lc__btab1 = df_loyalty_card[df_loyalty_card["Date"] > last_14].pivot_table(
    values="Period Joins",
    index=["Channel"],
    columns=["Date"],
    aggfunc="sum",
    fill_value=0,
)
df_lc__btab1 = df_lc__btab1.reset_index()
df_lc__btab1.columns = df_lc__btab1.columns.astype("str")

df_lc__btab2 = df_loyalty_card.copy()
df_lc__btab2["Date"] = pd.to_datetime(df_lc__btab2["Date"]).dt.to_period("M")
df_lc__btab2 = df_lc__btab2.pivot_table(
    values="Period Joins",
    index=["Channel"],
    columns=["Date"],
    aggfunc="sum",
    fill_value=0,
)
df_lc__btab2 = df_lc__btab2.reset_index()
df_lc__btab2.columns = df_lc__btab2.columns.astype("str")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            "Total Joins by Retailer and Channel",
                            className="text-center text-secondary, mb-4",
                            style={"text-align": "center"},
                        ),
                        html.Br(),
                        dash_table.DataTable(
                            df_lc__tab.to_dict("records"),
                            [{"name": i, "id": i} for i in df_lc__tab.columns],
                            id="txn_by_merchant",
                            style_cell={
                                "textAlign": "left",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "25",
                                "font-weight": 300,
                            },
                            style_cell_conditional=[
                                {"if": {"column_id": "name"}, "width": "30%"}
                            ],
                            style_header={
                                "backgroundColor": "rgb(30, 30, 30)",
                                "color": "white",
                                "border": "1px solid blue",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "25",
                                "font-weight": 700,
                            },
                            style_data={
                                "backgroundColor": "rgb(50, 50, 50)",
                                "color": "white",
                                "border": "1px solid blue",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "20",
                                "font-weight": 300,
                            },
                        ),
                    ],
                    xs=12,
                    sm=12,
                    md=12,
                    lg=6,
                    xl=6,
                ),
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("LBG Graph: Daily Bar and Cumulative Line"),
                        dcc.Graph(
                            id="txn_by_merchant",
                            figure=px.bar(
                                data_frame=df_lc__lbg_graph,
                                x="Date",
                                y="Period Joins",
                                color="Retailer",
                                hover_data=["Retailer", "Period Joins"],
                                template="plotly_dark",
                            ),
                        ),
                    ],
                    xs=12,
                    sm=12,
                    md=12,
                    lg=6,
                    xl=6,
                )
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("MiXR Graph: Daily Bar and Cumulative Line"),
                        dcc.Graph(
                            id="txn_by_merchant",
                            figure=px.bar(
                                data_frame=df_lc__mixr_graph,
                                x="Date",
                                y="Period Joins",
                                color="Retailer",
                                hover_data=["Retailer", "Period Joins"],
                                template="plotly_dark",
                            ),
                        ),
                    ],
                    xs=12,
                    sm=12,
                    md=12,
                    lg=6,
                    xl=6,
                )
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            "Daily Matched Transactions by Channel",
                            className="text-center text-secondary, mb-4",
                            style={"text-align": "center"},
                        ),
                        html.Br(),
                        dash_table.DataTable(
                            df_lc__btab1.to_dict("records"),
                            [{"name": i, "id": i} for i in df_lc__btab1.columns],
                            id="txn_by_channel",
                            style_cell={
                                "textAlign": "left",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "25",
                                "font-weight": 300,
                            },
                            style_cell_conditional=[
                                {"if": {"column_id": "name"}, "width": "30%"}
                            ],
                            style_header={
                                "backgroundColor": "rgb(30, 30, 30)",
                                "color": "white",
                                "border": "1px solid blue",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "25",
                                "font-weight": 700,
                            },
                            style_data={
                                "backgroundColor": "rgb(50, 50, 50)",
                                "color": "white",
                                "border": "1px solid blue",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "20",
                                "font-weight": 300,
                            },
                        ),
                    ],
                    xs=12,
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
            ],
            justify="center",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            "Monthly Matched Transactions by Channel",
                            className="text-center text-secondary, mb-4",
                            style={"text-align": "center"},
                        ),
                        html.Br(),
                        dash_table.DataTable(
                            df_lc__btab2.to_dict("records"),
                            [{"name": i, "id": i} for i in df_lc__btab2.columns],
                            id="txn_by_channel",
                            style_cell={
                                "textAlign": "left",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "25",
                                "font-weight": 300,
                            },
                            style_cell_conditional=[
                                {"if": {"column_id": "name"}, "width": "30%"}
                            ],
                            style_header={
                                "backgroundColor": "rgb(30, 30, 30)",
                                "color": "white",
                                "border": "1px solid blue",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "25",
                                "font-weight": 700,
                            },
                            style_data={
                                "backgroundColor": "rgb(50, 50, 50)",
                                "color": "white",
                                "border": "1px solid blue",
                                "font-family": "Roboto, sans-serif",
                                "fontSize": "20",
                                "font-weight": 300,
                            },
                        ),
                    ],
                    xs=12,
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
            ],
            justify="around",
        ),
    ],
    fluid=True,
)
