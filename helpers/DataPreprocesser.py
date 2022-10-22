import tkinter

import numpy as np
import pandas as pd


class DataPreprocessor:

    @classmethod
    def data_cleaner(cls, data_frame: pd.DataFrame):
        initial_number_of_data_entries = data_frame.shape[0]

        if "Weight" not in data_frame.dtypes:
            return "Weight column Not Exist"
        if data_frame.dtypes["Weight"] == 'int64' or data_frame.dtypes["Weight"] == 'float64':
            data_frame.dropna(inplace=True)
        else:
            data_frame["Weight"].replace(r'^([A-Za-z]|[0-9]|_)+$', np.NaN, regex=True, inplace=True)
            data_frame.dropna(inplace=True)
        data_frame.drop_duplicates(inplace=True)

        if data_frame.empty:
            return "Data Frame is Empty"
        available_number_of_data_entries = data_frame.shape[0]

        return "Out of " + str(initial_number_of_data_entries) + " data entries " + str(
            available_number_of_data_entries) + " are meet " \
                                                "the " \
                                                "required " \
                                                "conditions \n" \
                                                "so the " \
                                                "invalid "+str(initial_number_of_data_entries-available_number_of_data_entries)+" data entries will not " \
                                                "be represented in the chart", data_frame
