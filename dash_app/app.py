#!/usr/bin/env python3
import dash
import dash_auth
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output


# VALID_USERNAME_PASSWORD_PAIRS = {
#     'hello': 'world'
# }

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CERULEAN])
# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

# Expose Flask instance
server = app.server

app.layout = html.Div(
    [
    dash.page_container,
    # add a logout for the authenticated user
    dbc.Button("Logout", id="logout-button", n_clicks=0)
    ],
    style={'margin': '20px'}
    )

if __name__ == '__main__':
    app.run(debug=True)
