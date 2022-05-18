import os

import dash_bootstrap_components as dbc

from dash import Dash, html, dcc
from utils import Plots

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = "Summer Olympics Dashboard"

plots = Plots()

app.layout = html.Div(children=[
    dcc.Graph(figure=plots.interactive_rating_map),
    html.Div([
        html.Div(dcc.Graph(figure=plots.medals_tally_between_genders), className="col-6"),
        html.Div(dcc.Graph(figure=plots.gender_ratio_in_disciplines), className="col-6")
    ], className="row"),
    html.Div([
        html.Div(dcc.Graph(figure=plots.top_countries_by_representative_count), className="col-6"),
        html.Div(dcc.Graph(figure=plots.top_disciplines_by_representative_count), className="col-6")
    ], className="row"),
    html.Div([
        html.Div(dcc.Graph(figure=plots.top_countries_by_total_medals_count), className="col-6"),
        html.Div(dcc.Graph(figure=plots.total_share_of_total_medals), className="col-6")
    ], className="row"),
    html.Div([
        html.Div(dcc.Graph(figure=plots.top_countries_by_gold_medals_count), className="col-6"),
        html.Div(dcc.Graph(figure=plots.total_share_of_gold_medals), className="col-6")
    ], className="row")
])


def main(debug):
    app.run_server(debug=debug)


if __name__ == '__main__':
    main(debug=('DEBUG' not in os.environ or os.environ['DEBUG'] == 'True'))
