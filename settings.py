import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask

CSS_FONT_AWESOME_MIN_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'

server = flask.Flask(__name__)
external_stylesheets = [
    dbc.themes.FLATLY,
    CSS_FONT_AWESOME_MIN_CSS
]

app = dash.Dash(__name__, suppress_callback_exceptions=True, server=server, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
