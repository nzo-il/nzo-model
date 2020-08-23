import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

from components.stacked_power_graph import get_plotly_stacked_power_figures
from settings import app
import dash
import json

POWER_COLUMNS = [
    {'name': 'Station Name', 'id': 'station_name'},
    {'name': 'Category', 'id': 'category'},
    {'name': 'Annual Power Output', 'id': 'annual_output'},
    {'name': 'Planned Closing Year', 'id': 'closing_year'},
]

POWER_DATA = [
    {
        "station_name": "Rabin",
        "category": "Coal",
        "annual_output": 50,
        "closing_year": 2030,
    },
    {
        "station_name": "Hovav",
        "category": "Coal",
        "annual_output": 100,
        "closing_year": 2040,
    },
    {
        "station_name": "Reading",
        "category": "Coal",
        "annual_output": 10,
        "closing_year": 2025,
    },
    {
        "station_name": "Tveria",
        "category": "Coal",
        "annual_output": 30,
        "closing_year": 2034,
    },
    {
        "station_name": "Ashalim",
        "category": "Solar",
        "annual_output": 20,
        "starting_year": 2032,
    },
    {
        "station_name": "Ktora Sun 1",
        "category": "Green",
        "annual_output": 100,
        "yearly_degradation": 0.1,
        "starting_year": 2040,
    },
    {
        "station_name": "Ktora Sun 2",
        "category": "Solar",
        "annual_output": 70,
        "yearly_degradation": 0.006,
        "starting_year": 2028,
    },
    {
        "station_name": "Eshkol",
        "category": "Hydro",
        "annual_output": 70,
        "starting_year": 2034,
    },
]

YEARS = [year for year in range(2020, 2051)]

EXTRA_LINE = {
    'name': 'extra-line',
    'data': {year: (year-2020)*10 for year in YEARS},
    'color': 'red',
}

CATEGORY_COLORS = {
    "Coal": 'black',
    "Solar": 'yellow',
    "Hydro": 'blue',
    "Green": 'green',
}

def get_power_source_data(item):
    start_year = item.get("starting_year", YEARS[0])
    close_year = item.get("closing_year", YEARS[-1])

    values = {}
    values[YEARS[0]] = item['annual_output'] if start_year == YEARS[0] else 0

    for index, year in enumerate(YEARS[1:]):
        value = 0
        if year == start_year:
            value = item["annual_output"]
        elif start_year < year <= close_year:
            value = values[YEARS[index]] * (1 - item.get("yearly_degradation", 0))

        values[year] = value

    return {
        'name': item['station_name'],
        'color': CATEGORY_COLORS[item["category"]],
        'data': values
    }

@app.callback(
    dash.dependencies.Output('redirect-hidden-div', 'children'),
    [dash.dependencies.Input('g1', 'clickData')]
)
def point_clicked(clickData):
    if clickData is not None:
        return dcc.Location(pathname='/power_by_day5', id='whatever')

    raise PreventUpdate()


def get_power_by_day_layout():
    fig = go.Figure()
    fig.layout.hovermode = 'x'

    power_sources = []
    for item in POWER_DATA:
        power_sources.append(get_power_source_data(item))

    traces = get_plotly_stacked_power_figures(YEARS, power_sources, EXTRA_LINE)

    for t in traces:
        fig.add_trace(t)

    return html.Div([
        dcc.Graph(id='g1', figure=fig),
        "gi",
        html.Div(id='redirect-hidden-div'),
    ])
