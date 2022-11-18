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
df_os_winter = df_os_canada[df_os_canada["Season"] == "Winter"]
#print df
#print(df_os_canada.head())

#creating the app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{"name": "viewport","content": "width=device-width, initial-scale=1.0"}]) # automaticly creates a responsive site so that mobileusers can use it.



# Layout section: Bootstrap

# notes:
# 12 columns is the maximum of column in each rows.
# html.Main is html's own container. html.Div is 


#----------------------------------------------------------
app.layout = dbc.Container([ # Everything that shows up in the app needs to be in a container in order to be visable.
    dbc.Row([
        dbc.Col(html.H1("Canada Dashboard", # html.H1 is Title or header, 
        className="text-center text-danger mb-4"), # text center puts it in center, text danger makes text red.
        width=12)  
    ]),

    dbc.Row([
        dbc.Col([# new column inside row.
            dcc.Dropdown(id="my-drpdwn", multi=False, value="Swimming", #Sets dropdown and chooses Swimming as default.
                        options=[{"label": x, "value": x}  # Sets the options in drop down
                                    for x in sorted(df_os_winter["Sport"].unique())]), # Every option in sport is avaliable.
            dcc.Graph(id="bar-fig", figure={}) #creates an empty figure as placeholder
        
        ], width = {"size" :5, "offset":1,"order":1}), # offset changes how many columns it is offset to left/right.Sets size to the first 6 colums from the left, also changes width for both graph and dropdown because it is at the end of the column object.
        dbc.Col([ # new column inside row.
            dcc.Dropdown(id="my-drpdwn2", multi=True, value=["M","F"],  # auto selects both male and female
                        options=[{"label": x, "value": x}  # Sets the options in drop down
                                    for x in sorted(df_os_canada["Sex"].unique())]), # Every option in sex is avaliable.
            dcc.Graph(id="bar-fig2", figure={})
        ], width = {"size" :5, "offset":0, "order":2}) #Order changes what order elements will display.  # Sets size to the first avaliable space 6 colums from the left, also changes width for both graph and dropdown because it is at the end of the column object.
    ]),

    dbc.Row([


    ])

], fluid=True) # Fluid removes space from left and right. Try changing to false to see the difference.


# This code is needed in order to run.
if __name__ == "__main__":
    app.run_server(debug=True)