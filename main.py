#Youtube codealong: https://www.youtube.com/watch?v=0mfIK8zxUds&t=662

import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly_express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
import pandas as pd
from functions import clean_df_from_team, clean_df_from_athlet_repeat

pio.templates.default = "gridon" # Changes default template for all graphs. 

#creating the dataframe with read csv
df = pd.read_csv("Data/athlete_events.csv")

#--------------------------------------------------

# Option variables for dropdown and radio.
canada_options = [{"label": option, "value": option} for option in ("Best sports", "Number of medals", "Age distribution")]
sports_options = [{"label": option, "value": option} for option in ("Number of medals", "Average age per year", "Age distribution", "Relative number of athletes")]
radio_options = [{"label": option, "value": option} for option in ("Athletics", "Swimming", "Gymnastics")]

#----------------------------------------------------------

#creating the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]) # automaticly creates a responsive site so that mobileusers can use it.

server = app.server  # Needed for Heroku to connect to app.

#----------------------------------------------------------

# Layout section: Bootstrap

#----------------------------------------------------------

app.layout = dbc.Container([ # Everything that is shown in app needs to be in Container

# First row for both cards.
    dbc.Row([
    # Column for Canada
        dbc.Col([
            # Card for Canada
            dbc.Card([
                #Column with Text for Canada
                dbc.Col([html.H1("Canada",id= "canada_text", style={"textDecoration": "underline"} ,),
                
                #Same Column as below with CardImg
                dbc.CardImg(src = "../assets/Flag_Canada.png", id="c_logo")], id="header1"),

                #Column with Dropdown for Canada
                dbc.Col([dcc.Dropdown(id="canada_dropdown", multi=False, value="Number of medals",
                        options=canada_options)]),
                #Column with Graph for Canada
                dbc.Col([dcc.Graph(id="canada_graph", figure={},className="card")],),
                ],
            ),
        ],width={"size":6,"offset":0}),

    # Card two for Sports
        dbc.Col([
            # Card for Sports
            dbc.Card([
                #Column with Text for Sports
                dbc.Col([html.H1("Sports",id= "sports_text", style={"textDecoration": "underline"}),
                html.Img(src= "../assets/os_logo.png", id="os_logo")], id="header2"),

                
                #Column with RadioItems for Sports
                dbc.Col([dcc.RadioItems(id="sports_radio", options= radio_options, value="Swimming")]),
                
                #Column with Dropdown for Sports
                dbc.Col([dcc.Dropdown(id="sports_dropdown_options", value="Number of medals",
                        options=sports_options)]),
                #Column with Graph for Sports
                dbc.Col([dcc.Graph(id="sport_graph", figure={},className="mt-4 mb-3")]),
                ]
            )
        ],width={"size":6,"offset":0}),
    ],)
],className="col", fluid=True)

#--------------------------------------------------------------------------------
# canada analysis call-back
# input from drop-down

@app.callback(
    Output("canada_graph", "figure"),
    Input("canada_dropdown", "value"),
)
def update_canada_graph(analysis_chosen):
    dff = df[df["NOC"] == "CAN"]                # filters out rows for Canada
    
    # one if statement for each possible choice from canada_dropdown "value"
    # under each statment: dff is created by appropiat filtering and fig is created
    # function returns fig

    if analysis_chosen == "Best sports":
        # dff: removed pultiple entries for team efforts, grouped by Sport and counted valies for Medal, sorted and picked 10 top values
        dff = clean_df_from_team(dff).groupby("Sport").count().sort_values(by="Medal", ascending=False).head(10)
        # bar plot with x = Sport, y = medal
        fig = px.bar(dff, x=dff.index, y=["Medal"], title="Canada 10 top sports", labels={"value": "Total number of medals"}, color_discrete_sequence=["#b91d1d"])
        # legend is not shown
        fig.update_layout(showlegend=False)
    
    if analysis_chosen == "Number of medals":
        dff = clean_df_from_team(dff).groupby("Year").count().sort_values(by="Medal", ascending=False)
        fig = px.bar(dff, x=dff.index, y=["Medal"], title="Canadian medals per olympics", labels={"value": "Total number of medals"}, color_discrete_sequence=["#b91d1d"])
        fig.update_layout(showlegend=False)

    if analysis_chosen == "Age distribution":
        fig = px.histogram(dff, x="Age", nbins=80, title="Age distribution canadian athletes", labels={"count": "Number of athletes"}, color_discrete_sequence=["#b91d1d"])     
        fig.update_layout(yaxis_title="Number of athletes")
   
    return fig                                    # returns figure till Output

#---------------------------------------------------------------------------------------------------
# sports analysis call-back
# input from drop-down and radio-items

@app.callback(
    Output("sport_graph", "figure"),
    Input("sports_dropdown_options", "value"),
    Input("sports_radio", "value")                   # Swimming by default
)

def uppdate_sports_graph(analysis_chosen, sport_chosen):
    dff = df[df["Sport"] == sport_chosen]           # filters for sport selected in radio-item             
    sport_chosen = sport_chosen.lower()             # changes sport_chosen to lowercase for style reasons

    if analysis_chosen == "Number of medals":
        dff = clean_df_from_team(dff).groupby("Year").agg({"Medal":"count", "Age":"mean"})
        fig = px.bar(dff, x=dff.index, y=["Medal"], title=f"Total number of medals in {sport_chosen} per year", labels={"value": "Number of medals"}, color_discrete_sequence=["#b91d1d"])
        fig.update_layout(showlegend=False)
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Number of medals: %{value}")
    
    if analysis_chosen == "Average age per year":
        dff = dff.groupby("Year").agg({"Medal":"count", "Age":"mean"})
        fig = px.bar(dff, x=dff.index, y=["Age"], title= f"Average age in {sport_chosen} per year", labels={"value": "Average age"}, color_discrete_sequence=["#b91d1d"])
        fig.update_layout(showlegend=False, yaxis_range = [15,30])
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Average age: %{value}",)
    
    if analysis_chosen == "Age distribution":
        fig = px.histogram(dff, x="Age", nbins=80, title= f"Age distribution {sport_chosen}", labels={"count": "Number of athletes"}, color_discrete_sequence=["#b91d1d"])
        fig.update_layout(yaxis_title="Number of athletes")

    if analysis_chosen == "Relative number of athletes":
        # 2 temp dffs created: one for chosen sport and on for all sports
        # col "ID" shows number of athlets in each dff. "ID" is renamed in each to enable concatinarion
        # 2 temp dffs are concatinated and new column created with ratio of athletes from chosen sport
        dff_chosen_sport = clean_df_from_athlet_repeat(dff).groupby("Year").count().rename(columns={"ID":"Number in sport"})
        dff_all_sports = clean_df_from_athlet_repeat(df).groupby("Year").count().rename(columns={"ID":"Number tot"})
        dff = pd.concat([dff_chosen_sport, dff_all_sports], axis = 1)
        dff["Rel athletes in sport"] = 100 * dff["Number in sport"]/dff["Number tot"]
        fig = px.line(dff, x=dff.index, y=["Rel athletes in sport"], title=f"Number of athletes in {sport_chosen} relative to all athletes", labels={"value": "Percentage"})
        fig.update_layout(showlegend=False)            # legend is not shown
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Percentage: %{value}", line_color="#b91d1d", line_width=5)       # adjust info shown when hoovering over graph  and changes color of line


    return fig


# This code is needed in order to run.
if __name__ == "__main__":
    app.run_server(debug=True)