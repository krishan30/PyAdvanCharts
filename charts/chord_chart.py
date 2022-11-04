# Import Libraries

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.colors import ColorConverter, LinearSegmentedColormap
from matplotlib.colors import is_color_like

import pandas as pd
import networkx as nx
from scipy.ndimage import gaussian_filter
import numpy as np

"""
 To generate the chord chart and store the relevant attributes and provide interface to manipulate them
"""


class ChordChart:
    LINE_WIDTH = 0.3  # Line Width (Class Variable)

    def __init__(self, path=None, data_frame=None):
        if data_frame is None:
            data_frame = pd.read_csv(path)
        column_names = list(data_frame.columns)
        network_graph = nx.from_pandas_edgelist(data_frame, column_names[0], column_names[1],
                                                column_names[2])  # create networkx graph from dataframe
        adjacency_matrix = nx.to_pandas_adjacency(network_graph,
                                                  weight=column_names[2])  # create adjacency matrix from graph
        self.__node_names = list(adjacency_matrix.columns)
        self.__flux_matrix = adjacency_matrix.to_numpy()
        self.__title = "Chord Chart"
        self.__gap = 0.03
        self.__font_colour = "Black"
        self.__font_size = 7.5
        self.__font_type = 'sans-serif'
        self.__attribute_colour_map = 'viridis'
        self.__background_colour = "white"
        self.__title_font_colour = "Black"
        self.__title_font_type = 'sans-serif'
        self.__title_font_size = 20
        self.__alpha = 0.7
        self.__radius = 1.
        self.__width = 0.1
        self.__padding = 2.
        self.__chord_width = 0.7
        self.__start = 0
        self.__extent = 360
        self.__figure, self.__ax = None, None
        self.__patch = None

    """
    To change the colour scheme of the chart
    :parameters
        colour_map_index:The relevant index of the colour map
    """

    def change_attribute_colour_map(self, colour_map):
        colour_maps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        if colour_map not in colour_maps:
            return None
        else:
            self.__attribute_colour_map = colour_map
            return colour_map

    def get_attribute_colour_map(self):
        return self.__attribute_colour_map

    def get_title(self):
        return self.__title

    def change_background_colour(self, background_colour):
        if not (is_color_like(background_colour)):
            return None
        else:
            self.__background_colour = background_colour
            return background_colour

    def change_title_font_type(self, new_font_type):
        if new_font_type:
            self.__title_font_type = new_font_type
            return True
        else:
            return False

    def get_title_font_type(self):
        return self.__title_font_type

    def change_title_font_size(self, new_font_size):
        if 5 <= int(new_font_size) <= 40:
            self.__title_font_size = int(new_font_size)
            return True
        else:
            return False

    def get_title_font_size(self):
        return self.__title_font_size

    def change_title_font_colour(self, new_font_colour):
        if is_color_like(new_font_colour):
            self.__title_font_colour = new_font_colour
            return True
        else:
            return False

    def change_font_type(self, new_font_type):
        if new_font_type:
            self.__font_type = new_font_type
            return True
        else:
            return False

    def get_font_type(self):
        return self.__font_type

    """
    To change the title of the chart
    
    :parameters
    new_tittle-new title for the chord chart
    """

    def change_title(self, new_title):
        if not new_title:
            return False
        else:
            self.__title = new_title
            return True

    """
    To change the font colour of the chart
    
    :parameters
    new_colour-new colour for the font
    """

    def change_font_colour(self, new_colour):
        if is_color_like(new_colour):
            self.__font_colour = new_colour
            return True
        else:
            return False

    """
    To create the initial arc base
    
    :parameter
    start_degree-starting angle of the arc(polar)
    end_degree-ending angle of the arc(polar)
    radius-radius of the arc
    
    :return
    vertices-16 vertices coordination for draw the arc
    path_instructions-instruction for the patch to draw the arc
    """

    @classmethod
    def __arc_generator(cls, start_degree, end_degree, radius):
        if start_degree > end_degree:
            start_degree, end_degree = end_degree, start_degree

        factor = 4 / 3
        start_degree *= np.pi / 180.
        end_degree *= np.pi / 180.

        optimal_distance = factor * np.tan((end_degree - start_degree) / 16.) * radius
        inter_degree_1 = start_degree * (3. / 4.) + end_degree * (1. / 4.)
        inter_degree_2 = start_degree * (2. / 4.) + end_degree * (2. / 4.)
        inter_degree_3 = start_degree * (1. / 4.) + end_degree * (3. / 4.)

        vertices = [
            ChordChart.__polar_to_xy_convertor(radius, start_degree),
            ChordChart.__polar_to_xy_convertor(radius, start_degree) + ChordChart.__polar_to_xy_convertor(
                optimal_distance,
                start_degree + 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_1) + ChordChart.__polar_to_xy_convertor(
                optimal_distance,
                inter_degree_1 - 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_1),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_1),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_1) + ChordChart.__polar_to_xy_convertor(
                optimal_distance,
                inter_degree_1 + 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_2) + ChordChart.__polar_to_xy_convertor(
                optimal_distance,
                inter_degree_2 - 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_2),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_2),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_2) + ChordChart.__polar_to_xy_convertor(
                optimal_distance,
                inter_degree_2 + 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_3) + ChordChart.__polar_to_xy_convertor(
                optimal_distance,
                inter_degree_3 - 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_3),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_3),
            ChordChart.__polar_to_xy_convertor(radius, inter_degree_3) + ChordChart.__polar_to_xy_convertor(
                optimal_distance,
                inter_degree_3 + 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(radius, end_degree) + ChordChart.__polar_to_xy_convertor(
                optimal_distance,
                end_degree - 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(radius, end_degree)
        ]

        path_instructions = [
            Path.MOVETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
        ]

        return start_degree, end_degree, vertices, path_instructions

    """
    To create the chord arc of chart with width
    
    :parameter
        start_degree-starting angle of the arc(polar)
        end_degree-ending angle of the arc(polar)
        color-colour of the arc
        """

    def __ideogram_arc(self, start_degree, final_degree, color):
        start_degree, final_degree, vertices, path_instructions = ChordChart.__arc_generator(start_degree, final_degree,
                                                                                             self.__radius)

        optimal_distance = 4. / 3. * np.tan((final_degree - start_degree) / 16.) * self.__radius
        inner_radius = self.__radius * (1 - self.__width)
        inter_degree_1 = start_degree * (3. / 4.) + final_degree * (1. / 4.)
        inter_degree_2 = start_degree * (2. / 4.) + final_degree * (2. / 4.)
        inter_degree_3 = start_degree * (1. / 4.) + final_degree * (3. / 4.)

        vertices += [
            ChordChart.__polar_to_xy_convertor(inner_radius, final_degree),
            ChordChart.__polar_to_xy_convertor(inner_radius, final_degree) + ChordChart.__polar_to_xy_convertor(
                optimal_distance * (1 - self.__width),
                final_degree - 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_3) + ChordChart.__polar_to_xy_convertor(
                optimal_distance * (1 - self.__width),
                inter_degree_3 + 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_3),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_3),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_3) + ChordChart.__polar_to_xy_convertor(
                optimal_distance * (1 - self.__width),
                inter_degree_3 - 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_2) + ChordChart.__polar_to_xy_convertor(
                optimal_distance * (1 - self.__width),
                inter_degree_2 + 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_2),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_2),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_2) + ChordChart.__polar_to_xy_convertor(
                optimal_distance * (1 - self.__width),
                inter_degree_2 - 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_1) + ChordChart.__polar_to_xy_convertor(
                optimal_distance * (1 - self.__width),
                inter_degree_1 + 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_1),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_1),
            ChordChart.__polar_to_xy_convertor(inner_radius, inter_degree_1) + ChordChart.__polar_to_xy_convertor(
                optimal_distance * (1 - self.__width),
                inter_degree_1 - 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(inner_radius, start_degree) + ChordChart.__polar_to_xy_convertor(
                optimal_distance * (1 - self.__width),
                start_degree + 0.5 * np.pi),
            ChordChart.__polar_to_xy_convertor(inner_radius, start_degree),
            ChordChart.__polar_to_xy_convertor(self.__radius, start_degree),
        ]

        path_instructions += [
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CLOSEPOLY,
        ]

        path = Path(vertices, path_instructions)
        self.__patch = patches.PathPatch(path, facecolor=color, alpha=self.__alpha, edgecolor=color,
                                         lw=ChordChart.LINE_WIDTH, )

        self.__ax.add_patch(self.__patch)



    """
    To draw a chord in the chart that going from one arc to other connecting arc
    
    :parameter
        start_degree_1-staring angle
        final_degree_1-ending angle
        start_degree_2-staring  angle
        final_degree_2-ending angle
        radius-radius of the chord
        color_start-Color of the chord at the beginning
        color_end-Colour of the chord at the ending
    """

    def __chord_arc(self, start_degree_1, final_degree_1, start_degree_2, final_degree_2, radius, color_start,
                    color_end):
        chord_width = self.__chord_width
        chord_width_2 = self.__chord_width
        d_theta_1 = min((start_degree_1 - final_degree_2) % self.__extent,
                        (final_degree_2 - start_degree_1) % self.__extent)
        d_theta_2 = min((final_degree_1 - start_degree_2) % self.__extent,
                        (start_degree_2 - final_degree_1) % self.__extent)

        start_degree_1, final_degree_1, vertices_1, path_instructions = ChordChart.__arc_generator(start_degree_1,
                                                                                                   final_degree_1,
                                                                                                   radius)
        start_degree_2, final_degree_2, vertices_2, _ = ChordChart.__arc_generator(start_degree_2, final_degree_2,
                                                                                   radius)

        chord_width_2 *= np.clip(0.4 + (d_theta_1 - 2 * self.__padding) / (15 * self.__padding), 0.2, 1)

        chord_width *= np.clip(0.4 + (d_theta_2 - 2 * self.__padding) / (15 * self.__padding), 0.2, 1)

        radius_chord_1 = radius * (1 - chord_width)
        radius_chord_2 = radius * (1 - chord_width_2)

        vertices_1 += [ChordChart.__polar_to_xy_convertor(radius_chord_1, final_degree_1),
                       ChordChart.__polar_to_xy_convertor(radius_chord_1, start_degree_2)] + vertices_2

        vertices_1 += [
            ChordChart.__polar_to_xy_convertor(radius_chord_2, final_degree_2),
            ChordChart.__polar_to_xy_convertor(radius_chord_2, start_degree_1),
            ChordChart.__polar_to_xy_convertor(radius, start_degree_1),
        ]

        path_instructions += [
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.LINETO,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
        ]

        path = Path(vertices_1, path_instructions)

        # calculating the begin and final points of the gradient
        points, min_angle = None, None

        if d_theta_1 < d_theta_2:
            points = [
                ChordChart.__polar_to_xy_convertor(radius, start_degree_1),
                ChordChart.__polar_to_xy_convertor(radius, final_degree_2),
            ]

            min_angle = d_theta_1
        else:
            points = [
                ChordChart.__polar_to_xy_convertor(radius, final_degree_1),
                ChordChart.__polar_to_xy_convertor(radius, start_degree_2),
            ]

            min_angle = d_theta_2

        # creating the patch
        #patch = patches.PathPatch(path, facecolor="none", edgecolor="none", lw=ChordChart.LINE_WIDTH)
        patch = patches.PathPatch(path, facecolor=color_start, alpha=self.__alpha,edgecolor=color_start, lw=ChordChart.LINE_WIDTH)
        self.__ax.add_patch(patch)

        # creating the grid
        x = y = np.linspace(-1, 1, 100)
        mesh_grid = np.meshgrid(x, y)

        self.__gradient(points[0], points[1], min_angle, color_start, color_end, mesh_grid, patch)

    """
    To draw a chord that going from an arc to itself
    
    :parameter
        start_degree-staring angle
        end_degree-ending angle
        radius-radius of the chord
        chord_width-width of the chord
        color-colour of the chord
    """

    def __self_chord_arc(self, start_degree, end_degree, radius, chord_width, color):
        start_degree, end_degree, vertices, path_instructions = ChordChart.__arc_generator(start_degree, end_degree,
                                                                                           radius)
        radius_chord = radius * (1 - chord_width)

        vertices += [
            ChordChart.__polar_to_xy_convertor(radius_chord, end_degree),
            ChordChart.__polar_to_xy_convertor(radius_chord, start_degree),
            ChordChart.__polar_to_xy_convertor(radius, start_degree),
        ]

        path_instructions += [
            Path.CURVE4,
            Path.CURVE4,
            Path.CURVE4,
        ]

        path = Path(vertices, path_instructions)
        patch = patches.PathPatch(path, facecolor=color, alpha=self.__alpha, edgecolor=color,
                                  lw=ChordChart.LINE_WIDTH)
        self.__ax.add_patch(patch)

    """
    To generate the chord chart
    
    :parameter
    
    :return
        figure object
    """

    def generate_graph(self):
        self.__figure, self.__ax = plt.subplots()
        self.__patch = None
        flux_matrix = np.array(self.__flux_matrix, copy=True)
        num_nodes = flux_matrix.shape[0]
        rotate_names = [True] * num_nodes

        # colour configuration
        attributes_color = np.linspace(0, 1, num_nodes)
        cm = plt.get_cmap(self.__attribute_colour_map)
        attributes_color = cm(attributes_color)[:, :3]

        fontcolor = [self.__font_colour] * num_nodes
        chord_colors = attributes_color

        out_deg = flux_matrix.sum(axis=1)
        in_deg = None
        degree = out_deg.copy()

        position = {}
        arcs = []
        node_position = []
        rotation = []
        ChordChart.__compute_positions(flux_matrix, degree, self.__start, self.__extent, self.__padding, arcs,
                                       rotation, node_position, position)
        # plotting
        for i in range(num_nodes):
            color = attributes_color[i]
            x_pos, y_pos, _ = node_position[i]
            """self.__ax.annotate(
                'angle,\nshrink',
                xy=(x_pos, y_pos), xycoords='data',
                xytext=(x_pos+10, y_pos), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                shrinkA=0, shrinkB=10,
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"))"""
            # plotting the arcs
            start_at, end = arcs[i]

            self.__ideogram_arc(start_degree=start_at, final_degree=end, color=color)

            chord_color = chord_colors[i]
            # plotting the self chords
            if flux_matrix[i, i]:
                start_1, end_1, _, _ = position[(i, i)]
                self.__self_chord_arc(start_1, end_1, radius=self.__radius - self.__width - self.__gap,
                                      chord_width=0.7 * self.__chord_width, color=chord_color)

            # plot chords that are not self chords
            targets = range(i)

            for j in targets:
                colour_end = chord_colors[j]

                start_1, end_1, start_2, end_2 = position[(i, j)]

                if flux_matrix[i, j] > 0 or (flux_matrix[j, i] > 0):
                    self.__chord_arc(start_1, end_1, start_2, end_2, radius=self.__radius - self.__width - self.__gap,
                                     color_start=chord_color, color_end=colour_end)

        properties = {
            "fontsize": self.__font_size,
            "ha": "center",
            "va": "center",
            "rotation_mode": "anchor"
        }

        for i, (position, name, r) in enumerate(zip(node_position, self.__node_names, rotation)):
            rotate = rotate_names[i]
            pp = properties.copy()
            pp["color"] = fontcolor[i]
            if rotate:
                angle = np.average(arcs[i])
                rotate = 90

                if 90 < angle < 180 or 270 < angle:
                    rotate = -90

                if 90 < angle < 270:
                    pp["ha"] = "right"
                else:
                    pp["ha"] = "left"
            elif r:
                pp["va"] = "top"
            else:
                pp["va"] = "bottom"

            self.__ax.text(position[0], position[1], name, rotation=position[2] + rotate, fontname=self.__font_type,
                           **pp)

        # axis configuration
        self.__ax.set_xlim(-1.1, 1.1)
        self.__ax.set_ylim(-1.1, 1.1)

        self.__ax.set_aspect(1)
        self.__ax.axis('off')
        # adding the title
        plt.title(self.__title, color=self.__title_font_colour, pad=self.__title_font_size * 1.5,
                  fontsize=self.__title_font_size,
                  fontweight='bold', fontname=self.__title_font_type)
        plt.tight_layout()
        # adding the background colour
        self.__figure.patch.set_facecolor(self.__background_colour)

        return self.__figure

    """
    To calculate the distance between two points
    
    :parameter
        points-coordinates of the two points as [(x1,y1),(x2,y2)]
    
    :return
        float
    """

    @classmethod
    def __distance(cls, points):
        x1, y1 = points[0]
        x2, y2 = points[1]

        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    """
    To convert the polar form to xy form
    
    :parameter
        radius-radius of the circle
        angle-angle in radian
    
    :return
        numpy array as [x,y]
    """

    @classmethod
    def __polar_to_xy_convertor(cls, radius, angle):
        return np.array([radius * np.cos(angle), radius * np.sin(angle)])

    """
    To calculate the positions of the arcs,chords and attribute names
    
    :parameter
        matrix-adjacency matrix of network data
        degrees-list of angles for each arc
        start_at-starting angle of first arc
        extent-ending angle of last arc
        padding-gap between arcs
        arc-starting and ending positions of the arcs
        rotation-store whether the attribute rotate
        node_position-store attribute positions
        position- Store the start and end positions for each arc under the form:
            (start1, end1, start2, end2), where (start1, end1) are the limits of the
            chords starting point, and (start2, end2) are the limits of the chord's
            end point.
    """

    @classmethod
    def __compute_positions(cls, matrix, degrees, start_at, extent, padding, arc, rotation, node_position,
                            position):
        num_nodes = len(degrees)
        # calculating the position for each begin and final
        y = degrees / np.sum(degrees).astype(float) * (extent - padding * num_nodes)

        starts = [start_at] + (start_at + np.cumsum(y + padding * np.ones(num_nodes))).tolist()

        out_ends = [s + d for s, d in zip(starts, y)]

        # relative positions within an arc
        z_matrix = [ChordChart.__get_normed_line(matrix, i, degrees, starts[i], out_ends[i]) for i in range(num_nodes)]

        zin_matrix = z_matrix

        matrix_ids = ChordChart.__get_sorted_ids(num_nodes)

        # computing positions
        for i in range(num_nodes):
            start = starts[i]
            end = start + y[i]
            arc.append((start, end))
            angle = 0.5 * (start + end)

            if -30 <= (angle % 360) <= 180:
                angle -= 90
                rotation.append(False)
            else:
                angle -= 270
                rotation.append(True)

            node_position.append(
                tuple(ChordChart.__polar_to_xy_convertor(1.05, 0.5 * (start + end) * np.pi / 180.)) + (angle,))
            z = z_matrix[i]
            z0 = start

            for j in matrix_ids[i]:
                # computing arrival points
                zj = zin_matrix[j]
                start_j = starts[j]
                jids = matrix_ids[j]
                stop = np.where(np.equal(jids, i))[0][0]
                startji = start_j + zj[jids[:stop]].sum()
                position[(i, j)] = (z0, z0 + z[j], startji, startji + zj[jids[stop]])

                z0 += z[j]

    """
    To sort the chords order in a predefined way within an arc
    
    :parameter
        num_nodes-number of arcs in the chord diagram
    :return
        list with indices for order of the chords within arcs(matrix)    
    """

    @classmethod
    def __get_sorted_ids(cls, num_nodes):
        matrix_ids = []
        remainder = 0 if num_nodes % 2 else -1
        for i in range(num_nodes):
            ids = list(range(i - int(0.5 * num_nodes), i))[::-1]

            ids += [i]

            ids += list(range(i + int(0.5 * num_nodes) + remainder, i, -1))

            ids = np.array(ids)
            ids[ids < 0] += num_nodes
            ids[ids >= num_nodes] -= num_nodes

            matrix_ids.append(ids)

        return matrix_ids

    @classmethod
    def __get_normed_line(cls, matrix, i, x, start, end):
        return (matrix[i, :] / x[i]) * (end - start)

    """
    To generate colour transition from start to end
    :parameter
        starting_colour
        final_colour
        no_of_colours-no of colour transition needed
    :return
        list with indices for order of the chords within arcs(matrix)    
    """

    @classmethod
    def __linear_gradient(cls, starting_colour, final_colour, no_of_colours=10):
        start = np.array(ColorConverter.to_rgb(starting_colour))
        final = np.array(ColorConverter.to_rgb(final_colour))

        rgb_colour_list = []
        for i in range(no_of_colours):
            rgb_colour_list.append(start + (i / (no_of_colours - 1)) * (final - start))

        return rgb_colour_list

    """
    To apply the colour transition from starting colour to ending colour for a chord   
    """

    def __gradient(self, start_position, end_position, minimum_angle, color_1, color_2, mesh_grid, mask):
        x_start, y_start = start_position
        x_end, y_end = end_position

        X, Y = mesh_grid

        # get the distance to each point
        distance_to_start = (X - x_start) ** 2 + (Y - y_start) ** 2
        distance_to_end = (X - x_end) ** 2 + (Y - y_end) ** 2

        distance_maximum = (x_start - x_end) ** 2 + (y_start - y_end) ** 2

        # blur
        s_min = 0.015 * len(X)
        s_max = max(s_min, 0.1 * len(X) * min(minimum_angle / 120, 1))

        sigma = np.clip(distance_maximum * len(X), s_min, s_max)

        Z = gaussian_filter((distance_to_end < distance_to_start).astype(float), sigma=sigma)

        # generate the colormap
        n_bin = 100

        color_list = ChordChart.__linear_gradient(color_1, color_2, n_bin)

        c_map = LinearSegmentedColormap.from_list("gradient", color_list, N=n_bin)

        im = self.__ax.imshow(Z, interpolation='bilinear', cmap=c_map,
                              origin='lower', extent=[-1, 1, -1, 1], alpha=self.__alpha)

        im.set_clip_path(mask)
