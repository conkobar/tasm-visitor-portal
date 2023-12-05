#!/usr/bin/env python3
from dash import Dash, html, dcc, callback, Output, Input
from models.data_handler import DataHandler
from datetime import date

import plotly.express as px


# import data
data = DataHandler('dash_app/data/fake_data.csv')

# Create Dash app
app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(children='TASM Visitors'),

        dcc.DatePickerRange(
            id='my-date-picker-range',
            start_date=data.start_date,
            end_date=data.end_date
            ),

        html.Button(
            'Reset Dates',
            id='reset',
            type='text',
            n_clicks=0,
            style={'width':'100px'}
            ),

        html.Div(id='output-container-date-picker-range'),

        dcc.Graph(
            id='graph_content',
            style={'height': '700px',
                   'width': '1000px',
                   'align-self': 'center'}
            )
    ],

    style={
    'display':'flex',
    'flex-direction':'column',
    'height': '1000px'
    }
)

@callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

@callback(
    Output("graph_content", "figure"),
    Input("my-date-picker-range", "start_date"),
    Input('my-date-picker-range', 'end_date')
)
def update_map(start_date, end_date):
    data.start_date = start_date
    data.end_date = end_date
    data.filter_data()

    fig = px.scatter_mapbox(
        data.zip_code_count(),
        lat="lat",
        lon="lng",
        color="counts",
        size="counts",
        color_continuous_scale=px.colors.sequential.Teal,
        size_max=50,
        zoom=10,
        hover_data=['zipCode', 'counts']
        )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

@callback(
    Output('my-date-picker-range', 'start_date'),
    Output('my-date-picker-range', 'end_date'),
    Input('reset', 'n_clicks')
)
def reset_dates(n_clicks):
    data.reset()
    return data.start_date, data.end_date
    

if __name__ == '__main__':
    app.run(debug=True)
