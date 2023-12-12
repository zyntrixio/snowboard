import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from env import cnn

app = dash.Dash(__name__, requests_pathname_prefix="/dashboard/")

cs = cnn.cursor()
sql = "SELECT transaction_id FROM prod.bink_secure.fact_transaction WHERE duplicate_transaction = TRUE"
cs.execute(sql)
df = cs.fetch_pandas_all
print(df)
cs.close()
cnn.close()


# Sample data and graphs (replace with your own data)
# Sample data is provided just for demonstration purposes

# Sample data for graphs
categories = ["Loyalty Cards", "Payment Cards", "Users", "Transactions"]

overview_graphs = []
detailed_graphs = []
exploration_graphs = []

for category in categories:
    overview_graphs.append(
        dcc.Graph(
            id=f'{category.lower().replace(" ", "_")}_overview_graph',
            figure=px.line(
                x=[1, 2, 3], y=[4, 2, 3], title=f"Overview Graph for {category}"
            ),
        )
    )

    detailed_graphs.append(
        dcc.Graph(
            id=f'{category.lower().replace(" ", "_")}_detailed_graph_1',
            figure=px.bar(
                x=[1, 2, 3], y=[2, 3, 4], title=f"Detailed Graph 1 for {category}"
            ),
        )
    )
    detailed_graphs.append(
        dcc.Graph(
            id=f'{category.lower().replace(" ", "_")}_detailed_graph_2',
            figure=px.scatter(
                x=[1, 2, 3], y=[3, 4, 2], title=f"Detailed Graph 2 for {category}"
            ),
        )
    )
    detailed_graphs.append(
        dcc.Graph(
            id=f'{category.lower().replace(" ", "_")}_exploration',
            figure=px.line(
                x=[1, 2, 3], y=[2, 2, 2], title=f"Detailed Graph 3 for {category}"
            ),
        )
    )

# App layout
app.layout = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            value="overview",
            children=[
                dcc.Tab(label="Overview", value="overview"),
                dcc.Tab(label="Loyalty Cards", value="loyalty_cards"),
                dcc.Tab(label="Payment Cards", value="payment_cards"),
                dcc.Tab(label="Users", value="users"),
                dcc.Tab(label="Transactions", value="transactions"),
            ],
        ),
        html.Div(id="page-content"),
    ]
)


# Callback to update page content based on selected tab
@app.callback(Output("page-content", "children"), [Input("tabs", "value")])
def display_content(selected_tab):
    if selected_tab == "overview":
        return html.Div(
            [
                html.H1("High-Level Overview"),
                html.Div([html.H2("Loyalty Cards"), *overview_graphs[:3]]),
                html.Div([html.H2("Payment Cards"), *overview_graphs[3:6]]),
                html.Div([html.H2("Users"), *overview_graphs[6:9]]),
                html.Div([html.H2("Transactions"), *overview_graphs[9:12]]),
            ]
        )
    else:
        category_index = categories.index(selected_tab.capitalize())
        return html.Div(
            [
                html.H1(f"{selected_tab} Details"),
                html.Div(
                    [
                        html.H2("Section 1"),
                        *detailed_graphs[category_index * 12 : category_index * 12 + 3],
                    ]
                ),
                html.Div(
                    [
                        html.H2("Section 2"),
                        *detailed_graphs[
                            category_index * 12 + 3 : category_index * 12 + 6
                        ],
                    ]
                ),
                html.Div(
                    [
                        html.H2("Section 3"),
                        *detailed_graphs[
                            category_index * 12 + 6 : category_index * 12 + 9
                        ],
                    ]
                ),
                html.Div(
                    [
                        html.H2("Section 4"),
                        *detailed_graphs[
                            category_index * 12 + 9 : category_index * 12 + 12
                        ],
                    ]
                ),
            ]
        )


if __name__ == "__main__":
    app.run_server(debug=True)
