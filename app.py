import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import snowflake.connector
import pandas as pd
import env
import query as q

app = dash.Dash(__name__)

cnn = snowflake.connector.connect(
    user=env.user,
    password=env.password,
    account=env.account,
    warehouse=env.warehouse,
    role = env.role
)

# Create connection with snowflake
def query_to_df(query):
    cs = cnn.cursor()
    sql = query
    cs.execute(sql)
    df = cs.fetch_pandas_all
    print('query executed...')
    print(query)
    print("output:"+df.head(1))
    cs.close()
    cnn.close()


# Sample data and graphs (replace with your own data)
# Sample data is provided just for demonstration purposes

# Sample data for graphs
class Graph:
    def __init__(self, key, display_name, header, description, graph_type, query):
        self.key = key
        self.display_name = display_name
        self.header = header
        self.description = description
        self.graph_type = graph_type #this will need working on to make it dynamic for now everyhting is bar
        self.query = query
        self.data = None
        self.output = None

    def create_graph_from_query(self):
        cs = cnn.cursor()
        sql = self.query
        cs.execute(sql)
        df = cs.fetch_pandas_all
        self.dataframe = df
        print('query executed...')
        print(sql)
        print("output:"+df.head(1))
        cs.close()
        cnn.close()

        if self.graph_type == "bar":
            self.output = dcc.Graph(
                id=self.key,
                figure=px.bar(x=df[0]), y=df[1], title=self.header
            )        


class Section:
    def __init__(self, key, display_name, header, description):
        self.key = key
        self.display_name = display_name
        self.header = header
        self.description = description
        self.graphs = []
        self.graph_displays = [graph.output for graph in self.graphs]

    def add_graph(self, graph):
        self.graphs.append(graph)

class Category:
    def __init__(self, key, display_name, header, description):
        self.key = key
        self.display_name = display_name
        self.header = header
        self.description = description
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

#Use pydantic models
class DataStructure: 
    def __init__(self):
        self.categories=[]

    def add_category(self, category):
        self.categories.append(category)

# Example usage
data_structure = DataStructure()

#Categories
overview = Category("overview", "Overview", "Overview", "Graphs displaying overview data.")
loyalty_cards = Category("loyalty_cards", "Loyalty Cards", "Loyalty Cards", "Graphs displaying loyalty card data.")

data_structure.add_category(loyalty_cards)

#sections
lc_overview = Section("lc_overview", "Loyalty Cards Overview", "Loyalty Cards Overview", "Generic graphs for loyalty cards")

overview.add_section(lc_overview)
loyalty_cards.add_section(lc_overview)

#graphs
lc_successful_joins_graph = Graph("lc_successful_joins_graph", "Successful Joins", "Successful Joins", "Successful Joins", "bar", q.sql_joins_daily)
lc_successful_links_graph = Graph("lc_successful_links_graph", "Successful Links", "Successful Links", "Successful Links", "bar", q.sql_links_daily)
lc_combined_joins_graph = Graph("lc_combined_joins_graph", "Combined Joins", "Combined Joins", "Combined Joins", "bar", q.sql_combine_lc_daily)

lc_overview.add_graph([lc_successful_joins_graph, lc_successful_links_graph, lc_combined_joins_graph])

print('hiiiiiiii')
def tabs_children():
    tabs = []
    for category in data_structure.categories:
       tabs.append(dcc.Tab(label=category.display_name, value=category.key))
    return tabs

# App layout
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='overview', children=tabs_children()),
    html.Div(id='page-content')
])

# Callback to update page content based on selected tab
@app.callback(Output('page-content', 'children'), [Input('tabs', 'value')])
def display_content(selected_tab):
    layout = []
    for category in data_structure.categories:
        if category.key == selected_tab:
            print(category.display_name)
            for section in category.sections:
                layout.append(
                    html.Div(
                        html.H1(category.display_name),
                        html.Div([
                            html.H2(section.display_name),
                            *section.graph_displays
                        ])
                    )
                )
                print(layout)
    return html.Div([layout])


if __name__ == '__main__':
    app.run_server(debug=True)
