""" server.py """

import datetime
import os

import dash
import flask
import plotly.express as px
from dash.dependencies import Input, Output
from plot_dat import Dataset

server = flask.Flask(__name__, static_folder="static")
app = dash.Dash(__name__, server=server)#, routes_pathname_prefix="/dash/")
data = Dataset("./data/dat.csv")


app.layout = dash.html.Div([
    dash.html.H1("This is the Dash app."),

    dash.html.Video(
        controls=True,
        id = "movie_player",
        src = dash.get_asset_url("static/time-lapse.mp4"),
        autoPlay=True
    ),

    dash.dcc.Graph(id="Humidity vs Light"),
    dash.dcc.Graph(id="Daily Humidity"),
    dash.dcc.Graph(id="Daily Light"),
    dash.dcc.Graph(id="Light"),
    dash.dcc.Graph(id="Water"),
    dash.dcc.Graph(id="Temperature"),

    dash.dcc.Interval(
        id='interval-component',
        interval=600 * 1000,  # in milliseconds
        n_intervals=0
    ),
])


# Define callbacks to update graphs
@app.callback(
    Output("Humidity vs Light", 'figure'),
    Output('Daily Humidity', 'figure'),
    Output('Daily Light', 'figure'),
    Output('Light', 'figure'),
    Output('Water', 'figure'),
    Output('Temperature', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graphs(n_intervals):
    print(f"{datetime.datetime.now()} |\tUpdating...")
    humid_light = data.plotHL()
    humid_daily = data.plotToDH()
    light_daily = data.plotToDL()

    light = data.plotL()
    water = data.plotW()
    temp = data.plotT()

    return humid_light, humid_daily, light_daily, light, water, temp

if __name__ == "__main__":
    app.run(host="192.168.0.129", debug=True, ssl_context='adhoc')
