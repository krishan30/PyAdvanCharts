from tkinter import colorchooser, E, W

import customtkinter


def get_arc_modify_box(root, root_parent, arc_diagram, right_frame_width):
    modify_frame = customtkinter.CTkFrame(master=root)

    modify_frame.rowconfigure((1, 2, 3, 4, 5, 7, 9, 10, 11, 12, 13), weight=1)
    modify_frame.rowconfigure((6, 8, 14, 15), weight=5)
    modify_frame.columnconfigure((0, 2), weight=2)
    modify_frame.columnconfigure(1, weight=1)

    # Attributes of the graph
    background_colour = arc_diagram.get_background_colour()
    arc_colour = arc_diagram.get_graph_colour()
    node_selected_arc_colour = arc_diagram.get_node_selected_arc_colour()
    selected_line_colour = arc_diagram.get_selected_line_colour()
    graph_font = arc_diagram.get_font_type()
    graph_font_size = arc_diagram.get_font_size()
    line_width_multiplier = arc_diagram.get_line_width_multiplier()
    from_weight = arc_diagram.get_from_weight()
    to_weight = arc_diagram.get_to_weight()
    graph_title_font_type = arc_diagram.get_title_font_type()
    graph_title_font_size = arc_diagram.get_title_font_size()

    weight = ""

    # set background colour
    def set_background_color():
        nonlocal background_colour
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        background_colour = hex_code

    # set graph(default arcs) colour
    def set_arc_color():
        nonlocal arc_colour
        color_code = colorchooser.askcolor(title="Choose a colour")
        rgb_values, hex_code = color_code
        arc_colour = hex_code

    # set colour of the arcs with selected node
    def set_node_selected_arc_colour():
        nonlocal node_selected_arc_colour
        color_code = colorchooser.askcolor(title="Choose a colour")
        rgb_values, hex_code = color_code
        node_selected_arc_colour = hex_code

    # set colour of the selected arc
    def set_selected_line_colour():
        nonlocal selected_line_colour
        color_code = colorchooser.askcolor(title="Choose a colour")
        rgb_values, hex_code = color_code
        selected_line_colour = hex_code

    # Set font size
    def set_font_size(value):
        nonlocal graph_font_size
        if value is not None:
            graph_font_size = int(value)

    # Set font size in title
    def set_title_font_size(value):
        nonlocal graph_title_font_size
        if value is not None:
            graph_title_font_size = int(value)

    # Set font type
    def set_font_type(choice):
        nonlocal graph_font
        graph_font = choice

    # Set font type in the title
    def set_title_font_type(choice):
        nonlocal graph_title_font_type
        graph_title_font_type = choice

    # Set line width multiplier
    def set_line_width_multiplier_size(value):
        nonlocal line_width_multiplier
        if value is not None:
            line_width_multiplier = int(value)

    # Set font colour of title in arc diagram
    def set_arc_title_font_colour():
        color_code = colorchooser.askcolor(title="Choose a colour")
        rgb_values, hex_code = color_code
        arc_diagram.set_title_font_colour(hex_code)

    # Find weight between given two nodes here
    def find_weight():
        nonlocal weight
        node1 = node_1_text.get()
        node2 = node_2_text.get()
        if node1 and node2:
            weight = arc_diagram.get_weight_for_two_nodes(node1, node2)
            if not weight:
                weight = "No matching arc found"

        else:
            weight = "Enter node 1 & node 2"
        weight_display_label = customtkinter.CTkLabel(master=modify_frame, text=weight, anchor=E,
                                                      fg_color="#1F6AA5", corner_radius=5)
        weight_display_label.grid(row=10, column=2, pady=10, padx=60, sticky="e")

    # Regenerate graph according to the new changes
    def regenerate_graph():
        from modify_body_frames.arc_modify_frame import ArcModify
        nonlocal from_weight, to_weight
        arc_diagram.set_background_colour(background_colour)
        arc_diagram.set_graph_colour(arc_colour)
        arc_diagram.set_node_selected_arc_colour(node_selected_arc_colour)
        arc_diagram.set_selected_line_colour(selected_line_colour)
        arc_diagram.set_font_type(graph_font)
        arc_diagram.set_title_font_type(graph_title_font_type)
        arc_diagram.set_font_size(graph_font_size)
        arc_diagram.set_title_font_size(graph_title_font_size)
        arc_diagram.set_line_width_multiplier(line_width_multiplier)

        title = new_title_text.get()
        if title:
            arc_diagram.set_title(title)

        try:
            from_weight = int(from_weight_text.get())
            arc_diagram.set_from_weight(from_weight)
        except:
            pass

        try:
            to_weight = int(to_weight_text.get())
            arc_diagram.set_to_weight(to_weight)
        except:
            pass

        ArcModify.get_frame(root_parent, arc_diagram, right_frame_width)

    chart_modification_label = customtkinter.CTkLabel(master=modify_frame, text="Chart Customization",
                                                      text_font=("serif", 18))
    chart_modification_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Chart modification options
    chart_configuration_label = customtkinter.CTkLabel(master=modify_frame, text="Chart Modifications",
                                                       text_font=("serif", 15))
    chart_configuration_label.grid(row=1, column=0, pady=10, padx=50, sticky="w")

    # Background color selection
    bg_color_label = customtkinter.CTkLabel(master=modify_frame, text="Background Color :", anchor=E)
    bg_color_label.grid(row=2, column=0, pady=10, padx=50, sticky="w")

    bg_color_btn = customtkinter.CTkButton(master=modify_frame,
                                           text="Choose",
                                           command=set_background_color
                                           )
    bg_color_btn.grid(row=2, column=0, pady=10, padx=70, sticky="e")

    # Arc(normal) color selection
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Arc Line Color :", anchor=E)
    arc_color_label.grid(row=3, column=0, pady=10, padx=50, sticky="w")

    arc_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_arc_color
                                            )
    arc_color_btn.grid(row=3, column=0, pady=10, padx=70, sticky="e")

    # Arcs with selected node color selection
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Arc(Node selected) Color :", anchor=E)
    arc_color_label.grid(row=4, column=0, pady=10, padx=50, sticky="w")

    arc_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_node_selected_arc_colour
                                            )
    arc_color_btn.grid(row=4, column=0, pady=10, padx=70, sticky="e")

    # Selected arc color selection
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Arc(Selected) Color :", anchor=E)
    arc_color_label.grid(row=5, column=0, pady=10, padx=50, sticky="w")

    arc_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_selected_line_colour
                                            )
    arc_color_btn.grid(row=5, column=0, pady=10, padx=70, sticky="e")

    # Font size selection
    font_size_menu_label = customtkinter.CTkLabel(master=modify_frame, text="Font Size :", anchor=E)
    font_size_menu_label.grid(row=6, column=0, pady=10, padx=50, sticky="w")

    font_size_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                 values=[str(i) for i in range(5, 26)],
                                                 command=set_font_size
                                                 )
    font_size_menu.set(arc_diagram.get_font_size())
    font_size_menu.grid(row=6, column=0, pady=10, padx=70, sticky="e")

    # Font type selection
    font_type_menu_label = customtkinter.CTkLabel(master=modify_frame, text="Font Type :", anchor=E)
    font_type_menu_label.grid(row=7, column=0, pady=10, padx=50, sticky="w")

    font_type_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                 values=["sans-serif", "serif", "cursive", "fantasy", "monospace"],
                                                 command=set_font_type)
    font_type_menu.set("serif")
    font_type_menu.grid(row=7, column=0, pady=10, padx=70, sticky="e")

    # Line width selection
    arc_width_label = customtkinter.CTkLabel(master=modify_frame, text="Arc Width Size :", anchor=E)
    arc_width_label.grid(row=8, column=0, pady=10, padx=50, sticky="w")

    arc_width_size_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                      values=[str(i) for i in range(1, 6)],
                                                      command=set_line_width_multiplier_size
                                                      )
    arc_width_size_menu.set(arc_diagram.get_line_width_multiplier())
    arc_width_size_menu.grid(row=8, column=0, pady=10, padx=70, sticky="e")

    # Set weight range
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Weight Range :", anchor=E)
    arc_color_label.grid(row=9, column=0, pady=10, padx=50, sticky="w")

    from_weight_label = customtkinter.CTkLabel(master=modify_frame, text="From Weight:")
    from_weight_label.grid(row=10, column=0, pady=10, padx=100, sticky="w")
    from_weight_text = customtkinter.CTkEntry(master=modify_frame, placeholder_text="Enter from weight here")
    from_weight_text.grid(row=10, column=0, pady=10, padx=70, sticky="e")
    to_weight_label = customtkinter.CTkLabel(master=modify_frame, text="To Weight:")
    to_weight_label.grid(row=11, column=0, pady=10, padx=100, sticky="w")
    to_weight_text = customtkinter.CTkEntry(master=modify_frame, placeholder_text="Enter to weight here")
    to_weight_text.grid(row=11, column=0, pady=10, padx=70, sticky="e")

    # Title modification options
    title_configuration_label = customtkinter.CTkLabel(master=modify_frame, text="Title Modifications",
                                                       text_font=("serif", 15), anchor=W)
    title_configuration_label.grid(row=1, column=2, pady=10, padx=10, sticky="w")

    # Change title
    new_title_label = customtkinter.CTkLabel(master=modify_frame, text="New Title:", anchor=E)
    new_title_label.grid(row=2, column=2, pady=10, padx=10, sticky="w")
    new_title_text = customtkinter.CTkEntry(master=modify_frame, placeholder_text=arc_diagram.get_title())
    new_title_text.grid(row=2, column=2, pady=10, padx=60, sticky="e")

    # Change font colour of the title
    title_font_color_label = customtkinter.CTkLabel(master=modify_frame, text="Title Font Color:", anchor=E)
    title_font_color_label.grid(row=3, column=2, pady=10, padx=10, sticky="w")

    title_font_color_btn = customtkinter.CTkButton(master=modify_frame,
                                                   text="Choose", command=set_arc_title_font_colour
                                                   )
    title_font_color_btn.grid(row=3, column=2, pady=10, padx=60, sticky="e")

    # Font type of the title selection
    title_font_type_label = customtkinter.CTkLabel(master=modify_frame, text="Title Font Type:", anchor=E)
    title_font_type_label.grid(row=4, column=2, pady=10, padx=10, sticky="w")

    title_font_type_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                       values=["sans-serif", "serif", "cursive", "fantasy",
                                                               "monospace"],
                                                       command=set_title_font_type
                                                       )
    title_font_type_menu.set(arc_diagram.get_title_font_type())
    title_font_type_menu.grid(row=4, column=2, pady=10, padx=60, sticky="e")

    # Title font size selection
    title_font_size_label = customtkinter.CTkLabel(master=modify_frame, text="Title Font Size:", anchor=E)
    title_font_size_label.grid(row=5, column=2, pady=10, padx=10, sticky="w")

    title_font_size_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                       values=[str(i) for i in range(5, 41)],
                                                       command=set_title_font_size
                                                       )
    title_font_size_menu.set(str(arc_diagram.get_title_font_size()))
    title_font_size_menu.grid(row=5, column=2, pady=10, padx=60, sticky="e")

    # Find weight section
    title_configuration_label = customtkinter.CTkLabel(master=modify_frame, text="Find Weight",
                                                       text_font=("serif", 15), anchor=W)
    title_configuration_label.grid(row=7, column=2, pady=10, padx=10, sticky="w")

    # Node 1 details enter here
    node_1_label = customtkinter.CTkLabel(master=modify_frame, text="Node 1:", anchor=E)
    node_1_label.grid(row=8, column=2, pady=10, padx=10, sticky="w")
    node_1_text = customtkinter.CTkEntry(master=modify_frame, placeholder_text="Enter node 1 name here")
    node_1_text.grid(row=8, column=2, pady=10, padx=60, sticky="e")

    # Node 2 details enter here
    node_2_label = customtkinter.CTkLabel(master=modify_frame, text="Node 2:", anchor=E)
    node_2_label.grid(row=9, column=2, pady=10, padx=10, sticky="w")
    node_2_text = customtkinter.CTkEntry(master=modify_frame, placeholder_text="Enter node 2 name here")
    node_2_text.grid(row=9, column=2, pady=10, padx=60, sticky="e")

    # Weight between two nodes display here
    weight_label = customtkinter.CTkLabel(master=modify_frame, text="Weight:", anchor=E)
    weight_label.grid(row=10, column=2, pady=10, padx=10, sticky="w")
    weight_display_label = customtkinter.CTkLabel(master=modify_frame, text=weight, anchor=E,
                                                  fg_color="#1F6AA5", corner_radius=5)
    weight_display_label.grid(row=10, column=2, pady=10, padx=60, sticky="e")

    # Find weight button
    find_weight_btn = customtkinter.CTkButton(master=modify_frame,
                                              text="Find weight",
                                              command=find_weight
                                              )
    find_weight_btn.grid(row=11, column=2, pady=10, padx=60)

    # regenerate graph button
    regenerate_graph_btn = customtkinter.CTkButton(master=modify_frame,
                                                   text="Apply Changes",
                                                   command=regenerate_graph
                                                   )
    regenerate_graph_btn.grid(row=13, column=0, columnspan=3, pady=10, padx=0)

    return modify_frame
