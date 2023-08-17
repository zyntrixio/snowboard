import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Sample data and graphs (replace with your own data)
# Sample data is provided just for demonstration purposes

# Sample data for graphs
categories = ['Loyalty Cards', 'Payment Cards', 'Users', 'Transactions']

overview_graphs = []
detailed_graphs = []
exploration_graphs = []

for category in categories:
    overview_graphs.append(
        dcc.Graph(
            id=f'{category.lower().replace(" ", "_")}_overview_graph',
            figure=px.line(x=[1, 2, 3], y=[4, 2, 3], title=f'Overview Graph for {category}')
        )
    )
    
    detailed_graphs.append(
        dcc.Graph(
            id=f'{category.lower().replace(" ", "_")}_detailed_graph_1',
            figure=px.bar(x=[1, 2, 3], y=[2, 3, 4], title=f'Detailed Graph 1 for {category}')
        )
    )
    detailed_graphs.append(
        dcc.Graph(
            id=f'{category.lower().replace(" ", "_")}_detailed_graph_2',
            figure=px.scatter(x=[1, 2, 3], y=[3, 4, 2], title=f'Detailed Graph 2 for {category}')
        )
    )
    detailed_graphs.append(
        dcc.Graph(
            id=f'{category.lower().replace(" ", "_")}_detailed_graph_3',
            figure=px.line(x=[1, 2, 3], y=[2, 2, 2], title=f'Detailed Graph 3 for {category}')
        )
    )

    # Exploration graphs
    exploration_graphs.append(
        html.Div([
            dcc.Dropdown(
                id=f'{category.lower().replace(" ", "_")}_exploration_graph_type',
                options=[
                    {'label': 'Bar', 'value': 'bar'},
                    {'label': 'Scatter', 'value': 'scatter'},
                    {'label': 'Line', 'value': 'line'}
                ],
                value='bar'
            ),
            dcc.Dropdown(
                id=f'{category.lower().replace(" ", "_")}_exploration_metric',
                options=[
                    {'label': 'Metric 1', 'value': 'metric1'},
                    {'label': 'Metric 2', 'value': 'metric2'},
                    {'label': 'Metric 3', 'value': 'metric3'}
                ],
                value='metric1'
            ),
            dcc.Graph(
                id=f'{category.lower().replace(" ", "_")}_exploration_graph',
                # Initial graph will be added in the callback
            )
        ])
    )

# App layout
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='overview', children=[
        dcc.Tab(label='Overview', value='overview'),
        dcc.Tab(label='Loyalty Cards', value='loyalty_cards'),
        dcc.Tab(label='Payment Cards', value='payment_cards'),
        dcc.Tab(label='Users', value='users'),
        dcc.Tab(label='Transactions', value='transactions'),
    ]),
    html.Div(id='page-content')
])

# Callback to update page content based on selected tab
@app.callback(Output('page-content', 'children'), [Input('tabs', 'value')])
def display_content(selected_tab):
    if selected_tab == 'overview':
        return html.Div([
            html.H1('High-Level Overview'),
            html.Div([
                html.H2('Loyalty Cards'),
                *overview_graphs[:3]
            ]),
            html.Div([
                html.H2('Payment Cards'),
                *overview_graphs[3:6]
            ]),
            html.Div([
                html.H2('Users'),
                *overview_graphs[6:9]
            ]),
            html.Div([
                html.H2('Transactions'),
                *overview_graphs[9:12]
            ])
        ])
    else:
        category_index = categories.index(selected_tab.capitalize())
        return html.Div([
            html.H1(f'{selected_tab} Details'),
            html.Div([
                html.H2('Section 1'),
                *detailed_graphs[category_index * 12: category_index * 12 + 3]
            ]),
            html.Div([
                html.H2('Section 2'),
                *detailed_graphs[category_index * 12 + 3: category_index * 12 + 6]
            ]),
            html.Div([
                html.H2('Section 3'),
                *detailed_graphs[category_index * 12 + 6: category_index * 12 + 9]
            ]),
            html.Div([
                html.H2('Section 4'),
                *detailed_graphs[category_index * 12 + 9: category_index * 12 + 12]
            ]),
            *exploration_graphs[category_index]
        ])

# Callback to update exploration graphs based on dropdown selections
@app.callback(
    Output('loyalty_cards_exploration_graph', 'figure'),
    Output('payment_cards_exploration_graph', 'figure'),
    Output('users_exploration_graph', 'figure'),
    Output('transactions_exploration_graph', 'figure'),
    Input('loyalty_cards_exploration_graph_type', 'value'),
    Input('loyalty_cards_exploration_metric', 'value'),
    Input('payment_cards_exploration_graph_type', 'value'),
    Input('payment_cards_exploration_metric', 'value'),
    Input('users_exploration_graph_type', 'value'),
    Input('users_exploration_metric', 'value'),
    Input('transactions_exploration_graph_type', 'value'),
    Input('transactions_exploration_metric', 'value'),
)
def update_exploration_graphs(
    loyalty_cards_graph_type, loyalty_cards_metric,
    payment_cards_graph_type, payment_cards_metric,
    users_graph_type, users_metric,
    transactions_graph_type, transactions_metric
):
    loyalty_cards_fig = px.scatter(x=[1, 2, 3], y=[2, 3, 4], title=f'Exploration Graph for Loyalty Cards ({loyalty_cards_metric})')
    payment_cards_fig = px.scatter(x=[1, 2, 3], y=[2, 4, 3], title=f'Exploration Graph for Payment Cards ({payment_cards_metric})')
    users_fig = px.scatter(x=[1, 2, 3], y=[3, 3, 2], title=f'Exploration Graph for Users ({users_metric})')
    transactions_fig = px.scatter(x=[1, 2, 3], y=[4, 2, 4], title=f'Exploration Graph for Transactions ({transactions_metric})')

    return (
        loyalty_cards_fig, payment_cards_fig,
        users_fig, transactions_fig
    )

if __name__ == '__main__':
    app.run_server(debug=True)
