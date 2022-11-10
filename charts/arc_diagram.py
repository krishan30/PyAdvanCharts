import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import pandas as pd
from matplotlib.widgets import Cursor
import mplcursors


class ArcDiagram:

    def __init__(self, path=None, data_frame=None):
        self.nodes_count = None
        self.nodes = None
        self.positions_of_nodes = None
        self.ax = None
        self.weights = None
        self.targets = None
        self.sources = None
        self.num_of_rows = None
        self.fig = None
        self.path = path
        self.data_frame = data_frame
        self.graph_colour = "blue"
        self.title = "Arc Diagram"
        self.sub_title = None
        self.title_font_colour = "blue"
        self.title_font_type = "serif"
        self.title_font_size = 20
        self.background_colour = "white"
        self.node_selected_arc_colour = "red"
        self.selected_line_colour = "green"
        self.font_size = 10
        self.font_type = "serif"
        self.line_width_multiplier = 2
        self.from_weight = None
        self.to_weight = None

        # All the parameters required to the equations related to arcs are stored inside this
        self.arc_equations = None

        # Keeps record of weights for each node pairs used to make arcs
        self.lines_with_weights = None

        # Keeps the values of width in each arcs inside this list
        self.lines_width_values = None

        # previously clicked node and arc details are stored in here
        self.previously_selected_node = 0
        self.previously_selected_arc = -1

    def get_information(self):
        """
        Return the collection of details for selected file for draw
        arc diagram. Returns count of rows for given csv file, from
        nodes list, to nodes list and weights list.

        :return: number of nodes, from nodes list, to nodes list, weight list
        """

        self.arc_equations = []
        self.lines_width_values = []
        self.lines_with_weights = {}
        self.sub_title = "( Weight range: "

        self.previously_selected_node = 0
        self.previously_selected_arc = -1

        if self.path is None:
            df = self.data_frame
        else:
            df = pd.read_csv(self.path)

        node1, node2, weight = df.columns

        if self.from_weight is None:
            self.from_weight = min(df[weight])
            self.sub_title = self.sub_title + "  - "
        else:
            self.sub_title = self.sub_title + str(self.from_weight) + " - "

        if self.to_weight is None:
            self.to_weight = max(df[weight])
            self.sub_title = self.sub_title + "  )"
        else:
            self.sub_title = self.sub_title + str(self.to_weight) + " )"

        filtered_df = df.loc[(df[weight] >= self.from_weight) & (df[weight] <= self.to_weight)].reset_index()
        num_of_rows, num_of_cols = filtered_df.shape

        return num_of_rows, filtered_df[node1], filtered_df[node2], filtered_df[weight]

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
                         family=self.font_type,
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
                  lw=self.lines_with_weights[(src, des)] / (
                              max(self.weights) - min(self.weights)) * self.line_width_multiplier, gid=gid)
        self.ax.add_patch(arc)
        self.lines_width_values.append(
            self.lines_with_weights[(src, des)] / (max(self.weights) - min(self.weights)) * self.line_width_multiplier)
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
            line_half_width = 0.01 * self.lines_width_values[i]
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

        # Remove previously created weight text up on the arc
        if color == self.graph_colour:
            index_to_check = len(self.ax.texts)-1
            count_found = 0
            while count_found < len(index_lst) and index_to_check > 0:
                obj = self.ax.texts[index_to_check]
                try:
                    temp = int(obj.get_text())
                    obj.set_visible(False)
                    count_found += 1
                    self.ax.texts.remove(obj)
                except:
                    pass
                index_to_check -= 1

        for index in index_lst:
            self.change_arc_color(index, color)

            # Added weights up on the arcs
            if color != self.graph_colour:
                h, r = self.arc_equations[index]
                props = dict(boxstyle='round', facecolor=self.background_colour,
                             edgecolor=self.node_selected_arc_colour, alpha=0.5)
                self.ax.text(h, r, str(self.weights[index]), fontsize=self.font_size,
                              fontfamily=self.font_type, color=self.node_selected_arc_colour, bbox=props)
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
            self.change_line_colors_for_point(x_co, self.node_selected_arc_colour)
            # Change points colours
            self.ax.scatter(self.previously_selected_node, 0, marker='o', color=self.graph_colour)
            self.ax.scatter(x_co, 0, marker='o', color=self.node_selected_arc_colour)
            # Change node text styles
            self.add_node_text(self.previously_selected_node, self.background_colour, "bold",
                               self.nodes)
            self.add_node_text(self.previously_selected_node, self.graph_colour, "regular", self.nodes)
            self.add_node_text(x_co, self.background_colour, "regular", self.nodes)
            self.add_node_text(x_co, self.node_selected_arc_colour, "bold", self.nodes)
            self.previously_selected_node = x_co
        else:
            self.change_line_colors_for_point(self.previously_selected_node, self.graph_colour)
            self.add_node_text(self.previously_selected_node, self.graph_colour, "regular", self.nodes)
            self.add_node_text(self.previously_selected_node, self.background_colour, "bold",
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
            self.previously_selected_arc = -1

        if arc_id >= 0 and y_coordinate > 0.2:
            from_node = self.sources[arc_id]
            to_node = self.targets[arc_id]
            line_weight = self.weights[arc_id]
            self.change_arc_color(arc_id, self.selected_line_colour)
            self.previously_selected_arc = arc_id

        # Clear the previously created box in the graph
        delete_textstr = "Nodes  :- {f_node} - {t_node}\nWeight :- {w}".format(
            f_node="Delete this text from node for next time",
            t_node="Delete this text from node for next time",
            w=line_weight)
        props_del = dict(boxstyle='square', facecolor=self.background_colour, edgecolor=self.background_colour,
                         alpha=1, linewidth=2.0)
        self.ax.text(0.03, 0.95, delete_textstr, transform=self.ax.transAxes, fontsize=10,
                     color=self.background_colour, verticalalignment='top', bbox=props_del)

        # Create next details box according to the position clicked in the canvas
        textstr = "Nodes  :- {f_node} - {t_node}\nWeight :- {w}".format(f_node=from_node, t_node=to_node, w=line_weight)
        props = dict(boxstyle='round', facecolor='lightsteelblue', edgecolor='navy', alpha=0.5)
        self.ax.text(0.03, 0.95, textstr, transform=self.ax.transAxes, fontsize=10, fontfamily=self.font_type,
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

    def get_background_colour(self):
        """
        Return the value of background colour for the graph.

        :return: background colour
        """
        return self.background_colour

    def set_graph_colour(self, graph_colour):
        """
        Set the graph(default arcs) colour of the diagram for the plot and
        :return none.

        :param graph_colour: colour to change arcs(default)
        :return: none
        """
        self.graph_colour = graph_colour

    def get_graph_colour(self):
        """
        Return the value of graph(default arcs) colour for the graph.

        :return: graph colour
        """
        return self.graph_colour

    def set_node_selected_arc_colour(self, node_selected_arc_colour):
        """
        Set the colour of the arcs with selected node in the diagram
        :return none.

        :param node_selected_arc_colour: colour to change in arcs with selected node
        :return: none
        """
        self.node_selected_arc_colour = node_selected_arc_colour

    def get_node_selected_arc_colour(self):
        """
        Return the value of colour in arcs with selected node for the graph.

        :return: colour in arcs with selected node
        """
        return self.node_selected_arc_colour

    def set_selected_line_colour(self, selected_line_colour):
        """
        Set the colour of the selected arc in the diagram
        :return none.

        :param selected_line_colour: colour to change in arc selected
        :return: none
        """
        self.selected_line_colour = selected_line_colour

    def get_selected_line_colour(self):
        """
        Return the value of colour in arcs with selected node for the graph.

        :return: colour of the selected arc
        """
        return self.selected_line_colour

    def set_title_font_colour(self, title_font_colour):
        """
        Set the colour of the font in title of the diagram
        :return none.

        :param title_font_colour: colour to change in title of the graph
        :return: none
        """
        self.title_font_colour = title_font_colour

    def get_title_font_colour(self):
        """
        Return the value of colour in title of the graph.

        :return: colour of the font in title of the graph
        """
        return self.title_font_colour

    # Change value of the from weight of the graph
    def set_from_weight(self, from_weight):
        """
        Set value of the from weight used in the graph and return none.

        :param from_weight: value of from weight to change
        :return: none
        """
        self.from_weight = from_weight

    def get_from_weight(self):
        """
        Return value of the from weight in the graph.

        :return: from weight in graph
        """
        return self.from_weight

    def set_to_weight(self, to_weight):
        """
        Set value of the to weight used in the graph and return none.

        :param to_weight: value of to weight to change
        :return: none
        """
        self.to_weight = to_weight

    def get_to_weight(self):
        """
        Return value of the to weight in the graph.

        :return: to weight in graph
        """
        return self.to_weight

    def set_font_size(self, font_size):
        """
        Set font size used in the graph and return none.

        :param font_size: value of font size to change
        :return: none
        """
        self.font_size = font_size

    def get_font_size(self):
        """
        Return the font size in the graph.

        :return: font size in graph
        """
        return self.font_size

    def set_title_font_size(self, title_font_size):
        """
        Set font size of title used in the graph and return none.

        :param title_font_size: value of font size in title to change
        :return: none
        """
        self.title_font_size = title_font_size

    def get_title_font_size(self):
        """
        Return the font size of title in the graph.

        :return: font size of title in graph
        """
        return self.title_font_size

    def set_title(self, title):
        """
        Set title of the graph and return none.

        :param title: title to change
        :return: none
        """
        self.title = title

    def get_title(self):
        """
        Return the title of the graph.

        :return: title of the graph
        """
        return self.title

    def set_line_width_multiplier(self, line_width_multiplier):
        """
        Set value of the line_width_multiplier used in the graph and return none.

        :param line_width_multiplier: value of line width multiplier to change
        :return: none
        """
        self.line_width_multiplier = line_width_multiplier

    def get_line_width_multiplier(self):
        """
        Return value of the line width multiplier in the graph.

        :return: value of the line width multiplier in graph
        """
        return self.line_width_multiplier

    def set_font_type(self, font_type):
        """
        Set font type used in the graph and return none.

        :param font_type: font type to change
        :return: none
        """
        self.font_type = font_type

    def get_font_type(self):
        """
        Return the font type in the graph.

        :return: font type in graph
        """
        return self.font_type

    def set_title_font_type(self, title_font_type):
        """
        Set font type used for title in the graph and return none.

        :param title_font_type: font type to change in title
        :return: none
        """
        self.title_font_type = title_font_type

    def get_title_font_type(self):
        """
        Return the font type of the title in the graph.

        :return: font type of the title in the graph
        """
        return self.title_font_type

    def save_image(self, location):
        """
        Save graph as a image in given location and return None
        :param location: path to save image
        :return: None
        """
        plt.savefig(location, bbox_inches="tight", dpi=150)

    def get_weight_for_two_nodes(self, node_1, node_2):
        """
        Return weight of the arc between given two nodes(if there exist any arc)
        Else return None
        :param node_1: Name of the first node
        :param node_2: Name of the second node
        :return: Weight of the arc between two nodes(or None)
        """
        if (node_1, node_2) in self.lines_with_weights.keys():
            return self.lines_with_weights[(node_1, node_2)]
        elif (node_2, node_1) in self.lines_with_weights.keys():
            return self.lines_with_weights[(node_2, node_1)]
        else:
            return None

    def generate_chart(self):
        """
        Generate chart using values of attributes in the graph and
        :return none.

        :return: none
        """

        self.fig = plt.figure(figsize=(6, 6))
        self.num_of_rows, self.sources, self.targets, self.weights = self.get_information()
        self.nodes, self.positions_of_nodes = self.get_sorted_list_of_nodes_with_positions(self.sources, self.targets)

        self.set_lines_weights_for_no_duplicate_data(self.sources, self.targets, self.weights, self.num_of_rows)
        self.nodes_count = len(self.nodes)

        # Setup window
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim(-5, self.nodes_count / 2 + 1)
        self.ax.set_xlim(-1, self.nodes_count + 1)
        self.ax.axis('off')
        self.fig.set_facecolor(self.background_colour)

        # Position the nodes in the graph
        xs = [i for i in range(self.nodes_count)]
        ys = [0] * self.nodes_count
        points = self.ax.scatter(xs, ys, c=self.graph_colour, marker='o')

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
            self.add_node_text(x_co, self.graph_colour, 'regular', self.nodes)

        # Add events
        self.fig.canvas.mpl_connect('button_press_event', self.click_on_node)
        self.fig.canvas.mpl_connect('button_press_event', self.click_on_arc)

        plt.suptitle(self.title, color=self.title_font_colour,
                     # pad=self.title_font_size * 1.5,
                     fontsize=self.title_font_size,
                     fontweight='bold', fontname=self.title_font_type)

        if self.sub_title != "( Weight range:   -   )":
            plt.title(self.sub_title, color=self.title_font_colour,
                      pad=self.title_font_size * 1.5,
                      fontsize=self.title_font_size // 2,
                      fontname=self.title_font_type)

        self.fig.tight_layout()

        self.from_weight = None
        self.to_weight = None

        return self.fig
