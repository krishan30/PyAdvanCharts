from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# function for drawing our sankey chart
def draw_sankey(root,sankeychart):
    #sankeychart = SankeyChart(file)
    figure = sankeychart.generate_chart()

    chart = FigureCanvasTkAgg(figure, root)
    return chart
    # chart.get_tk_widget().grid(row=1, column=2,columnspan=2, rowspan=4, pady=2, padx=20, sticky="ns")


# function for drawing  chord chart
def draw_chord(root, chord_diagram):
    figure = chord_diagram.generate_graph()
    chart = FigureCanvasTkAgg(figure, root)
    return chart


# function for drawing arc diagram
def draw_arc_diag(root, arc_diagram):
    figure = arc_diagram.generate_chart()

    chart = FigureCanvasTkAgg(figure, root)
    return chart


