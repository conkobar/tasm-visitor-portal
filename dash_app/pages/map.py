#!/usr/bin/env python3
import dash
import plotly.express as px

from dash import html, dcc, callback, Output, Input
from datetime import date
from models import data


# register page
dash.register_page(__name__)

layout = html.Div(
    [
        dcc.DatePickerRange(
            id='map-date-picker-range',
            start_date=data.start_date,
            end_date=data.end_date
            ),
        html.H2(id='map_visitor_count'),
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
    Input("interval-component", "n_intervals"),
    Input('map-date-picker-range', 'start_date'),
    Input('map-date-picker-range', 'end_date')
)
def update_map(n, start_date, end_date):
    vdff = data.filter_data(data.visitor_df, start_date, end_date)
    gdff = data.filter_data(data.group_df, start_date, end_date)

    fig = px.scatter_mapbox(
        data.zip_code_count(vdff, gdff),
        lat="lat",
        lon="lng",
        color="counts",
        size="counts",
        color_continuous_scale=['#791b1e', '#d9232a', '#00a3da', '#3da447', '#263777'],
        size_max=50,
        zoom=10,
        hover_data=['zip', 'counts'],
        opacity=0.5,
        center={'lat': 36.1540, 'lon': -95.937332}
        )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

@callback(
    Output('map_visitor_count', 'children'),
    Input('map-date-picker-range', 'start_date'),
    Input('map-date-picker-range', 'end_date'),
    Input("interval-component", "n_intervals"))
def update_map(start_date, end_date, n):
    vdff = data.filter_data(data.visitor_df, start_date, end_date)
    gdff = data.filter_data(data.group_df, start_date, end_date)

    visitor_count_string = f'{data.count_visitors(vdff) + data.count_visitors(gdff)} total visitors in selected date range'

    return visitor_count_string
