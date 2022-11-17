import pandas as pd
import os


class SportData:
    def __init__(self, data_folder_path: str) -> None: 
        self._data_folder_path = data_folder_path # Creates data_folder_path

    def sport_dataframe(self, sportname: str) -> list:
        sport_df_list = []

        for path_ending in [
            "_athletics_athletes_rel.csv",
            "_athletics_medal_age.csv",
            "_athletics.csv",
            "_swimmers_rel.csv",
            "_swimming_medal_age.csv",
            "_swimming.csv"
        ]:
            # explanation of code below:
            # data_folder_path: C:\Users\Agam\Documents\Github\Databehandling-Alexander-Andersson\Code-alongs\L5-stocky_dashboard\stocksdata
            # stockname: AAPL,
            # path_ending: _TIME_SERIES_DAILY_ADJUSTED.csv
            # So below code = stockname+path_ending = AAPL_TIME_SERIES_DAILY_ADJUSTED.csv
            path = os.path.join(self._data_folder_path, sportname + path_ending)

            sport = pd.read_csv(path)
            #sport.index.rename("Date", inplace=True) This is not needed, index is correct as is. 

            sport_df_list.append(sport)

        return