""" server.py """

import os

import dash
import flask
import plotly.express as px
from dash.dependencies import Input, Output
from plot_dat import Dataset

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, routes_pathname_prefix="/dash/")
data = Dataset("./data/dat.csv")


app.layout = dash.html.Div([
    dash.html.H1("This is the Dash app."),

    dash.dcc.Graph(id="Humidity"),
    dash.dcc.Graph(id="Light"),
    
    dash.dcc.Interval(
        id='interval-component',
        interval=600 * 1000,  # in milliseconds
        n_intervals=0
    ),
    ])


# Define callbacks to update graphs
@app.callback(
    Output('Daily Humidity', 'figure'),
    Output('Daily Light', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graphs(n_intervals):
    # Update Humidity Plot
    humid_daily = data.plotToDH()

    # Update Light Plot
    light_daily = data.plotToDL()

    return humid_daily, light_daily

if __name__ == "__main__":
    app.run(host="192.168.0.129", debug=True, ssl_context='adhoc')
