import pandas as pd


def values_by_change_from_initial(initial_x, initial_y, changes: list):
    assert initial_x < changes[0][0]
    result = [(initial_x, initial_y)]
    while changes:
        x, y_percentage = changes.pop(0)
        y_change = y_percentage / 100 + 1
        y = initial_y * y_change
        result.append((x, y))
    return result


def interpolate(vectors):
    # interpolate y by x, and return two arrays
    # TODO: This doesn't calculate right.
    x_result = []
    y_result = []
    for i in range(len(vectors)):
        try:
            x = vectors[i][0]
            y = vectors[i][1]
            next_x = vectors[i + 1][0]
            next_y = vectors[i + 1][1]
        except IndexError:
            continue
        x_diff = next_x - x
        y_diff = next_y - y
        interval = y_diff / x_diff
        for j in range(0, x_diff):
            x_result.append(x + j)
            y_result.append(y + (interval * abs(j)))
    return x_result, y_result


def get_unit_or_false(rows):
    # Get the unit (string) for the selected rows, and return False if there are multiple units selected.
    # We can't do anything with multiple units.
    units = set([row['unit'].lower() for row in rows])
    if len(units) > 1:
        return False
    return list(units)[0]


def remap_areas_data(raw_values):
    # headers = [
    #     'קטגוריה',
    #     'SUM of SUM of סולארי מותקן עד 2030', 'SUM of SUM of שטח פנוי נותר ב-2030', 'סיכום שטח 2030',
    #     'סולארי מותקן עד 2050', 'SUM of SUM of שטח פנוי נותר ב-2050', 'סיכום שטח 2050', 'סה״כ הספק סולארי 2030',
    #     'סה״כ הספק סולארי 2050', 'SUM of SUM of התפלגות הספק סולארי 2030', 'SUM of SUM of התפלגותת הספק סולארי 2050']
    #
    # row_names = ['גגות', 'שדות קרקעיים', 'שטחים מבונים נוספים', 'מאגרי מים', 'חזיתות', 'כבישים', 'חניונים',
    #              'אזורי תעשיה',
    #              'אגריוולטאי']

    mapped_values = pd.DataFrame(raw_values[1:], columns=raw_values[0])
    mapped_values['category'] = mapped_values['קטגוריה']
    mapped_values['total_area_2030'] = (
        mapped_values['סיכום שטח 2030'].str.replace(',', '').astype(float))
    mapped_values['utilized_area_2030'] = (
        mapped_values['SUM of SUM of סולארי מותקן עד 2030'].str.replace(',', '').astype(float))
    mapped_values['percent_utilized_2030'] = (
        mapped_values['utilized_area_2030'] / mapped_values['total_area_2030'] * 100)
    mapped_values['capacity_2030'] = mapped_values['סה״כ הספק סולארי 2030']

    mapped_values['total_area_2050'] = mapped_values['סיכום שטח 2050'].str.replace(
        ',', '').astype(float)
    mapped_values['utilized_area_2050'] = mapped_values['סולארי מותקן עד 2050'].str.replace(',', '').astype(
        float)
    mapped_values['percent_utilized_2050'] = (
        mapped_values['utilized_area_2050'] / mapped_values['total_area_2050'] * 100)
    mapped_values['capacity_2050'] = mapped_values['סה״כ הספק סולארי 2050']

    return [
        {
            'category': row['category'],
            'capacity_2030': row['capacity_2030'],
            'capacity_2050': row['capacity_2050']
        }
        for row in mapped_values.to_dict(orient='records')
    ]


def to_float_or_none(value):
    if (value == ''):
        return None
    else:
        return float(value)


def remap_prices_data(raw_values):
    columns_to_drop = ['2030', '2040', '2050']
    mapping = {
        'Category': 'category',
        'Sub Category': 'sub_category',
        'Source': 'source',
        'Unit': 'unit',
        '2020 Price': '2020_price',
        '2030 Change (%)': '2030_change_percantage',
        '2040 Change (%)': '2040_change_percantage',
        '2050 Change (%)': '2050_change_percantage',
        'show': 'show',
        'editable': 'editable',
    }

    mapped_values = pd.DataFrame(raw_values[1:], columns=raw_values[0])
    mapped_values.rename(columns=mapping, inplace=True)
    mapped_values.drop(columns=columns_to_drop, inplace=True)
    mapped_values['2030_change_percantage'] = mapped_values['2030_change_percantage'].str.replace(
        '%', '').map(to_float_or_none)
    mapped_values['2040_change_percantage'] = mapped_values['2040_change_percantage'].str.replace(
        '%', '').map(to_float_or_none)
    mapped_values['2050_change_percantage'] = mapped_values['2050_change_percantage'].str.replace(
        '%', '').map(to_float_or_none)

    mapped_values['show'] = mapped_values['show'].str.replace(
        'NO', '').astype(bool)
    mapped_values['editable'] = mapped_values['editable'].str.replace(
        'NO', '').astype(bool)

    data = [
        {
            column_key: row[column_key]
            for column_key in mapped_values.columns
        }
        for row in mapped_values.to_dict(orient='records')
    ]
    return data
