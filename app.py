from typing import Dict, List
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import (
    Input,
    Output,
)

from sources import sheets_api
from utils import values_by_change_from_initial, interpolate, get_unit_or_false, remap_areas_data, remap_prices_data
from power_by_category import get_power_layout
from settings import app
from sources import sheets_api
from utils import (
    fix_values,
    get_unit_or_false,
    interpolate,
    values_by_change_from_initial,
)
from power_by_day import get_power_by_day_layout


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
    {'name': '2020 Price', 'id': '2020_price', 'editable': True},
    {'name': '2030 Change (%)', 'id': '2030_change_percantage', 'editable': True},
    {'name': '2040 Change (%)', 'id': '2040_change_percantage', 'editable': True},
    {'name': '2050 Change (%)', 'id': '2050_change_percantage', 'editable': True},
    {'name': 'show', 'id': 'show', 'editable': False},
    {'name': 'editable', 'id': 'editable', 'editable': False},
]


areas_columns = [
    {'id': 'category', 'name': 'Category'},
    {'id': 'capacity_2030', 'name': 'Capacity 2030'},
    {'id': 'capacity_2050', 'name': 'Capacity 2050'},
]


def get_cell_css_selector(columns: List[Dict], column_id: str):
    for index, column in enumerate(columns):
        if column['id'] == column_id:
            return f'td.dash-cell.column-{index}'
    raise Exception(f'Could not find column with id "{column_id}"')


def prices_editable_cells_css():
    global prices_columns

    css = []
    for column in prices_columns:
        if column['editable'] is True:
            css.append({
                'selector': get_cell_css_selector(columns=prices_columns, column_id=column['id']),
                'rule': 'background-color: #fff7f7',
            })
            css.append({
                'selector': get_cell_css_selector(columns=prices_columns, column_id=column['id']) + ':hover',
                'rule': 'cursor: pointer; outline: 1px solid hotpink;',
            })

    return css


areas_data = remap_areas_data(sheets_api.get_data_for_areas())
prices_data = remap_prices_data(sheets_api.get_data_for_prices())


style_cell_conditional = [
    {
        'if': {'column_id': c},
        'textAlign': 'left'
    } for c in ['category', 'sub_category', 'source', 'unit']
]


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
        sort_action="native",
        sort_mode="multi",
        row_selectable='multi',
        hidden_columns=['show', 'editable'],
        style_cell_conditional=style_cell_conditional,
        style_as_list_view=True,
        css=[
            {
                'selector': '.show-hide',
                'rule': 'display: none'
            },
        ] + prices_editable_cells_css()
    ),
])


# areas_layout = html.Div([
#     dash_table.DataTable(
#         id='production-areas-editable-table',
#         columns=areas_columns,
#         data=areas_data,
#         editable=True
#     ),
#     dbc.Row(
#         dbc.Col(
#             dbc.Container(
#                 dbc.Col(html.Div(id="tab-content"), width={"size": 6, "offset": 3}, )),
#             className='bg-light'
#         ),
#         id='graph-content'
#     ),
#     dbc.Row([
#         dbc.Col(html.Span(''), width=9),
#         dbc.Col(dcc.Link([html.I(className='fa fa-download'), ' Export to PDF'], href='#'), width=2),
#     ], id='footer', className='bg-white', justify='end')
# ], id='tab-body',
#     fluid=True,
#     className='bg-light p-0',
# )


areas_styled_dummy_layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Container(
                [
                    dbc.Col(html.H3('NZO2050'), width=12, className='bg-dark'),
                    dbc.Col(html.H5('Lorem ipsum dolor sit amet, consectetur adipiscing'), width=12,
                            className='bg-dark'),
                    dbc.Col(html.P(
                        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                        'Aenean euismod bibendum laoreet. Proin gravida dolor sit amet '
                        'lacus accumsan et viverra justo commodo. '
                    ), width=12)
                ], id='headers-container'
            ),
        ), className='text-primary bg-dark p-5', id='headers'),
    dbc.Row(
        dbc.Col(
            dbc.Container(
                dbc.Col(
                    dbc.Tabs(
                        [
                            dbc.Tab(label='2030', tab_id='2030'),
                            dbc.Tab(label='2050', tab_id='2050'),
                        ],
                        id='tabs'
                    ),
                    width=True,
                )
            ), className='bg-dark px-5'), id='graph-tabs'
    ),
    dbc.Row(
        dbc.Col(
            dbc.Container(
                dbc.Col(html.Div(id="tab-content"), width={"size": 6, "offset": 3}, )),
            className='bg-light'
        ),
        id='graph-content'
    ),
    dbc.Row([
        dbc.Col(html.Span(''), width=9),
        dbc.Col(dcc.Link([html.I(className='fa fa-download'), ' Export to PDF'], href='#'), width=2),
    ], id='footer', className='bg-white', justify='end')
], id='tab-body',
    fluid=True,
    className='bg-light p-0',
)


def get_areas_layout():
    areas_raw_values = sheets_api.get_data_for_areas()
    areas_fixed_values = fix_values(areas_raw_values)
    # todo: consider rewrite using: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/table/
    return html.Div([
        dash_table.DataTable(
            id='production-areas-editable-table',
            columns=areas_columns,
            data=[{'category': row['category'],
                   'capacity_2030': row['capacity_2030'],
                   'capacity_2050': row['capacity_2050'],
                   # 'percent_utilized': row['percent_utilized_2030']
                   }
                  for row
                  in areas_fixed_values.to_dict(orient='records')
                  ],
            editable=True
        ),
        dcc.Graph(id='production-areas-bar-chart', config={'editable': True})
    ])


@app.callback(Output('tab-content', 'children'), [Input("tabs", 'active_tab')])
def tab_content(active_tab):
    if active_tab == '2030':
        return html.Img(src='https://picsum.photos/id/100/200/300?grayscale')
    elif active_tab == '2050':
        return html.Img(src='https://picsum.photos/id/200/200/300?grayscale')
    else:
        return html.H3('Tab not found')


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
        return get_areas_layout()
    elif pathname == '/power':
        return get_power_layout()
    elif pathname == '/layout':
        # according to design: https://3judob.axshare.com/#id=qtqu20&p=2030_graph&g=1
        return areas_styled_dummy_layout
    elif pathname == '/power_by_day':
        return get_power_by_day_layout()
    else:
        return prices_layout


server = app.server

if __name__ == '__main__':
    app.run_server(
        # debug=True,
        # dev_tools_hot_reload=True,
    )
