import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import (
    Input,
    Output,
)

from sources import sheets_api

app = dash.Dash(__name__)


def fix_values(_raw_values):
    # headers = [
    #     'קטגוריה',
    #     'SUM of SUM of סולארי מותקן עד 2030', 'SUM of SUM of שטח פנוי נותר ב-2030', 'סיכום שטח 2030',
    #     'סולארי מותקן עד 2050', 'SUM of SUM of שטח פנוי נותר ב-2050', 'סיכום שטח 2050', 'סה״כ הספק סולארי 2030',
    #     'סה״כ הספק סולארי 2050', 'SUM of SUM of התפלגות הספק סולארי 2030', 'SUM of SUM of התפלגותת הספק סולארי 2050']
    #
    # row_names = ['גגות', 'שדות קרקעיים', 'שטחים מבונים נוספים', 'מאגרי מים', 'חזיתות', 'כבישים', 'חניונים',
    #              'אזורי תעשיה',
    #              'אגריוולטאי']

    _fixed_values = pd.DataFrame(_raw_values[1:], columns=_raw_values[0])
    _fixed_values['category'] = _fixed_values['קטגוריה']
    _fixed_values['total_area_2030'] = (_fixed_values['סיכום שטח 2030'].str.replace(',', '').astype(float))
    _fixed_values['utilized_area_2030'] = (
        _fixed_values['SUM of SUM of סולארי מותקן עד 2030'].str.replace(',', '').astype(float))
    _fixed_values['percent_utilized_2030'] = (
            _fixed_values['utilized_area_2030'] / _fixed_values['total_area_2030'] * 100)
    _fixed_values['capacity_2030'] = _fixed_values['סה״כ הספק סולארי 2030']

    _fixed_values['total_area_2050'] = _fixed_values['סיכום שטח 2050'].str.replace(',', '').astype(float)
    _fixed_values['utilized_area_2050'] = _fixed_values['סולארי מותקן עד 2050'].str.replace(',', '').astype(
        float)
    _fixed_values['percent_utilized_2050'] = (
            _fixed_values['utilized_area_2050'] / _fixed_values['total_area_2050'] * 100)
    _fixed_values['capacity_2050'] = _fixed_values['סה״כ הספק סולארי 2050']

    return _fixed_values


raw_values = sheets_api.get_data_for_areas()

fixed_values = fix_values(raw_values)

columns = [
    {'id': 'category', 'name': 'Category'},
    {'id': 'capacity_2030', 'name': 'Capacity 2030'},
    {'id': 'capacity_2050', 'name': 'Capacity 2050'},
]

app.layout = html.Div([
    dash_table.DataTable(
        id='table-editing-simple',
        columns=columns,
        data=[{'category': row['category'],
               'capacity_2030': row['capacity_2030'],
               'capacity_2050': row['capacity_2050'],
               # 'percent_utilized': row['percent_utilized_2030']
               }
              for row
              in fixed_values.to_dict(orient='records')
              ],
        editable=True
    ),
    dcc.Graph(id='table-editing-simple-output')
])


@app.callback(
    Output('table-editing-simple-output', 'figure'),
    [
        Input('table-editing-simple', 'data'),
        Input('table-editing-simple', 'columns')
    ])
def display_output(rows, cols):
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


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
