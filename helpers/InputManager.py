import pandas as pd
from os.path import exists
import re


class InputManager:
    COLUMN_COUNT = 3

    def __init__(self):
        pass

    @classmethod
    def __read_csv_file(cls, file_name):
        if file_name:
            try:
                data_frame = pd.read_csv(file_name)
                if data_frame.empty:
                    return "NO entries"
                elif data_frame.shape[1] != InputManager.COLUMN_COUNT:
                    return "Column are not matched"
                else:
                    return data_frame
            except:
                return "File is empty"
        return "File name is empty"

    @classmethod
    def __read_xlsx_or_xls_file(cls, file_name):
        if file_name:
            try:
                data_frame = pd.read_excel(file_name)
                if data_frame.empty:
                    return "NO entries"
                elif data_frame.shape[1] != InputManager.COLUMN_COUNT:
                    return "Column are not matched"
                else:
                    return data_frame
            except:
                return "File is empty"
        return "File name is empty"

    @classmethod
    def __check_file_path_exists(cls, file_name):
        return exists(file_name)

    @classmethod
    def read_input(cls, file_name):

        if InputManager.__check_file_path_exists(file_name):
            if re.search('\.csv$', file_name, flags=re.IGNORECASE):
                return InputManager.__read_csv_file(file_name)
            elif re.search('\.xlsx$', file_name, flags=re.IGNORECASE) or re.search('\.xls$', file_name,
                                                                                   flags=re.IGNORECASE):
                return InputManager.__read_xlsx_or_xls_file(file_name)
            else:
                return "Invalid File Type"
        else:
            return "Invalid Path"
