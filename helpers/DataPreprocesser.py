import numpy as np
import pandas as pd


class DataPreprocessor:

    @classmethod
    def data_cleaner(cls, data_frame: pd.DataFrame):
        initial_number_of_data_entries = data_frame.shape[0]

        if data_frame.dtypes["Weight"] == 'int64' or data_frame.dtypes["Weight"] == 'float64':
            data_frame.dropna(inplace=True)
        else:
            # r^([A-Za-z]|_)+$
            data_frame["Weight"].replace(r'\D+', np.NaN, regex=True, inplace=True)
            data_frame.dropna(inplace=True)
        indexes = data_frame[pd.to_numeric(data_frame["Weight"]) < 0].index
        data_frame.drop(indexes, inplace=True)
        data_frame.drop_duplicates(inplace=True)
        if data_frame.empty:
            return "Data Frame is Empty", None
        available_number_of_data_entries = data_frame.shape[0]

        return "Out of " + str(initial_number_of_data_entries) + " data entries " + str(
            available_number_of_data_entries) + " are meet " \
                                                "the " \
                                                "required " \
                                                "conditions \n" \
                                                "so the " \
                                                "invalid " + str(
            initial_number_of_data_entries - available_number_of_data_entries) + " data entries will not " \
                                                                                 "be represented in the chart", data_frame
