import numpy as np
import pandas as pd


class DataPreprocessor:

    @classmethod
    def data_cleaner(cls, data_frame: pd.DataFrame):

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

        return data_frame

