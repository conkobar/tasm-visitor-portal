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
                html.Div('Download data in selected range:', style={'margin-right': '10px'}),
                html.Button("Download CSV", id="btn_csv", style={'margin-right': '10px'}),
                dcc.Download(id="download-dataframe-csv"),
            ],
            style={
                'display': 'flex',
                'flex-direction': 'row',
                'justify-content': 'flex-end'
                }
        ),

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
    vdff = data.filter_data(data.visitor_df, start_date, end_date)
    gdff = data.filter_data(data.group_df, start_date, end_date)

    visitor_count_string = f'{data.count_visitors(vdff) + data.count_visitors(gdff)} total visitors in selected date range'

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
    return data.start_date, data.end_date

@callback(
    Output("visitor_line_chart", "figure"),
    Input("my-date-picker-range", "start_date"),
    Input('my-date-picker-range', 'end_date')
)
def update_visitor_line_chart(start_date, end_date):
    vdff = data.filter_data(data.visitor_df, start_date, end_date)
    gdff = data.filter_data(data.group_df, start_date, end_date)

    # show 14 day rolling average if date range allows
    y =  ['Non-School Visitors', 'School Group Visitors']
    window = 14 if data.date_range() >= 60 else None
    if window is not None:
        y.append('Visitor Avg (2wks)')

    # create plot
    fig = px.line(
        data.daily_total_visitor_count(vdff, gdff, window),
        x='date',
        y=y,
        line_shape='spline',
        labels={'value': 'Num. Visitors', 'date': 'Date', 'variable': 'Visitor Type'},
        color_discrete_sequence=['#d9232a', '#00a3da', '#3da447', '#263777']
        )

    return fig

@callback(
    Output("visitor_bar_chart", "figure"),
    Input("my-date-picker-range", "start_date"),
    Input('my-date-picker-range', 'end_date')
)
def update_visitor_bar_chart(start_date, end_date):
    vdff = data.filter_data(data.visitor_df, start_date, end_date)
    gdff = data.filter_data(data.group_df, start_date, end_date)

    # create plot
    df = data.visitor_demographics(vdff, gdff).rename({
        'adults': "Adults (18-64)",
        'students': "Students (5-17)",
        'kids': "Children (0-4)",
        'seniors': 'Seniors (65+)'
        })
    fig = px.bar(
        df,
        labels={'value': 'Num. Visitors',
                'index': 'Category'
                },
        color=df.index,
        color_discrete_sequence=['#d9232a', '#00a3da', '#3da447', '#263777']
        )

    return fig

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    Input("my-date-picker-range", "start_date"),
    Input('my-date-picker-range', 'end_date'),
    prevent_initial_call=True,
)
def func(n_clicks, start_date, end_date):
    if n_clicks:
        vdff = data.filter_data(data.visitor_df, start_date, end_date)
        gdff = data.filter_data(data.group_df, start_date, end_date)
        
        df = vdff.merge(gdff, how='outer').sort_values('date').reset_index(drop=True)

        return dcc.send_data_frame(df.to_csv, "tasm_visitor_data(" + start_date + '_to_' + end_date + ").csv")
