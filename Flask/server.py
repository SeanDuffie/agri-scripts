import dash
import flask
import os

server = flask.Flask(__name__)


@server.route("/")
def home():
    print(os.getcwd())
    return flask.render_template("home.html")

@server.route("/stats")
def stats():
    return flask.render_template("stats.html")


app = dash.Dash(server=server, routes_pathname_prefix="/dash/")

app.layout = dash.html.Div("This is the Dash app.")

if __name__ == "__main__":
    app.run_server(host="192.168.0.129", debug=True)