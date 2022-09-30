import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import pandas as pd
from matplotlib.widgets import Cursor
import mplcursors


class ArcDiagram:
    # Properties in the graph window

    graph_selection_colour = "red"
    graph_background_colour = "white"
    clicked_line_color = "green"
    font_size = 10
    fig = plt.figure(figsize=(6, 6))

    def __init__(self, path, graph_colour="blue"):
        self.nodes_count = None
        self.nodes = None
        self.positions_of_nodes = None
        self.ax = None
        self.max_position = None
        self.weights = None
        self.targets = None
        self.sources = None
        self.num_of_rows = None
        self.path = path
        self.graph_colour = graph_colour

        # previously clicked node details are stored in here
        self.previously_selected_node = 0
        self.previously_selected_arc = -1

        # All the parameters required to the equations related to arcs are stored inside this
        self.arc_equations = []

        # Keeps record of weights for each node pairs used to make arcs
        self.lines_with_weights = {}

    # Return required information from file
    def get_information_from_file(self, file_name):
        df = pd.read_csv(file_name)
        num_of_rows, num_of_cols = df.shape
        node1, node2, weight = df.columns
        return num_of_rows, df[node1], df[node2], df[weight]

    # Get nodes positions array
    def get_nodes_positions(self, nodes_list):
        positions_of_nodes = {}
        x_pos = 0
        for node in nodes_list:
            positions_of_nodes[node] = x_pos
            x_pos += 1
        return positions_of_nodes

    # Return sorted nodes list with positions array for given two nodes list
    def get_sorted_list_of_nodes_with_positions(self, src_lst, tar_lst):
        nodes_list = src_lst.to_list()
        nodes_list.extend(tar_lst.to_list())
        nodes_list = list(set(nodes_list))
        nodes_list.sort()
        return nodes_list, self.get_nodes_positions(nodes_list)

    # Set weights for each line when there are duplicated node pairs in data
    def set_lines_weights_for_duplicate_data(self, sources, targets, weights, num_of_rows):
        pairs = []
        for row in range(num_of_rows):
            if (sources[row], targets[row]) in pairs:
                self.lines_with_weights[(sources[row], targets[row])] += weights[row]
            elif (targets[row], sources[row]) in pairs:
                self.lines_with_weights[(targets[row], sources[row])] += weights[row]
            else:
                pairs.append((sources[row], targets[row]))
                self.lines_with_weights[(sources[row], targets[row])] = weights[row]

    # Set weights for each line when there are no duplicated node pairs in data
    def set_lines_weights_for_no_duplicate_data(self, sources, targets, weights, num_of_rows):
        for row in range(num_of_rows):
            self.lines_with_weights[(sources[row], targets[row])] = weights[row]

    # Add or change text related to node
    def add_or_change_node_text(self, node_index, color, weight, nodes):
        node_index = int(node_index)
        label = nodes[node_index]

        self.ax.annotate(label,  # this is the text
                         (node_index, 0),  # these are the coordinates to position the label
                         textcoords="offset points",  # how to position the text
                         xytext=(-4, -6),  # distance from text to points (x,y)
                         rotation=90,
                         va='top',
                         fontsize=self.font_size,
                         weight=weight,
                         color=color,
                         ha='left')

    # Draw arc
    def draw_arc(self, src, des, color, gid):
        x1 = self.positions_of_nodes[src]
        x2 = self.positions_of_nodes[des]
        arc = Arc(((x1 + x2) / 2, 0), abs(x2 - x1), abs(x2 - x1), 0, 0, 180, color=color,
                  lw=self.lines_with_weights[(src, des)] / self.max_position * 2, gid=gid)
        self.ax.add_patch(arc)
        return (x1 + x2) / 2, abs(x1 - x2) / 2

    # Check given cordinates on any arcs or not. If it is on the arc, return arc id
    def check_point_on_arc_or_not(self, x_co, y_co):
        if y_co < 0:
            return -1
        for i in range(len(self.arc_equations)):
            h, r = self.arc_equations[i]
            value = y_co ** 2 + (x_co - h) ** 2
            line_half_width = 0.01 * (self.nodes_count - 1) * self.weights[i] / self.max_position / 2
            if (r - line_half_width) ** 2 < value < (r + line_half_width) ** 2:
                return i
        return -1

    # Change arc colour
    def change_patch_color(self, n, color):
        self.ax.patches[n].set_color(color)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.show()

    # change color of the lines that are starting or ending from given point
    def change_line_colors_for_point(self, point, color):
        node_index = list(self.positions_of_nodes.values()).index(point)
        node_name = list(self.positions_of_nodes.keys())[node_index]

        index_lst = self.sources.index[self.sources == node_name].tolist()
        index_lst.extend(self.targets.index[self.targets == node_name].tolist())
        for index in index_lst:
            self.ax.patches[index].set_color(color)
            # h, r = self.arc_equations[index]
            # text_color = color
            # weight = 'regular'
            # if text_color == self.graph_colour:
            #     text_color = self.graph_background_colour
            #     weight = 'bold'
            # self.ax.annotate(self.weights[index], (h, r), xytext=(0, 6), rotation=0, textcoords="offset points",
            #                  fontsize=10,
            #                  ha='left', va='bottom', color=text_color, weight=weight)
        return self.fig

    # When user click on a node, change line colors related to selected node.
    def click_on_node(self, event):
        x1, y1 = event.xdata, event.ydata
        x_co = round(x1, 1)
        y_co = round(y1, 0)
        if int(y_co) == 0 and x_co.is_integer():
            # Change line colours
            self.change_line_colors_for_point(self.previously_selected_node, self.graph_colour)
            self.change_line_colors_for_point(x_co, self.graph_selection_colour)
            # Change points colours
            self.ax.scatter(self.previously_selected_node, 0, marker='o', color=self.graph_colour)
            self.ax.scatter(x_co, 0, marker='o', color=self.graph_selection_colour)
            # Change node text styles
            self.add_or_change_node_text(self.previously_selected_node, self.graph_background_colour, "bold",
                                         self.nodes)
            self.add_or_change_node_text(self.previously_selected_node, self.graph_colour, "regular", self.nodes)
            self.add_or_change_node_text(x_co, self.graph_background_colour, "regular", self.nodes)
            self.add_or_change_node_text(x_co, self.graph_selection_colour, "bold", self.nodes)
            self.previously_selected_node = x_co
        else:
            self.change_line_colors_for_point(self.previously_selected_node, self.graph_colour)
            self.add_or_change_node_text(self.previously_selected_node, self.graph_colour, "regular", self.nodes)
            self.add_or_change_node_text(self.previously_selected_node, self.graph_background_colour, "bold",
                                         self.nodes)
            self.add_or_change_node_text(self.previously_selected_node, self.graph_colour, "regular", self.nodes)
            self.ax.scatter(self.previously_selected_node, 0, marker='o', color=self.graph_colour)

    # When user click on a point in arc
    def click_on_arc(self, event):
        x_coordinate, y_coordinate = event.xdata, event.ydata
        arc_id = self.check_point_on_arc_or_not(x_coordinate, y_coordinate)
        from_node = ""
        to_node = ""
        line_weight = 0
        if self.previously_selected_arc > 0:
            self.ax.patches[self.previously_selected_arc].set_color(self.graph_colour)
            self.previously_selected_arc = -1
        if arc_id >= 0:
            from_node = self.sources[arc_id]
            to_node = self.targets[arc_id]
            line_weight = self.weights[arc_id]
            self.ax.patches[arc_id].set_color(self.clicked_line_color)
            self.previously_selected_arc = arc_id

        # Clear the previously created box in the graph
        delete_textstr = "Nodes  :- {f_node} - {t_node}\nWeight :- {w}".format(
            f_node="Delete this text from node for next time",
            t_node="Delete this text from node for next time",
            w=line_weight)
        props_del = dict(boxstyle='square', facecolor='white', edgecolor='white', alpha=1, linewidth=2.0)
        self.ax.text(0.03, 0.95, delete_textstr, transform=self.ax.transAxes, fontsize=10, color='white',
                     verticalalignment='top', bbox=props_del)

        # Create next details box according to the position clicked in the canvas
        textstr = "Nodes  :- {f_node} - {t_node}\nWeight :- {w}".format(f_node=from_node, t_node=to_node, w=line_weight)
        props = dict(boxstyle='round', facecolor='lightsteelblue', edgecolor='navy', alpha=0.5)
        self.ax.text(0.03, 0.95, textstr, transform=self.ax.transAxes, fontsize=10,
                     verticalalignment='top', bbox=props)

    def generate_chart(self):

        self.num_of_rows, self.sources, self.targets, self.weights = self.get_information_from_file(self.path)
        self.nodes, self.positions_of_nodes = self.get_sorted_list_of_nodes_with_positions(self.sources, self.targets)
        self.max_position = max(self.positions_of_nodes.values())

        self.set_lines_weights_for_no_duplicate_data(self.sources, self.targets, self.weights, self.num_of_rows)
        self.nodes_count = len(self.nodes)

        # Setup window
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim(-5, self.nodes_count / 2 + 1)
        self.ax.set_xlim(-1, self.nodes_count + 1)
        self.fig.canvas.set_window_title('Arc diagram')
        self.ax.axis('off')

        # Position the nodes in the graph
        xs = [i for i in range(self.nodes_count)]
        ys = [0] * self.nodes_count
        points = self.ax.scatter(xs, ys, marker='o')

        # Add annotation for cursor hovering events on nodes(display node name when hovering)
        cursor_for_points = mplcursors.cursor(points, hover=True)

        @cursor_for_points.connect("add")
        def on_add(select):
            select.annotation.set(text=self.nodes[select.index])

        cursor = Cursor(self.ax, horizOn=False, vertOn=False)

        # Draw arcs according to the data in lines dictionary
        gid = 0
        for src, des in self.lines_with_weights:
            h, r = self.draw_arc(src, des, self.graph_colour, gid)
            self.arc_equations.append((h, r))
            gid += 1

        # Add names in nodes
        for x_co in xs:
            self.add_or_change_node_text(x_co, 'blue', 'regular', self.nodes)

        # Add events
        self.fig.canvas.mpl_connect('button_press_event', self.click_on_node)
        self.fig.canvas.mpl_connect('button_press_event', self.click_on_arc)

        self.fig.tight_layout()

        # self.figure=plt.figure()
        # plt.gcf().set_size_inches(6, 6)

        return self.fig
        # return self.figure
