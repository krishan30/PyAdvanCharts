import unittest

from charts import arc_diagram as ad


class ArcTestCase(unittest.TestCase):

    def test_get_lines_weights_for_duplicate_data(self):
        arc_diagram = ad.ArcDiagram("../csv_samples/test_arc.csv")
        num_of_rows, sources, targets, weights = arc_diagram.get_information_from_file()

        arc_diagram.set_lines_weights_for_duplicate_data(sources, targets, weights, num_of_rows)

        self.assertEqual(arc_diagram.get_lines_details(),
                         {('B', 'D'): 6, ('A', 'B'): 9, ('A', 'C'): 2, ('A', 'D'): 1})

    def test_check_point_on_arc_or_not(self):
        arc_diagram = ad.ArcDiagram("../csv_samples/test_arc.csv")
        # Add values to some attributes for testing
        arc_diagram.set_arc_equations([(2, 1)])  # Add (x-2)**2 + y**2 = 1
        arc_diagram.set_weights([5])
        arc_diagram.set_nodes_count(2)

        self.assertEqual(arc_diagram.check_point_on_arc_or_not(2, 1), 0)
        self.assertEqual(arc_diagram.check_point_on_arc_or_not(2, -1), -1)
        self.assertEqual(arc_diagram.check_point_on_arc_or_not(2, 1.1), -1)
        self.assertEqual(arc_diagram.check_point_on_arc_or_not(3, 0.9), -1)

    def test_get_nodes_positions(self):
        arc_diagram = ad.ArcDiagram("../csv_samples/test_arc.csv")
        self.assertEqual(arc_diagram.get_nodes_positions(["node1", "node2"]),
                         {"node1": 0, "node2": 1})

    def test_get_sorted_list_of_nodes_with_positions(self):
        arc_diagram = ad.ArcDiagram("../csv_samples/test_arc.csv")
        num_of_rows, sources, targets, weights = arc_diagram.get_information_from_file()

        self.assertEqual(arc_diagram.get_sorted_list_of_nodes_with_positions(sources, targets),
                         (['A', 'B', 'C', 'D'], {'A': 0, 'B': 1, 'C': 2, 'D': 3}))


if __name__ == '__main__':
    unittest.main()
