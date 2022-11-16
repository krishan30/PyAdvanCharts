import unittest

from charts.sankey_chart import SankeyChart

class SankeyTestCase(unittest.TestCase):

    def test_label(self):
        sankey_diagram = SankeyChart("./csv_samples/sankey_sample.csv")
        sankey_diagram.init_datas()
        sankey_diagram.find_labels()

        for i in range(4):
            self.assertEqual(sankey_diagram.fromLabels[i], ['Ashok' ,'Keerthi', 'Susi' ,'Meena'][i])

        for i in range(4):
            self.assertEqual(sankey_diagram.toLabels[i], ['Study' ,'Food' ,'Sport', 'Music'][i])

    def test_pallete(self):
        sankey_diagram = SankeyChart("./csv_samples/sankey_sample.csv")
        sankey_diagram.init_datas()
        sankey_diagram.find_labels()
        sankey_diagram.set_pallete("hls","flare")
        self.assertEqual(sankey_diagram.get_pallete(), ("hls","flare"))
    
    def test_font_size(self):
        sankey_diagram = SankeyChart("./csv_samples/sankey_sample.csv")
        sankey_diagram.init_datas()
        sankey_diagram.find_labels()
        sankey_diagram.set_label_font_size(12)
        self.assertEqual(sankey_diagram.get_label_font_size(), 12)
    
    def test_weight_size(self):
        sankey_diagram = SankeyChart("./csv_samples/sankey_sample.csv")
        sankey_diagram.init_datas()
        sankey_diagram.find_labels()
        sankey_diagram.set_block_alpha(0.5)
        self.assertEqual(sankey_diagram.get_block_alpha(), 0.5)

    def test_bg_color(self):
        sankey_diagram = SankeyChart("./csv_samples/sankey_sample.csv")
        sankey_diagram.init_datas()
        sankey_diagram.find_labels()
        sankey_diagram.set_bg_color("grey")
        self.assertEqual(sankey_diagram.get_bg_color(), "grey")
    
    def test_block_v_m(self):
        sankey_diagram = SankeyChart("./csv_samples/sankey_sample.csv")
        sankey_diagram.init_datas()
        sankey_diagram.find_labels()
        sankey_diagram.set_block_v_m(0.5)
        self.assertEqual(sankey_diagram.get_block_v_m(), 0.5)

    def test_title(self):
        sankey_diagram = SankeyChart("./csv_samples/sankey_sample.csv")
        sankey_diagram.init_datas()
        sankey_diagram.find_labels()
        sankey_diagram.set_title("test title")
        self.assertEqual(sankey_diagram.get_title(), "test title")

if __name__ == '__main__':
    unittest.main()
