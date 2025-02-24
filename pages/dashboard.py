import dash
import dash_player
import base64
from dash import Dash, html, dcc, callback, ctx, Output, Input, State, ALL, no_update
import dash_bootstrap_components as dbc

from dtmf import get_signal

dash.register_page(__name__, path='/')

def layout():
    return index()

def index():

    mode_choice_btn = html.Div(children=[
        html.H4('Sample rate kHz'),
        dcc.Slider(id='sample-rate-input', min=2, max=20, step=2, value=10),
        html.H4('Mode choice'),
        dcc.RadioItems(
            options=['Single', 'Multiple'],
            value='Single',
            id='mode-choice',
            className='mode-choice'
        ),
    ])

    number_info = html.Div(id='number-info', children=
        [
            html.H4('Number: '),
            html.H5('', id='number'),
            html.Div(children=
                [
                    dbc.Button('Call', id='btn-call', color='success', n_clicks=0, className='input-btn'),
                ]),
        ],
        className='hidden',
    )
    
    player = html.Audio(id='audio-player', src='', controls=True, autoPlay=True, className='player')

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
            player,
            input_menu,
        ],
        className='sidenav text-white'
    )

    graph = dcc.Graph(id='graph-content')

    return html.Div(
        [
            side_menu_form,
            graph,
        ],
        className=__name__)

@callback(
    [
        Output('number', 'children', allow_duplicate=True),
        Output('graph-content', 'figure'),
        Output('audio-player', 'src', allow_duplicate=True),
    ],
    Input({'type': 'btn', 'index': ALL}, 'n_clicks'),
    [
        State('mode-choice', 'value'),
        State('sample-rate-input', 'value'),
        State('number', 'children'),
    ],
    prevent_initial_call=True,
)
def num_click(_, mode, sample_rate_kHz, number):

    btn_index = eval(ctx.triggered[0]['prop_id'].split('.')[0])['index']

    if mode == 'Single':

        signal = get_signal(btn_index, sample_rate_kHz)

        signal.generate_audio(sample_rate_kHz)

        encoded_sound = base64.b64encode(open('audio/dtmf.wav', 'rb').read())
        src = 'data:audio/wav;base64,{}'.format(encoded_sound.decode())

        return '', signal.get_graph(), src
    
    elif mode == 'Multiple':

        return number + btn_index, no_update, no_update

    return no_update, no_update, no_update

@callback(
    Output('audio-player', 'src', allow_duplicate=True),
    Input('btn-call', 'n_clicks'),
    State('sample-rate-input', 'value'),
    prevent_initial_call=True,
)
def call_click(_, sample_rate_kHz):

    pass

@callback(
    [
        Output('number-info', 'className'),
        Output('number', 'children', allow_duplicate=True),
    ],
    Input('mode-choice', 'value'),
    prevent_initial_call=True,
)
def mode_choice(mode):

    if mode == 'Single':

        return 'hidden', ''
    
    if mode == 'Multiple':

        return 'visible', no_update
    
    return no_update, no_update