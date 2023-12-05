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
        html.H1(children='TASM Data Dashboard'),

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

        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            id='visitor_count'
                            ),

                        dcc.Graph(
                            id='visitor_line_chart'
                            ),
                        ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'align-items': 'flex-start'
                        }
                    ),
                html.Div(
                    [
                        dcc.Graph(
                            id='visitor_bar_chart'
                            ),
                        ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'justify-content': 'flex-end',
                        'height': '100%'
                        }
                    )
                ],
            style={
                'display': 'flex',
                'flex-direction':'row',
                'width': '100%'
                }
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
    Output('visitor_count', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    data.start_date = start_date
    data.end_date = end_date
    data.filter_data()

    visitor_count_string = f'{data.total_visitors} total visitors in selected date range'

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
        return 'Select a date to see it displayed here', visitor_count_string
    else:
        return string_prefix, visitor_count_string

@callback(
    Output('my-date-picker-range', 'start_date'),
    Output('my-date-picker-range', 'end_date'),
    Input('reset', 'n_clicks')
)
def reset_dates(n_clicks):
    data.reset()
    return data.start_date, data.end_date

@callback(
    Output("visitor_line_chart", "figure"),
    Input("my-date-picker-range", "start_date"),
    Input('my-date-picker-range', 'end_date')
)
def update_visitor_line_chart(start_date, end_date):
    # set start and end dates
    data.start_date = start_date
    data.end_date = end_date
    data.filter_data()

    # show 14 day rolling average if date range allows
    window = 14 if data.date_range() >= 14 else None
    y = ['Daily Visitors', 'Visitors (Rolling)'] if window is not None else 'Daily Visitors'

    # create plot
    fig = px.line(
        data.daily_total_visitor_count(window),
        x='date',
        y=y,
        line_shape='spline',
        labels={'value': 'Visitors', 'date': 'Date'}
        )

    return fig

@callback(
    Output("visitor_bar_chart", "figure"),
    Input("my-date-picker-range", "start_date"),
    Input('my-date-picker-range', 'end_date')
)
def update_visitor_bar_chart(start_date, end_date):
    # set start and end dates
    data.start_date = start_date
    data.end_date = end_date
    data.filter_data()

    # create plot
    df = data.visitor_demographics()
    fig = px.bar(
        df,
        labels={'value': 'Num. Visitors', 'index': 'Category'},
        color=df.index
        )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
