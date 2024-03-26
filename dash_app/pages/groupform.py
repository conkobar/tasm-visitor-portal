#!/usr/bin/env python3
import dash
import dash_bootstrap_components as dbc

from dash import html, dcc, callback, Output, Input
from datetime import date
from models import data


dash.register_page(__name__, external_stylesheets=[dbc.themes.CERULEAN])

states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

layout = dbc.Container(
    [
        html.H1('TASM School Field Trip Entry Form', style={'margin-bottom': '20px'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3('Visit Date'),
                        dcc.DatePickerSingle(
                            id='input_date',
                            date=date.today(),
                            display_format='MM/DD/YYYY'
                        )
                    ],
                    style={'margin-bottom': '10px'}
                )
            ],
            style={'margin-bottom': '20px'}
        ),
        dbc.Row(
            dbc.Col([html.H3('School Information')]),
            style={'margin-bottom': '20px'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(
                            id='input_school_name',
                            type='text',
                            placeholder='School Name',
                            debounce=True,
                            required=True,
                            style={'margin-bottom': '10px'}
                        ),
                        dbc.Input(
                            id='input_leader_name',
                            type='text',
                            placeholder='Group Leader Name',
                            debounce=True,
                            required=True
                        )
                    ],
                    style={'margin-bottom': '10px'},
                    width=4
                )
            ],
            style={'margin-bottom': '20px'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(
                            id='input_school_address',
                            type='text',
                            placeholder='Address',
                            debounce=True,
                            required=True,
                            style={'margin-bottom': '10px'}
                        ),
                        dbc.Select(
                            id='input_school_state',
                            options=[{'label': state, 'value': state} for state in states],
                            value='OK',
                            placeholder='State'
                        )
                    ],
                    width=4
                ),
                dbc.Col(
                    [
                        dbc.Input(
                            id='input_school_city',
                            type='text',
                            placeholder='City',
                            debounce=True,
                            required=True,
                            style={'margin-bottom': '10px'}
                        ),
                        dbc.Input(
                            id='input_school_zip',
                            type='number',
                            placeholder='Zip Code',
                            min=10000,
                            max=99999,
                            step=1,
                            inputMode='numeric',
                            debounce=True,
                            required=True
                        )
                    ],
                    width=3
                )
            ],
            style={'margin-bottom': '20px'}
        ),
        dbc.Row(
            [
                html.H3('Participant Information')
            ],
            style={'margin-bottom': '20px'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Input(
                            id='input_adults',
                            type='number',
                            placeholder='Number of Adults',
                            min=1,
                            inputMode='numeric',
                            debounce=True,
                            required=True,
                            style={'margin-bottom': '10px'}
                        ),
                        dbc.Input(
                            id='input_students',
                            type='number',
                            placeholder='Number of Students',
                            min=1,
                            inputMode='numeric',
                            debounce=True,
                            required=True
                        )
                    ],
                    style={'margin-bottom': '10px'},
                    width=2
                ),
                dbc.Col(
                    [
                        dbc.Input(
                            id='input_boys',
                            type='number',
                            placeholder='Number of Boys',
                            min=0,
                            inputMode='numeric',
                            debounce=True,
                            style={'margin-bottom': '10px'}
                        ),
                        dbc.Input(
                            id='input_girls',
                            type='number',
                            placeholder='Number of Girls',
                            min=0,
                            inputMode='numeric',
                            debounce=True
                        )
                    ],
                    width=2
                )
            ],
            style={'margin-bottom': '20px'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Input(
                                    id=f'input_grade_{grade}',
                                    type='number',
                                    placeholder=f'Students in Grade {grade}',
                                    min=0,
                                    inputMode='numeric',
                                    debounce=True,
                                    style={'margin-bottom': '10px'}
                                )
                                for grade in range(1, 5)
                            ]
                        )
                    ],
                    width=2
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Input(
                                    id=f'input_grade_{grade}',
                                    type='number',
                                    placeholder=f'Students in Grade {grade}',
                                    min=0,
                                    inputMode='numeric',
                                    debounce=True,
                                    style={'margin-bottom': '10px'}
                                )
                                for grade in range(5, 9)
                            ]
                        )
                    ],
                    width=2
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Input(
                                    id=f'input_grade_{grade}',
                                    type='number',
                                    placeholder=f'Students in Grade {grade}',
                                    min=0,
                                    inputMode='numeric',
                                    debounce=True,
                                    style={'margin-bottom': '10px'}
                                )
                                for grade in range(9, 13)
                            ],
                        )
                    ],
                    width=2
                )
            ],
            style={'margin-bottom': '20px'}
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button('Submit', id='submit-val', n_clicks=0),
                        html.Div(id='error-message', style={'color': 'red'})
                    ]
                )
            ],
            style={'margin-bottom': '20px'}
        )
    ],
    fluid=True
)

# Callback to submit form data to firestore database
@callback(
    Output('submit-val', 'n_clicks'),
    Output('error-message', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('input_date', 'date'),
    Input('input_school_name', 'value'),
    Input('input_leader_name', 'value'),
    Input('input_school_address', 'value'),
    Input('input_school_city', 'value'),
    Input('input_school_state', 'value'),
    Input('input_school_zip', 'value'),
    Input('input_adults', 'value'),
    Input('input_students', 'value'),
    Input('input_boys', 'value'),
    Input('input_girls', 'value'),
    Input('input_grade_1', 'value'),
    Input('input_grade_2', 'value'),
    Input('input_grade_3', 'value'),
    Input('input_grade_4', 'value'),
    Input('input_grade_5', 'value'),
    Input('input_grade_6', 'value'),
    Input('input_grade_7', 'value'),
    Input('input_grade_8', 'value'),
    Input('input_grade_9', 'value'),
    Input('input_grade_10', 'value'),
    Input('input_grade_11', 'value'),
    Input('input_grade_12', 'value')
)
def submit_form(n_clicks, date, school_name, leader_name, school_address, school_city, school_state, school_zip, adults, students, boys, girls, *grades):
    if n_clicks:
        # check for empty fields
        if not school_name:
            return 0, 'School name is required'
        if not leader_name:
            return 0, 'Group leader name is required'
        if not school_address:
            return 0, 'School address is required'
        if not school_city:
            return 0, 'School city is required'
        if not school_zip:
            return 0, 'School zip code is required'
        if not adults:
            return 0, 'Number of adults must be greater than 0!'
        if not students:
            return 0, 'Number of students must be greater than 0!'

        # set empty fields to 0
        if not boys:
            boys = 0
        if not girls:
            girls = 0
        grades = [int(grade) if grade else 0 for grade in grades]

        # create dictionary of form data
        form_data = {
            'date': date,
            'name': school_name,
            'leader_name': leader_name,
            'address': school_address,
            'city': school_city,
            'state': school_state,
            'zip': school_zip,
            'adults': adults,
            'students': students,
            'boys': boys,
            'girls': girls,
            'first_grade': grades[0],
            'second_grade': grades[1],
            'third_grade': grades[2],
            'fourth_grade': grades[3],
            'fifth_grade': grades[4],
            'sixth_grade': grades[5],
            'seventh_grade': grades[6],
            'eighth_grade': grades[7],
            'ninth_grade': grades[8],
            'tenth_grade': grades[9],
            'eleventh_grade': grades[10],
            'twelfth_grade': grades[11]
        }

        # send form data to firestore database
        message = data.send_to_firestore(form_data, 'groups')

        return 0, message

    return 0, None
