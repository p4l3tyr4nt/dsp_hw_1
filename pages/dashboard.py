import dash
from dash import Dash, html, dcc, callback, ctx, Output, Input, State, ALL, no_update
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

def layout():
    return index()

def index():

    mode_choice_btn = html.Div(children=[
        dbc.Label('Sample rate kHz', html_for='sample-rate-slider'),
        dcc.Slider(id='sample-rate-input', min=2, max=10, step=1, value=10),
        html.H4('Mode choice'),
        dcc.RadioItems(
            options=['Single', 'Multi'],
            value='Single',
            id='mode-choice',
            className='mode-choice'
        ),
    ])

    number_info = html.Div(id='number-info', children=
        [
            dbc.Label('Number: '),
            html.Div('', id='number'),
            html.Div(children=
                [
                    dbc.Button('Call', id='btn-call', color='success', n_clicks=0, className='input-btn'),
                ]),
        ],
        className='number-info hidden',
        )

    input_menu =  html.Div(
        [
            dbc.Button(
                symbol,
                id={'type': 'btn', 'index': symbol},
                color='success',
                n_clicks=0,
                className='input-btn'
            ) for symbol in '123456789*0#'
        ],
        className='input-menu',
    )

    side_menu_form = html.Div(
        [
            mode_choice_btn,
            number_info,
            input_menu,
        ],
        className='sidenav text-white'
    )

    graph = dcc.Graph(id='graph-content', config={'displayModeBar': False})

    return html.Div(
        [
            side_menu_form,
            graph,
        ],
        className=__name__)

@callback(
    Output('number', 'children'),
    Output('graph-content', 'figure'),
    Input({'type': 'btn', 'index': ALL}, 'n_clicks'),
    State('mode-choice', 'value'),
    State('sample-rate-input', 'value'),
    prevent_initial_call=True,
)
def num_click(_, mode, sample_rate):

    btn_index = eval(ctx.triggered[0]['prop_id'].split('.')[0])['index']

    return no_update, no_update

@callback(
    Input('btn-call', 'n_clicks'),
    State('sample-rate-input', 'value'),
    prevent_initial_call=True,
)
def call_click(_, sample_rate):
    pass

@callback(
    Output('number-info', 'className'),
    Input('mode-choice', 'value'),
    prevent_initial_call=True,
)
def mode_choice(mode):
    if mode == 'Single':
        return 'number-info hidden'
    elif mode == 'Multi':
        return 'number-info'
    return no_update