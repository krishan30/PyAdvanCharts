import unittest
from charts import chord_chart as cc


class ChordTestCase(unittest.TestCase):

    def test_change_title_empty(self):
        chord_diagram = cc.ChordChart("../csv_samples/data2.csv")
        self.assertEqual(chord_diagram.change_title(""), False)

    def test_change_title(self):
        chord_diagram = cc.ChordChart("../csv_samples/data2.csv")
        self.assertEqual(chord_diagram.change_title("Chord Chart"), True)

    def test_change_font_colour(self):
        chord_diagram = cc.ChordChart("../csv_samples/data2.csv")
        self.assertEqual(chord_diagram.change_font_colour("Black"), True)

    def test_change_font_colour_Not_A_colour(self):
        chord_diagram = cc.ChordChart("../csv_samples/data2.csv")
        self.assertEqual(chord_diagram.change_font_colour("Hi"), False)

    def test_change_attribute_colour_map(self):
        chord_diagram = cc.ChordChart("../csv_samples/data2.csv")
        self.assertEqual(chord_diagram.change_attribute_colour_map('plasma'), 'plasma')

    def test_change_attribute_colour_map_not_A_colour_map(self):
        chord_diagram = cc.ChordChart("../csv_samples/data2.csv")
        self.assertEqual(chord_diagram.change_attribute_colour_map(10), None)


if __name__ == '__main__':
    unittest.main()
