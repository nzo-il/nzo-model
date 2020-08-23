import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

from sources import sheets_api
from utils import values_by_change_from_initial, interpolate, get_unit_or_false, remap_areas_data, remap_prices_data
from settings import app


# prices_demo_state = [
#     {
#         'category': 'Coal',
#         'sub_category': 'CAPEX',
#         'source': 'Breyer',
#         'unit': 'ILS/kw',
#         '2020_price': 5856,
#         '2030_change_percantage': -45,
#         '2040_change_percantage': -55,
#         '2050_change_percantage': -60,
#     },
#     {
#         'category': 'CCGT',
#         'sub_category': 'CAPEX',
#         'source': 'Breyer',
#         'unit': 'ILS/kw',
#         '2020_price': 3025.9,
#         '2030_change_percantage': -45,
#         '2040_change_percantage': -55,
#         '2050_change_percantage': -60,
#     },
#     {
#         'category': 'Coal',
#         'sub_category': 'OPEX-var',
#         'source': 'Breyer',
#         'unit': 'ILS/kwh',
#         '2020_price': 15000,
#         '2030_change_percantage': -45,
#         '2040_change_percantage': -55,
#         '2050_change_percantage': -60,
#     }
# ]


prices_columns = [
    {'name': 'Category', 'id': 'category', 'editable': False},
    {'name': 'Sub Category', 'id': 'sub_category', 'editable': False},
    {'name': 'Source', 'id': 'source', 'editable': False},
    {'name': 'Unit', 'id': 'unit', 'editable': False},
    {'name': '2020 Price', 'id': '2020_price'},
    {'name': '2030 Change (%)', 'id': '2030_change_percantage'},
    {'name': '2040 Change (%)', 'id': '2040_change_percantage'},
    {'name': '2050 Change (%)', 'id': '2050_change_percantage'},
    {'name': 'show', 'id': 'show'},
    {'name': 'editable', 'id': 'editable'},
]


areas_columns = [
    {'id': 'category', 'name': 'Category'},
    {'id': 'capacity_2030', 'name': 'Capacity 2030'},
    {'id': 'capacity_2050', 'name': 'Capacity 2050'},
]


areas_data = remap_areas_data(sheets_api.get_data_for_areas())
prices_data = remap_prices_data(sheets_api.get_data_for_prices())


style_cell_conditional = [
    {
        'if': {'column_id': c},
        'textAlign': 'left'
    } for c in ['category', 'sub_category', 'source', 'unit']
]
style_cell_conditional.append({
    'if': {'column_editable': True},
    'background_color': 'lightgray'
})


prices_layout = html.Div([
    dcc.Graph(id='graph'),
    html.Div(
        id='table-error-message',
        children='',
        style={
            'marginTop': 25,
            'marginBottom': 40,
            'color': '#ce1919',
            'font': 'Ariel',
            'fontSize': 20,
        }
    ),
    dash_table.DataTable(
        id='prices-editable-data-table',
        columns=prices_columns,
        data=prices_data,
        editable=True,
        row_selectable='multi',
        hidden_columns=['show', 'editable'],
        style_cell_conditional=style_cell_conditional,
        style_as_list_view=True,
        css=[
            {
                "selector": ".show-hide",
                "rule": "display: none"
            },
            # {
            #     "selector": ".input-active.focused.dash-cell-value",
            #     "rule": "background-color: white"
            # }
        ]
    ),
])


areas_layout = html.Div([
    dash_table.DataTable(
        id='production-areas-editable-table',
        columns=areas_columns,
        data=areas_data,
        editable=True
    ),
    dcc.Graph(id='production-areas-bar-chart', config={'editable': True})
])


@app.callback(
    Output('production-areas-bar-chart', 'figure'),
    [
        Input('production-areas-editable-table', 'data'),
        Input('production-areas-editable-table', 'columns')
    ])
def render_areas_graph(rows, cols):
    df = pd.DataFrame(rows, columns=[c['id'] for c in cols])
    return {
        'layout': {
            'title': 'הספק עתידי לפי שטח',
            'xaxis': {'title': 'הספק, מגה-ווט'},
            'yaxis': {'title': 'סוג שטח'}
        },
        'data': [
            {
                'type': 'bar',
                'orientation': 'h',
                'y': df['category'],
                'x': df['capacity_2030'],
                'name': '2030'
            },
            {
                'type': 'bar',
                'orientation': 'h',
                'y': df['category'],
                'x': df['capacity_2050'],
                'name': '2050'

            }
        ]
    }


@app.callback(
    Output('prices-editable-data-table', 'selected_rows'),
    [
        Input('prices-editable-data-table', 'data'),
    ]
)
def prices_default_rows_selection(rows):
    default_indices = []
    for index, row in enumerate(rows):
        if row['category'].lower() == 'ccgt' or row['category'].lower() == 'solar-residential':
            if row['sub_category'].lower() == 'capex':
                default_indices.append(index)
    return default_indices


@app.callback(
    Output('table-error-message', 'children'),
    [
        Input('prices-editable-data-table', 'data'),
        Input('prices-editable-data-table', 'selected_rows'),
    ]
)
def prices_row_selection_error_message(rows, selected_rows_indices):
    if selected_rows_indices:
        rows = [rows[index] for index in selected_rows_indices]
        if get_unit_or_false(rows):
            return ''
        else:
            return 'Cannot show graph for different units'


@app.callback(
    Output('graph', 'figure'),
    [
        Input('prices-editable-data-table', 'data'),
        Input('prices-editable-data-table', 'selected_rows'),
    ]
)
def render_prices_graph(rows, selected_rows_indices):
    data = []
    layout = {
        'xaxis': {'title': 'Year', 'type': 'log'},
        'yaxis': {'title': 'Price'},
    }

    if selected_rows_indices:
        rows = [rows[index] for index in selected_rows_indices]
        unit = get_unit_or_false(rows)
        if unit:
            layout['yaxis']['title'] = unit
            for row in rows:
                change_by_year = [
                    (2030, row['2030_change_percantage']),
                    (2040, row['2040_change_percantage']),
                    (2050, row['2050_change_percantage']),
                ]

                clean_value = float(row['2020_price'].replace('%', ''))

                values = values_by_change_from_initial(
                    2020,
                    clean_value,
                    change_by_year
                )
                x, y = interpolate(values)
                line = {
                    'type': 'line',
                    'name': f'{row["sub_category"]} by {row["source"]}',
                    'x': x,
                    'y': y,
                }
                data.append(line)

    return {
        'data': data,
        'layout': layout,
    }


@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [
        dash.dependencies.Input('url', 'pathname')
    ]
)
def router(pathname):
    if pathname == '/prices':
        return prices_layout
    elif pathname == '/areas':
        return areas_layout
    else:
        return prices_layout


server = app.server

if __name__ == '__main__':
    app.run_server(
        # debug=True,
        # dev_tools_hot_reload=True,
    )
