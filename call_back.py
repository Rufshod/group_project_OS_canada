# df is all dataframe
df = #### add path
# i layouten dcc.Store(id="dff")

#----------------------------------------
# canada analysis
# canada-analysis-dropdown can be "Best sports", "Number of medals", "Age distribution", thus drop-down has those choices

@app.callback(
    Output("canada-graph", "figure"),
    Input("canada-analysis-dropdown", "analysis"),
)
def update_canada_graph(analysis_chosen):
    dff = df[df["NOC"] == "CAN"]                # filters out rows for Canada
    
    if analysis_chosen == "Best sports":
        dff = dff.clean_df_from_team().groupby("Sport").count().sort_values(by="Medal", ascending=False).head(10)
        fig = px.bar(dff, x=dff.index, y=["Medal"], title="Canada 10 top sports", labels={"value": "Total number of medals"})
        fig.update_layout(showlegend=False)
    
    if analysis_chosen == "Number of medals":
        dff = dff.clean_df_from_team().groupby("Year").count().sort_values(by="Medal", ascending=False)
        fig = px.bar(dff, x=dff.index, y=["Medal"], title="Canadian medals per olympics", labels={"value": "Total number of medals"})
        fig.update_layout(showlegend=False)

    if analysis_chosen == "Age distribution":
        fig = px.histogram(dff, x="Age", nbins=80, title="Age distribution canadian athletes", labels={"count": "Number of athletes"})     
    
    return fig

#----------------------------------------------------

#sports analysis part

# sports-analysis-dropdown can be ["Number of medals", "Average age per year", "Age distribution", "Relative number of athletes"]
# sports-radio can be ["Athletics", "Swimming"]

@app.callback(
    Output("sports-graph", "figure"),
    Input("sports-analysis-dropdown", "analysis"),
    Input("sports-radio", "sport")
)

def uppdate_sports_graph(analysis_chosen, sport_chosen):
    dff = df[df["Sport"] == sport_chosen]                 # hur får man in rätt värde här dvs Athletics eller swimming

    if analysis_chosen == "Number of medals":
        dff = dff.clean_df_from_team().groupby("Year").agg({"Medal":"count", "Age":"mean"})
        fig = px.bar(dff, x=dff.index, y=["Medal"], title=f"Total number of medals in {sport_chosen} per year", labels={"value": "Number of medals"})
        fig.update_layout(showlegend=False)
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Number of medals: %{value}")
    
    if analysis_chosen == "Average age per year":
        dff = dff.groupby("Year").agg({"Medal":"count", "Age":"mean"})
        fig = px.bar(dff, x=dff.index, y=["Age"], title= f"Average age in {sport_chosen} per year", labels={"value": "Average age"})
        fig.update_layout(showlegend=False, yaxis_range = [15,30])
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Average age: %{value}")
    
    if analysis_chosen == "Age distiribution":
        fig = px.histogram(dff, x="Age", nbins=80, title= f"Age distribution {sport_chosen}", labels={"count": "Number of athletes"})
    
    if analysis_chosen == "Relative number of athletes":
        dff_chosen_sport = dff.clean_df_from_athlet_repeat().groupby("Year").count().rename(columns={"ID":"Number in sport"})
        dff_all_sports = df.clean_df_from_athlet_repeat().groupby("Year").count().rename(columns={"ID":"Number tot"})
        dff = pd.concat([dff_chosen_sport, dff_all_sports], axis = 1)
        dff["Rel athletes in sport"] = 100 * dff["Number in sport"]/dff["Number tot"]
        fig = px.bar(dff, x=dff.index, y=["Rel athletes in sport"], title=f"Number of athletes in {sport_chosen} relative to all athletes", labels={"value": "Percentage"})
        fig.update_layout(showlegend=False)
        fig.update_traces(hovertemplate = "Year: %{label}: <br>Percentage: %{value}")

    return fig

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

