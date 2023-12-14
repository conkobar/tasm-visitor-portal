#!/usr/bin/env python3
import dash
import plotly.express as px

from dash import html, dcc, callback, Output, Input
from datetime import date
from models import data


# register page
dash.register_page(__name__, '/')

layout = html.Div(
    [
        dcc.Graph(
            id='graph_content',
            style={'height': '700px',
                   'width': '1000px',
                   'align-self': 'center'}
            ),
            dcc.Interval(
                id='interval-component',
                interval=5*1000, # in milliseconds
                n_intervals=0
        )
    ],

    style={
    'display':'flex',
    'flex-direction':'column',
    'height': '1000px'
    }
)

@callback(
    Output("graph_content", "figure"),
    Input("interval-component", "n_intervals")
)
def update_map(n):
    fig = px.scatter_mapbox(
        data.zip_code_count(),
        lat="lat",
        lon="lng",
        color="counts",
        size="counts",
        color_continuous_scale=['#791b1e', '#d9232a', '#00a3da', '#3da447', '#263777'],
        size_max=50,
        zoom=10,
        hover_data=['zip', 'counts'],
        opacity=0.5
        )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig
