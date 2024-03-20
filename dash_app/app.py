#!/usr/bin/env python3
import dash
from dash import Dash, html


app = Dash(__name__, use_pages=True)

# Expose Flask instance
server = app.server

app.layout = html.Div([
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)
