import dash
import flask

server = flask.Flask(__name__)


@server.route("/")
def home():
    return "Hello, Flask!"


app = dash.Dash(server=server, routes_pathname_prefix="/dash/")

app.layout = dash.html.Div("This is the Dash app.")

if __name__ == "__main__":
    app.run_server(host="192.168.0.129", debug=True)