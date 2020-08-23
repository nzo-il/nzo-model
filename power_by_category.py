import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


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
CATEGORY_COLORS = {
    "Coal": 'black',
    "Solar": 'yellow',
    "Hydro": 'blue',
    "Green": 'green',
}

def get_trace(item):
    start_year = item.get("starting_year", YEARS[0])
    close_year = item.get("closing_year", YEARS[-1])
    values = [item["annual_output"] if start_year == YEARS[0] else 0]
    for index, year in enumerate(YEARS[1:]):
        value = 0
        if year == start_year:
            value = item["annual_output"]
        elif start_year < year <= close_year:
            value = values[index] * (1 - item.get("yearly_degradation", 0))
        values.append(value)

    return go.Scatter(
        name=item["station_name"],
        x=YEARS,
        y=values,
        hoveron='points+fills',
        hoverinfo='x+y',
        mode='lines',
        line={"color": CATEGORY_COLORS[item["category"]]},
        stackgroup='one'  # define stack group
    )



def get_power_layout():
    fig = go.Figure()
    for item in POWER_DATA:
        fig.add_trace(get_trace(item))

    return html.Div([
        dcc.Graph(figure=fig),
    ])
