# df is all dataframe
# i layouten dcc.Store(id="dff")

# canada analysisf part

# canada-analysis-dropdown can be "Best sports", "Number of medals", "Age distribution", thus drop-down has those choices

@app.callback(
    Output("canada-graph", "figure"),
    Input("canada-analysis-dropdown", "analysis"),
)
def update_canada_graph(analysis_chosen):
    dff = df[df["NOC"] == "CAN"]                # filters out rows for Canada
    
    if analysis_chosen == "Best sports":
        dff = dff.clean_df_from_team()
        dff = dff.groupby("Sport").count().sort_values(by="Medal", ascending=False).head(10)
        fig = px.bar(dff, x=dff.index, y=["Medal"], title="Canada 10 top sports", labels={"value": "Total number of medals"})
        fig.update_layout(showlegend=False)
    
    if analysis_chosen == "Number of medals":
        dff = dff.clean_df_from_team()
        dff = dff.groupby("Year").count().sort_values(by="Medal", ascending=False).head(10)
        fig = px.bar(dff, x=dff.index, y=["Medal"], title="Canadian medals per olympics", labels={"value": "Total number of medals"})
        fig.update_layout(showlegend=False)

    if analysis_chosen == "Age distribution":
        fig = px.histogram(dff, x="Age", nbins=80, title="Age distribution canadian athletes", labels={"count": "Number of athletes"})     
    
    return fig



#sports analysis part

# sports-analysis-dropdown can be ["Number of medals", "Average age", "Age distribution", "Relative number of athletes"]
# sports-radio can be ["Athletics", "Swimming"]

@app.callback(
    Output("sports-graph", "figure"),
    Input("sports-analysis-dropdown", "analysis"),
    Input("sports-radio", "sport")
)

def uppdate_sports_graph(analysis_chosen, sports_chosen):
    # dff = df filtered on sport from sports-radio
    # if analysis_chosen == XXX:
        # how should dff be filtered
        # fig = create figure
    # return fig


def clean_df_from_team(df):
    """Function removes duplicates where each idividual is indicated with medal in team efforts"""
    dff = df.drop_duplicates(subset=["Year", "Event"])
    return dff

