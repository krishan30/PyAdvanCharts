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

    def __init__(self, path, graph_colour="blue", title="", background_colour="white"):
        self.nodes_count = None
        self.nodes = None
        self.positions_of_nodes = None
        self.ax = None
        self.weights = None
        self.targets = None
        self.sources = None
        self.num_of_rows = None
        self.path = path
        self.graph_colour = graph_colour
        self.title = title
        self.background_colour = background_colour

        # previously clicked node details are stored in here
        self.previously_selected_node = 0
        self.previously_selected_arc = -1

        # All the parameters required to the equations related to arcs are stored inside this
        self.arc_equations = []

        # Keeps record of weights for each node pairs used to make arcs
        self.lines_with_weights = {}


    def get_information_from_file(self):
        """
        Return the collection of details for selected file for draw
        arc diagram. Returns count of rows for given csv file, from
        nodes list, to nodes list and weights list.

        :return: number of nodes, from nodes list, to nodes list, weight list
        """

        df = pd.read_csv(self.path)
        num_of_rows, num_of_cols = df.shape
        node1, node2, weight = df.columns
        return num_of_rows, df[node1], df[node2], df[weight]


    def get_nodes_positions(self, nodes_list):
        """
        Return nodes positions for the graph for given nodes list

        :param nodes_list: list of nodes
        :return: dictionary with details of position of each node for
        given nodes list
        """

        positions_of_nodes = {}
        x_pos = 0
        for node in nodes_list:
            positions_of_nodes[node] = x_pos
            x_pos += 1
        return positions_of_nodes

    def get_sorted_list_of_nodes_with_positions(self, src_lst, tar_lst):
        """
        Combine the src_list and tar_lst and return sorted list of nodes
        in ascending order and dictionary with details of nodes position
        in the graph.

        :param src_lst: from nodes list
        :param tar_lst: to nodes list
        :return: sorted list of nodes in ascending order and dictionary
        with details of nodes position in the diagram
        """

        nodes_list = src_lst.to_list()
        nodes_list.extend(tar_lst.to_list())
        nodes_list = list(set(nodes_list))
        nodes_list.sort()
        return nodes_list, self.get_nodes_positions(nodes_list)

    def set_lines_weights_for_duplicate_data(self, sources, targets, weights, num_of_rows):
        """
        Set list of weights for each arc by getting the sum of weights
        for duplicate node pairs in the graph and return none.

        :param sources: from nodes list
        :param targets: to nodes list
        :param weights: weight list for each node pair
        :param num_of_rows:
        :return: none
        """

        pairs = []
        for row in range(num_of_rows):
            if (sources[row], targets[row]) in pairs:
                self.lines_with_weights[(sources[row], targets[row])] += weights[row]
            elif (targets[row], sources[row]) in pairs:
                self.lines_with_weights[(targets[row], sources[row])] += weights[row]
            else:
                pairs.append((sources[row], targets[row]))
                self.lines_with_weights[(sources[row], targets[row])] = weights[row]

    def set_lines_weights_for_no_duplicate_data(self, sources, targets, weights, num_of_rows):
        """
        Set weights of arc for each pair of nodes in the graph and
        return none.

        :param sources: from nodes list
        :param targets: to nodes list
        :param weights: weight list for each node pair
        :param num_of_rows:
        :return: none
        """

        for row in range(num_of_rows):
            self.lines_with_weights[(sources[row], targets[row])] = weights[row]

    def get_lines_details(self):
        """
        Return details about arcs with weights for the graph

        :return: Dictionary with details about arcs(nodes pair)
        and weights of each arc
        """
        return self.lines_with_weights

    def add_node_text(self, node_index, color, weight, nodes):
        """
        Add node text in the diagram with the given attributes
        for the text decoration and return none.

        :param node_index: position of the node in the graph
        :param color: font colour
        :param weight: type of text decoration (normal, regular,..)
        :param nodes: list of nodes for the graph
        :return: none
        """

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

    def draw_arc(self, src, des, color, gid):
        """
        Draw arc in the graph using between src(node) and des(node) using
        given color and return none.

        :param src: from node
        :param des: to node
        :param color: arc colour
        :param gid: graph id
        :return: none
        """

        x1 = self.positions_of_nodes[src]
        x2 = self.positions_of_nodes[des]
        arc = Arc(((x1 + x2) / 2, 0), abs(x2 - x1), abs(x2 - x1), 0, 0, 180, color=color,
                  lw=self.lines_with_weights[(src, des)] / (self.nodes_count - 1) * 2, gid=gid)
        self.ax.add_patch(arc)
        return (x1 + x2) / 2, abs(x1 - x2) / 2

    # Check given cordinates on any arcs or not. If it is on the arc, return arc id
    def check_point_on_arc_or_not(self, x_co, y_co):
        """
        Check given x coordinate(x_co) and y coordinate(y_co) on any arc or not in
        the graph.

        If point on any arc, return graph id of arc.

        If point is not in any arc, return (-1)

        :param x_co: x coordinate
        :param y_co: y coordinate
        :return: graph id or (-1)
        """

        if y_co < 0:
            return -1
        for i in range(len(self.arc_equations)):
            h, r = self.arc_equations[i]
            value = y_co ** 2 + (x_co - h) ** 2
            line_half_width = 0.01 * (self.nodes_count - 1) * self.weights[i] / (self.nodes_count - 1) / 2
            if (r - line_half_width) ** 2 < value < (r + line_half_width) ** 2:
                return i
        return -1

    def change_arc_color(self, n, color):
        """
        Change color of the arc and return none.

        :param n: graph id of arc
        :param color: colour to change the arc
        :return: none
        """

        self.ax.patches[n].set_color(color)

    def change_line_colors_for_point(self, point, color):
        """
        Change colours of all the arcs connected to the given point.
        Change colours of arcs to given colour and return none. Show
        the weight of those arcs on top of the arc.

        :param point: selected node
        :param color: colour to change on arc
        :return: none
        """

        node_index = list(self.positions_of_nodes.values()).index(point)
        node_name = list(self.positions_of_nodes.keys())[node_index]

        index_lst = self.sources.index[self.sources == node_name].tolist()
        index_lst.extend(self.targets.index[self.targets == node_name].tolist())
        for index in index_lst:
            self.change_arc_color(index, color)

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

    def click_on_node(self, event):
        """
        Change the colours of selected node, arcs connected to selected node
        and return none.

        :param event: event
        :return: none
        """
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
            self.add_node_text(self.previously_selected_node, self.graph_background_colour, "bold",
                               self.nodes)
            self.add_node_text(self.previously_selected_node, self.graph_colour, "regular", self.nodes)
            self.add_node_text(x_co, self.graph_background_colour, "regular", self.nodes)
            self.add_node_text(x_co, self.graph_selection_colour, "bold", self.nodes)
            self.previously_selected_node = x_co
        else:
            self.change_line_colors_for_point(self.previously_selected_node, self.graph_colour)
            self.add_node_text(self.previously_selected_node, self.graph_colour, "regular", self.nodes)
            self.add_node_text(self.previously_selected_node, self.graph_background_colour, "bold",
                               self.nodes)
            self.add_node_text(self.previously_selected_node, self.graph_colour, "regular", self.nodes)
            self.ax.scatter(self.previously_selected_node, 0, marker='o', color=self.graph_colour)

    def click_on_arc(self, event):
        """
        Change the colour of selected arc and update the details of
        the selected arc on details box on left top corner and return
        none.

        :param event: event
        :return: none
        """
        x_coordinate, y_coordinate = event.xdata, event.ydata
        arc_id = self.check_point_on_arc_or_not(x_coordinate, y_coordinate)
        from_node = ""
        to_node = ""
        line_weight = 0

        if self.previously_selected_arc > 0:
            self.change_arc_color(self.previously_selected_arc, self.graph_colour)
            # self.ax.patches[self.previously_selected_arc].set_color(self.graph_colour)
            self.previously_selected_arc = -1

        if arc_id >= 0:
            from_node = self.sources[arc_id]
            to_node = self.targets[arc_id]
            line_weight = self.weights[arc_id]
            self.change_arc_color(arc_id, self.clicked_line_color)
            # self.ax.patches[arc_id].set_color(self.clicked_line_color)
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

    def get_arc_equations(self):
        """
        Return the list of set of characteristics for equations related to
        arcs on the graph. Characteristics set contains x coordinate of
        center point of the circle and radius value of the circle.

        :return: list of set of characteristics for equations
        """
        return self.arc_equations

    def set_arc_equations(self, arc_equations):
        """
        Set the characteristics for arc_equations related to graph and
        return none. Characteristics set contains x coordinate of
        center point of the circle and radius value of the circle.

        :param arc_equations: Set of characteristics for arcs
        :return: none
        """
        self.arc_equations = arc_equations

    # Set weights (For testing purpose)
    def set_weights(self, weights):
        """
        Set the weights list related to arcs drawing in the graph and
        return none.

        :param weights: list of weights for each arc
        :return: none
        """
        self.weights = weights

    # Set nodes count (For testing purpose)
    def set_nodes_count(self, nodes_count):
        """
        Set the count of nodes in the graph and return none.

        :param nodes_count: number of counts in the graph
        :return: none
        """
        self.nodes_count = nodes_count

    def set_background_colour(self, background_colour):
        """
        Set the background colour of the diagram for the plot and
        :return none.

        :param background_colour: colour to change background
        :return: none
        """
        self.background_colour = background_colour

    # Change font size of the graph
    def set_font_size(self, font_size):
        """
        Set font size used in the graph and return none.

        :param font_size: value of font size to change
        :return: none
        """
        self.font_size = font_size

    def generate_chart(self):
        """
        Generate chart using values of attributes in the graph and
        :return none.

        :return: none
        """

        self.num_of_rows, self.sources, self.targets, self.weights = self.get_information_from_file()
        self.nodes, self.positions_of_nodes = self.get_sorted_list_of_nodes_with_positions(self.sources, self.targets)

        self.set_lines_weights_for_no_duplicate_data(self.sources, self.targets, self.weights, self.num_of_rows)
        self.nodes_count = len(self.nodes)

        # Setup window
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim(-5, self.nodes_count / 2 + 1)
        self.ax.set_xlim(-1, self.nodes_count + 1)
        self.fig.canvas.set_window_title('Arc diagram')
        self.ax.axis('off')
        self.ax.title.set_text(self.title)
        self.fig.set_facecolor(self.background_colour)

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
            self.add_node_text(x_co, 'blue', 'regular', self.nodes)

        # Add events
        self.fig.canvas.mpl_connect('button_press_event', self.click_on_node)
        self.fig.canvas.mpl_connect('button_press_event', self.click_on_arc)

        self.fig.tight_layout()

        return self.fig
