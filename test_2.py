#Youtube codealong: https://www.youtube.com/watch?v=0mfIK8zxUds&t=662

import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly_express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
import pandas as pd

pio.templates.default = "gridon"

#creating the dataframe with read csv
df = pd.read_csv("Data/athlete_events.csv")

#--------------------------------------------------

# functions

def clean_df_from_team(df):
    """Function removes duplicates where each idividual is indicated with medal in team efforts"""
    dff = df.drop_duplicates(subset=["Year", "Event", "Medal"])
    return dff

def clean_df_from_athlet_repeat(df):
    """Function removes duplicates where same individual is listed several times same olympics"""
    dff = df.drop_duplicates(subset=["ID", "Year"])
    return dff



#print df
#print(df_os_canada.head())

#creating the app

#Variables # Check type
canada_options = [{"label": option, "value": option} for option in ("Best sports", "Number of medals", "Age distribution")]
sports_options = [{"label": option, "value": option} for option in ("Number of medals", "Average age per year", "Age distribution", "Relative number of athletes")]
radio_options = [{"label": option, "value": option} for option in ("Athletics", "Swimming", "Gymnastics")]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE],
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
#       dffilter = df.query("Sport == @sport") @sport is a variable from above.
#       fig = px.bar(...)
            #return fig

#----------------------------
  #@callback(Output(graph-left),input("sport-drop"))
  # def medal.graph(sport)

  # def team_df.clean(df):
    #   return df.

#----------------------------------------------------------
app.layout = dbc.Container([ # Everything that shows up in the app needs to be in a container in order to be visable.
# First row with dashboard header and olympic logo.
    dbc.Row([

        dbc.Col([html.H1("Dashboard",id= "head1",className="text bold" )],width={"offset":0}, ), # html.H1 is Title or header, 
        dbc.Col([html.Img(src= "../assets/os_logo.png", id="os_logo", className="mb-3 ")]),   
    ]),
# Second row for both cards.
    dbc.Row([
    # Column for Canada
        dbc.Col([
            # Card for Canada
            dbc.Card([
                #Column with Text for Canada
                dbc.Col([html.H1("Canada",id= "canada_text",className="" , style={"textDecoration": "underline"} ),dbc.CardImg(src = "../assets/Flag_Canada.png", id="c_logo", className="")],width={}),

                #Column with CardImg
                dbc.Col([]),
                
                #Column with Dropdown for Canada
                dbc.Col([dcc.Dropdown(id="canada_dropdown", className="mb-", multi=False, value="Number of medals", #Sets dropdown and chooses Swimming as default.
                        options=canada_options),]),
                #Column with Graph for Canada
                dbc.Col([dcc.Graph(id="canada_graph", figure={},className="card mb-3")],),
                
                ],
                


                ),
                ],width={"size":6,"offset":0}),

    # Card two for Sports
        dbc.Col([
            # Card for Sports
            dbc.Card([
                #Column with Text for Sports
                dbc.Col([html.H1("Sports",id= "sports_text",className="", style={"textDecoration": "underline"} )],width={}),

                #Column with Dropdown for Sports
                dbc.Col([dcc.Dropdown(id="sports_dropdown_options", value="Number of medals",  # auto selects both male and female
                        options=sports_options)]),
                
                #Column with RadioItems for Sports
                dbc.Col([dcc.RadioItems(id="sports_radio", options= radio_options, value="Swimming",)]
                ,width = {}, className="mt-3 mb-3"),
                #Column with Graph for Sports
                dbc.Col([dcc.Graph(id="sport_graph", figure={},className="mb-3")],),
                
                ]
                


                )
                ],width={"size":6,"offset":0}),




        ])
])

#----------------------------------------
# canada analysis
# canada-analysis-dropdown can be "Best sports", "Number of medals", "Age distribution", thus drop-down has those choices

@app.callback(
    Output("canada_graph", "figure"),
    Input("canada_dropdown", "value"),
)
def update_canada_graph(analysis_chosen):
    dff = df[df["NOC"] == "CAN"]                # filters out rows for Canada
    
    if analysis_chosen == "Best sports":
        dff = clean_df_from_team(dff).groupby("Sport").count().sort_values(by="Medal", ascending=False).head(10)
        fig = px.bar(dff, x=dff.index, y=["Medal"], title="Canada 10 top sports", labels={"value": "Total number of medals"})
        fig.update_layout(showlegend=False)
    
    if analysis_chosen == "Number of medals":
        dff = clean_df_from_team(dff).groupby("Year").count().sort_values(by="Medal", ascending=False)
        fig = px.bar(dff, x=dff.index, y=["Medal"], title="Canadian medals per olympics", labels={"value": "Total number of medals"})
        fig.update_layout(showlegend=False)

    if analysis_chosen == "Age distribution":
        fig = px.histogram(dff, x="Age", nbins=80, title="Age distribution canadian athletes", labels={"count": "Number of athletes"})     
        fig.update_layout(yaxis_title="Number of athletes")
        
    return fig

#----------------------------------------------------

#sports analysis part

# sports-analysis-dropdown can be ["Number of medals", "Average age per year", "Age distribution", "Relative number of athletes"]
# sports-radio can be ["Athletics", "Swimming"]

@app.callback(
    Output("sport_graph", "figure"),
    Input("sports_dropdown_options", "value"),
    Input("sports_radio", "value") # Swimming by default
)

def uppdate_sports_graph(analysis_chosen, sport_chosen):
    dff = df[df["Sport"] == sport_chosen]                 # hur får man in rätt värde här dvs Athletics eller swimming

    if analysis_chosen == "Number of medals":
        dff = clean_df_from_team(dff).groupby("Year").agg({"Medal":"count", "Age":"mean"})
        fig = px.bar(dff, x=dff.index, y=["Medal"], title=f"Total number of medals in {sport_chosen.lower()} per year", labels={"value": "Number of medals"})
        fig.update_layout(showlegend=False)
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Number of medals: %{value}")
    
    if analysis_chosen == "Average age per year":
        dff = dff.groupby("Year").agg({"Medal":"count", "Age":"mean"})
        fig = px.bar(dff, x=dff.index, y=["Age"], title= f"Average age in {sport_chosen.lower()} per year", labels={"value": "Average age"})
        fig.update_layout(showlegend=False, yaxis_range = [15,30])
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Average age: %{value}")
    
    if analysis_chosen == "Age distribution":
        fig = px.histogram(dff, x="Age", nbins=80, title= f"Age distribution {sport_chosen.lower()}", labels={"count": "Number of athletes"})
        fig.update_layout(yaxis_title="Number of athletes")

    if analysis_chosen == "Relative number of athletes":
        dff_chosen_sport = clean_df_from_athlet_repeat(dff).groupby("Year").count().rename(columns={"ID":"Number in sport"})
        dff_all_sports = clean_df_from_athlet_repeat(df).groupby("Year").count().rename(columns={"ID":"Number tot"})
        dff = pd.concat([dff_chosen_sport, dff_all_sports], axis = 1)
        dff["Rel athletes in sport"] = 100 * dff["Number in sport"]/dff["Number tot"]
        fig = px.line(dff, x=dff.index, y=["Rel athletes in sport"], title=f"Number of athletes in {sport_chosen.lower()} relative to all athletes", labels={"value": "Percentage"})
        fig.update_layout(showlegend=False)
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Percentage: %{value}")

    return fig


# This code is needed in order to run.
if __name__ == "__main__":
    app.run_server(debug=True)