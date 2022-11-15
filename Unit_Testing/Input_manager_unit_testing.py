import unittest

import customtkinter

from helpers.InputManager import InputManager


class InputManagerTestCase(unittest.TestCase):

    def test_read_input_invalid_file_path(self):
        root = None
        self.assertEqual(InputManager.read_input("data", root), True)

    def test_read_input_csv_file(self):
        root = None
        self.assertEqual(InputManager.read_input("data2.csv", root), True)

    def test_read_input_invalid_file(self):
        root = None
        self.assertEqual(InputManager.read_input("data2.cs", root), "Invalid File Type")
