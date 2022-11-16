#Importing dependencies:
import dash
import os # os to access 
from load_data import StockData
from dash.dependencies import Output, Input
import plotly_express as px
from time_filtering import filter_time
import pandas as pd
from layout import Layout
import dash_bootstrap_components as dbc




# Adding directory path as variable.
directory_path = os.path.dirname(__file__)



# Boiler plate code:

if __name__ == "__main__":
    app.run_server(debug=True)