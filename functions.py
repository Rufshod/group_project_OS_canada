# File that holds our functions
import pandas as pd

# functions

def clean_df_from_team(df):
    """Function removes duplicates where each idividual is indicated with medal in team efforts"""
    dff = df.drop_duplicates(subset=["Year", "Event", "Medal"])
    return dff

def clean_df_from_athlet_repeat(df):
    """Function removes duplicates where same individual is listed several times same olympics"""
    dff = df.drop_duplicates(subset=["ID", "Year"])
    return dff
