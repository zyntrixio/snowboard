import dash
import dash_bootstrap_components as dbc

#https://www.bootstrapcdn.com/bootswatch/   ---- THIS IS A BOOTSTRAP STYLING PAGE
#https://hackerthemes.com/bootstrap-cheatsheet/  ---- THIS IS A BOOTSTRAP CHEATSHEET


# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
