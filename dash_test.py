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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
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
        className="text-left text-danger mb-4"), # text center puts it in center, text danger makes text red.
        width={"size" :2, "offset":1,"order":1}),

        dbc.Col(html.H1("Olympic rings", # html.H1 is Title or header, 
        className="text-right text-danger mb-4"), # text center puts it in center, text danger makes text red.
        width={"size" :2, "offset":6,"order":2}),
        dbc.CardImg(src="os_logo.png")    
    ]),

    dbc.Row([
        dbc.Col([# new column inside row.
            dcc.Dropdown(id="my-drpdwn", multi=False, value="Swimming", #Sets dropdown and chooses Swimming as default.
                        options=[{"label": x, "value": x}  # Sets the options in drop down
                                    for x in sorted(df_os_summer["Sport"].unique())]), # Every option in sport is avaliable.
        
        ], width = {"size" :2, "offset":1,"order":1}), # offset changes how many columns it is offset to left/right.Sets size to the first 6 colums from the left, also changes width for both graph and dropdown because it is at the end of the column object.
        dbc.Col([ # new column inside row.
            dcc.Dropdown(id="my-drpdwn2", multi=True, value=["Atlanta","Sydney"],  # auto selects both male and female
                        options=[{"label": x, "value": x}  # Sets the options in drop down
                                    for x in sorted(df_os_canada["City"].unique())]), # Every option in sex is avaliable.

        ], width = {"size" :2, "offset":4, "order":2  }), #Order changes what order elements will display.  # Sets size to the first avaliable space 6 colums from the left, also changes width for both graph and dropdown because it is at the end of the column object.
        dbc.Col([ # new column inside row.
            dcc.Dropdown(id="my-drpdwn3", multi=True, value=["Sydney"],  # auto selects both male and female
                        options=[{"label": "RADIOITEM", "value": x}  # Sets the options in drop down
                                    for x in sorted(df_os_canada["City"].unique())]), # Every option in sex is avaliable.

        ], width = {"size" :2, "offset":0, "order":3}) #Order changes what order elements will display.  # Sets size to the first avaliable space 6 colums from the left, also changes width for both graph and dropdown because it is at the end of the column object.
    
    ],),

    dbc.Row([
        dbc.Col([dcc.Graph(id="testplot", figure={})]),
        dbc.Col([dcc.Graph(id="testplot1", figure={})]),
        ])

], fluid=True) # Fluid removes space from left and right. Try changing to false to see the difference.




# This code is needed in order to run.
if __name__ == "__main__":
    app.run_server(debug=True)