import plotly.graph_objects as go

# Power sources is:
# [ { name: <name>, data: { <axis notch>: value, <axis_notch>: value }, color: <color> }, ...]
def get_plotly_stacked_power_figures(axis_notches, power_sources):
    out = []
    for power_source in power_sources:
        out.push(
            go.Scatter(
                name=power_sources['station_name'],
                x=axis_notches,
                y=[power_source['data'][n] for n in axis_notches],
                hoveron='points+fills',
                hoverinfo='text+x+y',
                mode='lines',
                line={'color': power_source['color']},
                stackgroup='one',
            )
        )

    return out
