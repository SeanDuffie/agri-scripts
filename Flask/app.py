""" @file app.py
    @author Sean Duffie
    @brief Flask Framework for webserver to be run on RPi
    
    This website will allow the user to view data collected from the Sensors and Camera
"""
from flask import Flask, render_template, send_from_directory, url_for, redirect, request

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/roll")
def roll():
    return send_from_directory("./static/", "video copy.html")

if __name__ == "__main__":
    app.run(debug=True)
