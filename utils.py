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
    units = set([row['unit'] for row in rows])
    if len(units) > 1:
        return False
    return list(units)[0]


def get_areas_fixed_values(_raw_values):
    # headers = [
    #     'קטגוריה',
    #     'SUM of SUM of סולארי מותקן עד 2030', 'SUM of SUM of שטח פנוי נותר ב-2030', 'סיכום שטח 2030',
    #     'סולארי מותקן עד 2050', 'SUM of SUM of שטח פנוי נותר ב-2050', 'סיכום שטח 2050', 'סה״כ הספק סולארי 2030',
    #     'סה״כ הספק סולארי 2050', 'SUM of SUM of התפלגות הספק סולארי 2030', 'SUM of SUM of התפלגותת הספק סולארי 2050']
    #
    # row_names = ['גגות', 'שדות קרקעיים', 'שטחים מבונים נוספים', 'מאגרי מים', 'חזיתות', 'כבישים', 'חניונים',
    #              'אזורי תעשיה',
    #              'אגריוולטאי']

    fixed_values = pd.DataFrame(_raw_values[1:], columns=_raw_values[0])
    fixed_values['category'] = fixed_values['קטגוריה']
    fixed_values['total_area_2030'] = (
        fixed_values['סיכום שטח 2030'].str.replace(',', '').astype(float))
    fixed_values['utilized_area_2030'] = (
        fixed_values['SUM of SUM of סולארי מותקן עד 2030'].str.replace(',', '').astype(float))
    fixed_values['percent_utilized_2030'] = (
        fixed_values['utilized_area_2030'] / fixed_values['total_area_2030'] * 100)
    fixed_values['capacity_2030'] = fixed_values['סה״כ הספק סולארי 2030']

    fixed_values['total_area_2050'] = fixed_values['סיכום שטח 2050'].str.replace(
        ',', '').astype(float)
    fixed_values['utilized_area_2050'] = fixed_values['סולארי מותקן עד 2050'].str.replace(',', '').astype(
        float)
    fixed_values['percent_utilized_2050'] = (
        fixed_values['utilized_area_2050'] / fixed_values['total_area_2050'] * 100)
    fixed_values['capacity_2050'] = fixed_values['סה״כ הספק סולארי 2050']

    return fixed_values
