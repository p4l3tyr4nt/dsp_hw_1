import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

def layout():
    return index()

def index():

    mode_choice_btn = html.Div(children=[
        dbc.Label("Sample rate kHz", html_for="sample-rate-slider"),
        dcc.Slider(id="sample-rate-input", min=2, max=10, step=1, value=10),
        html.H4("Mode choice"),
        dcc.RadioItems(
            options=["Single", "Multi"],
            value="Single",
            id="mode-choice",
            className="mode-choice"
        ),
    ])

    number_info = html.Div(children=
        [
            dbc.Label("Number: -"),
            html.Div(children=
                [
                    dbc.Button("Call", id='btn-call', color='success', n_clicks=0, className='input-btn'),
                ]),
        ],
        className='number-info hidden',
        )

    input_menu =  html.Div(
        [
            dbc.Button(
                symbol,
                id='btn' + symbol,
                color="success",
                n_clicks=0,
                className='input-btn'
            ) for symbol in '123456789*0#'
        ],
        className="input-menu",
    )

    side_menu_form = html.Div(
        [
            mode_choice_btn,
            number_info,
            input_menu,
        ],
        className="sidenav text-white"
    )

    graph = dcc.Graph(id='graph-content', config={'displayModeBar': False})

    return html.Div(
        [
            side_menu_form,
            graph,
        ],
        className=__name__)