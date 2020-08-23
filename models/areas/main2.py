import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.graph_objects as go

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

    _fixed_values['total_area_2050'] = _fixed_values['סיכום שטח 2050'].str.replace(',', '').astype(float)
    _fixed_values['utilized_area_2050'] = _fixed_values['סולארי מותקן עד 2050'].str.replace(',', '').astype(
        float)
    _fixed_values['percent_utilized_2050'] = (
            _fixed_values['utilized_area_2050'] / _fixed_values['total_area_2050'] * 100)

    return _fixed_values


raw_values = sheets_api.get_data_for_areas()

fixed_values = fix_values(raw_values)

columns = [
    {'id': 'category', 'name': 'Category'},
    {'id': 'area_2030', 'name': 'Area 2030'},
    {'id': 'area_2050', 'name': 'Area 2050'},
    {'id': 'percent_utilized', 'name': '% Utilized'},
]

app.layout = html.Div([
    dash_table.DataTable(
        id='table-editing-simple',
        columns=columns,
        data=[{'category': row['category'],
               'area_2030': row['total_area_2030'],
               'area_2050': row['total_area_2050'],
               # 'percent_utilized': row['percent_utilized_2030']
               }
              for row
              in fixed_values.to_dict(orient='records')
              ],
        editable=True
    ),
    dcc.Graph(id='sankey')
])


@app.callback(
    Output('sankey', 'figure'),
    [
        Input('table-editing-simple', 'data'),
        Input('table-editing-simple', 'columns')
    ])
def display_output(rows, cols):
    df = pd.DataFrame(rows, columns=[c['id'] for c in cols])

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=["A1", "A2", "B1", "B2", "C1", "C2"],
            color="blue"
        ),
        link=dict(
            source=[0, 1, 0, 2, 3, 3],  # indices correspond to labels, eg A1, A2, A2, B1, ...
            target=[2, 3, 3, 4, 4, 5],
            value=[8, 4, 2, 8, 4, 2]
        ))])

    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
