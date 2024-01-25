# %%
# from turtle import left, width
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import (
    Input,
    Output,
)  # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc
from loguru import logger
from datetime import datetime, timedelta
from ext_data import fetch_data_from_snowflake
from app import app

# %%

txns_query: str = """SELECT * FROM output.ext.ext_dashboard_view_lc_txns 
                     where DATE > '2023-02-01'
                     and CATEGORY = 'TRANSACTIONS';"""

df_txn = pd.DataFrame(fetch_data_from_snowflake(txns_query))

df_txn.rename(
    columns={
        "DATE": "Date",
        "LOYALTY_PLAN_COMPANY": "Retailer",
        "CHANNEL": "Channel",
        "BRAND": "Brand",
        "T075__TXNS__DAILY_CHANNEL_BRAND_RETAILER__DCOUNT": "Transaction Count",
        "T069__TXNS__DAILY_CHANNEL_BRAND_RETAILER__CSUM": "Transaction Cumulative",
    },
    inplace=True,
)

# %%
df_txn__ttab = df_txn.pivot_table(
    values="Transaction Count",
    index=["Retailer"],
    columns=["Brand"],
    aggfunc="sum",
    fill_value=0,
)
df_txn__ttab = df_txn__ttab.reset_index()
df_txn__ttab.columns = df_txn__ttab.columns.astype("str")
df_txn__ttab
# %%
# %%
df_txn__lbg_graph = df_txn[df_txn["Channel"] == "LLOYDS"]
df_txn__mixr_graph = df_txn[df_txn["Channel"] == "MIXR"]
# df_txn__btab1 = df_txn.groupby(["Date","Channel"]).sum()["Transaction Count"].reset_index()
# %%
last_14 = datetime.today().date() - timedelta(days=14)
df_txn__btab1 = df_txn[df_txn["Date"] > last_14].pivot_table(
    values="Transaction Count",
    index=["Channel"],
    columns=["Date"],
    aggfunc="sum",
    fill_value=0,
)
df_txn__btab1 = df_txn__btab1.reset_index()
df_txn__btab1.columns = df_txn__btab1.columns.astype("str")
# %%
df_txn__btab2 = df_txn.copy()
df_txn__btab2["Date"] = pd.to_datetime(df_txn__btab2["Date"]).dt.to_period("M")
df_txn__btab2 = df_txn__btab2.pivot_table(
    values="Transaction Count",
    index=["Channel"],
    columns=["Date"],
    aggfunc="sum",
    fill_value=0,
)
df_txn__btab2 = df_txn__btab2.reset_index()
df_txn__btab2.columns = df_txn__btab2.columns.astype("str")

# %%
# %%
# ------------------------------------------------------------------------------
# App layout - everything in the dash goes in here including the HTML
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            "Total Matched Transactions by Merchant and Channel",
                            className="text-center text-secondary, mb-4",
                            style={"text-align": "center"},
                        ),
                        html.Br(),
                        dash_table.DataTable(
                            df_txn__ttab.to_dict("records"),
                            [{"name": i, "id": i} for i in df_txn__ttab.columns],
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
        # dbc.Row([
        #     dbc.Col(
        #         [
        #             dcc.Dropdown(id="slct_year_txn",
        #                 options=[
        #                     {"label": "2019", "value": 2023},
        #                     {"label": "2020", "value": 2024}],
        #                 multi=False,
        #                 value=2024,
        #                 style={'width': "40%"},
        #                 persistence=True,
        #                 persistence_type='local'
        #                 ),
        #             html.Div(id='output_container_txn', children=[]),
        #             ],
        #         xs=12, sm=12, md=12, lg=6, xl=6
        #         )
        #     ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("LBG Graph: Daily Bar and Cumulative Line"),
                        dcc.Graph(
                            id="txn_by_merchant",
                            figure=px.bar(
                                data_frame=df_txn__lbg_graph,
                                x="Date",
                                y="Transaction Count",
                                color="Retailer",
                                hover_data=["Retailer", "Transaction Count"],
                                template="plotly_dark",
                            ),
                        ),
                    ],  # width ={'size':6, 'offset':0,'order':1}
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
                                data_frame=df_txn__mixr_graph,
                                x="Date",
                                y="Transaction Count",
                                color="Retailer",
                                hover_data=["Retailer", "Transaction Count"],
                                template="plotly_dark",
                            ),
                        ),
                    ],  # width ={'size':6, 'offset':0,'order':1}
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
                            df_txn__btab1.to_dict("records"),
                            [{"name": i, "id": i} for i in df_txn__btab1.columns],
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
                            df_txn__btab2.to_dict("records"),
                            [{"name": i, "id": i} for i in df_txn__btab2.columns],
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

# %%
