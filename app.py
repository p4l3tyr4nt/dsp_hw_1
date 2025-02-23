from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    title='DSP HW1',
    prevent_initial_callbacks=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        page_container,
    ]
)

if __name__ == '__main__':
    app.run(debug=False)