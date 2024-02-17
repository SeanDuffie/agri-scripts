""" plot_dat.py
"""

import dash
import pandas as pd
import plotly.express as px
import numpy as np


class Dataset:
    def __init__(self, path):
        self.data = pd.read_csv(path)
        self.data["Temperature"] = np.round((9*self.data["Temperature"] + 32*5)/5, 2)
        # self.data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
        # print(self.data)

    def plotHT(self):
        fig = px.scatter(self.data, x = "Humidity", y = "Temperature", title="Temperature vs Humidity")
        # fig.show()
        return fig

    def plotHL(self):
        fig = px.scatter(self.data, x = "Humidity", y = "Light Intensity", title="Light vs Humidity")
        # fig.show()
        return fig

    def plotToDH(self):
        fig = px.scatter(self.data, x = "Hour", y = "Humidity", title="Humidity vs Time of Day")
        # fig.show()
        return fig

    def plotToDT(self):
        fig = px.scatter(self.data, x = "Hour", y = "Temperature", title="Temperature vs Time of Day")
        # fig.show()
        return fig

    def plotToDL(self):
        fig = px.scatter(self.data, x = "Hour", y = "Light Intensity", title="Light vs Time of Day")
        # fig.show()
        return fig
    
    def plotToDW(self):
        fig = px.scatter(self.data, x = "Hour", y = "Soil Moisture", title="Water vs Time of Day")
        # fig.show()
        return fig
    
    def plotL(self):
        fig = px.scatter(self.data, x = "Date", y = "Light Intensity", title="Light over Time")
        # fig.show()
        return fig

    def plotW(self):
        fig = px.scatter(self.data, x = "Date", y = "Soil Moisture", title="Soil Moisture over Time")
        # fig.show()
        return fig

    def plotT(self):
        fig = px.scatter(self.data, x = "Date", y = "Temperature", title="Temperature over Time")
        # fig.show()
        return fig


if __name__ == "__main__":
    plant = Dataset("./data/dat.csv")

    plant.plotToDH()
    plant.plotToDT()
    plant.plotToDL()