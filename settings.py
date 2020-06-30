import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

server = flask.Flask(__name__)

app = dash.Dash(__name__, suppress_callback_exceptions=True, server=server)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
