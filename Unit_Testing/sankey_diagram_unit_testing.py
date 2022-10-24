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

   

if __name__ == '__main__':
    unittest.main()
