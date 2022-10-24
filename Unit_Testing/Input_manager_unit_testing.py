import unittest
from InputManager import InputManager
import pandas as pd


class InputManagerTestCase(unittest.TestCase):

    def test_read_input_invalid_file_path(self):
        self.assertEqual(InputManager.read_input("data"), "Invalid Path")

    def test_read_input_csv_file(self):
        print(InputManager.read_input("data2.csv"))
        self.assertEqual( InputManager.read_input("data2.csv"), True)

    def test_read_input_invalid_file(self):
        self.assertEqual(InputManager.read_input("data2.cs"), "Invalid File Type")
