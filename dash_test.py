#Youtube codealong: https://www.youtube.com/watch?v=0mfIK8zxUds&t=662

import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly_express as px
import dash_bootstrap_components as dbc
import pandas as pd

#creating the dataframe with read csv
df = pd.read_csv("Data/athlete_events.csv")
df_os_canada = df[df["NOC"]=="CAN"] # Creating Canada df.
df_os_summer = df_os_canada[df_os_canada["Season"] == "Summer"]
#print df
#print(df_os_canada.head())

#creating the app

#Variables 
canada_options = [{"label": option, "value": option} for option in ("top 10 sports", "medals per os", "prop athletes", "age distro can", "sex distro")]
sports_options = [{"label": option, "value": option} for option in ("num of medals", "mean age", "prop athletes", "age distro sport")]
radio_options = [{"label": option, "value": option} for option in ("Athletics", "Swimming")]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{"name": "viewport","content": "width=device-width, initial-scale=1.0"}]) # automaticly creates a responsive site so that mobileusers can use it.



# Layout section: Bootstrap

# notes:
# 12 columns is the maximum of column in each rows.
# html.Main is html's own container. html.Div is 
# dcc.store
# Ett stort dataframe, filtrerings funktion:
#df 

# @callback(Output("graph-left")),
#            input("sport.dropdown")
# def update.sport.graph(sport)
#       dffilter = df.query("Sport == @sport") @sport is a variable from aboce.
#       fig = px.bar(...)
            #return fig

#----------------------------
  #@callback(Output(graph-left),input("sport-drop"))
  # def medal.graph(sport)

  # def team_df.clean(df):
    #   return df.


#----------------------------------------------------------
app.layout = dbc.Container([ # Everything that shows up in the app needs to be in a container in order to be visable.
    dbc.Row([
        dbc.Col(html.H1("Dashboard", # html.H1 is Title or header, 
        className="text-left text-danger mb-4 border border-danger", style={"textDecoration": "underline"}), # text center puts it in center, text danger makes text red.
        width={"size" :2, "offset":1,"order":1}),

        dbc.Col(html.H1("os_logo.png", # html.H1 is Title or header, 
        className="text-right text-danger mb-4"), # text center puts it in center, text danger makes text red.
        width={"size" :2, "offset":6,"order":2}),
        #html.Img(src= "../assets/os_logo.png", className="img-fluid", alt="Responsive image"), # Add in image later.
        ]),

    dbc.Row([
        dbc.Col([# new column inside row.

        # ----------------------------------- CANADA DROPDOWN -----------------------------------
            dcc.Dropdown(id="canada_dropdown", multi=False, value="top 10 sports", #Sets dropdown and chooses Swimming as default.
                        options=canada_options), # Every option in sport is avaliable.
                        ], width = {"size" :2, "offset":1,"order":1}), # offset changes how many columns it is offset to left/right.Sets size to the first 6 colums from the left, also changes width for both graph and dropdown because it is at the end of the column object.
        
        dbc.Col([ # new column inside row.
        # ----------------------------------- SPORTS DROPDOWN -----------------------------------
            dcc.Dropdown(id="sports_dropdown_options", value="mean age",  # auto selects both male and female
                        options=sports_options), # sets drop down options

        ], width = {"size" :2, "offset":4, "order":2  }), #Order changes what order elements will display.  # Sets size to the first avaliable space 6 colums from the left, also changes width for both graph and dropdown because it is at the end of the column object.
        # ----------------------------------- RADIO DROPDOWN -----------------------------------
        dbc.Col([ # new column inside row.
            dcc.RadioItems(id="sports_radio", options= radio_options, value="Swimming",), #radio_options var can be found on row 21 
                ], width = {"size" :2, "offset":0, "order":3}, className="text-success")]), # MR 3 should put a larger space between Athletics and swimming. It does not work though...

 #Order changes what order elements will display.  # Sets size to the first avaliable space 6 colums from the left, also changes width for both graph and dropdown because it is at the end of the column object.
    

    dbc.Row([
        dbc.Col([dcc.Graph(id="canada_graph", figure={})]),
        dbc.Col([dcc.Graph(id="sport_graph", figure={})]),
        ])

], fluid=True) # Fluid removes space from left and right. Try changing to false to see the difference.




# This code is needed in order to run.
if __name__ == "__main__":
    app.run_server(debug=True)