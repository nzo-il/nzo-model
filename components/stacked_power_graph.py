import plotly.graph_objects as go

# Power sources is:
# [ { name: <name>, data: { <axis notch>: value, <axis_notch>: value }, color: <color> }, ...]

# Unstacked line is the same format
def get_plotly_stacked_power_figures(axis_notches, power_sources, unstacked_line):
    out = []
    for power_source in power_sources:
        out.append(
            go.Scatter(
                name=power_source['name'],
                x=axis_notches,
                y=[power_source['data'][n] for n in axis_notches],
                hoveron='points',
                hoverinfo='text+x+y',
                mode='lines',
                line={'color': power_source['color']},
                stackgroup='one',
            )
        )

    if unstacked_line is not None:
        out.append(
            go.Scatter(
                name=unstacked_line['name'],
                x=axis_notches,
                y=[unstacked_line['data'][n] for n in axis_notches],
                hoveron='points',
                hoverinfo='text+x+y',
                mode='lines',
                line={'color': unstacked_line['color']},
            )
        )

    return out
