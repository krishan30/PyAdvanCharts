from tkinter import colorchooser

import customtkinter


def get_arc_modify_box(root, root_parent, arc_diagram):
    modify_frame = customtkinter.CTkFrame(master=root)

    modify_frame.rowconfigure((1, 2, 3, 4, 6), weight=1)
    modify_frame.rowconfigure((7, 8, 9, 10, 11, 12), weight=5)
    modify_frame.columnconfigure((0, 1, 2, 3), weight=1)

    # Attributes of the graph
    background_colour = arc_diagram.get_background_colour()
    arc_colour = arc_diagram.get_graph_colour()
    node_selected_arc_colour = arc_diagram.get_node_selected_arc_colour()
    selected_line_colour = arc_diagram.get_selected_line_colour()
    graph_font = arc_diagram.get_font_type()
    graph_font_size = arc_diagram.get_font_size()

    # set background colour
    def set_background_color():
        nonlocal background_colour
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        background_colour = hex_code

    # set graph(default arcs) colour
    def set_arc_color():
        nonlocal arc_colour
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        arc_colour = hex_code

    # set colour of the arcs with selected node
    def set_node_selected_arc_colour():
        nonlocal node_selected_arc_colour
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        node_selected_arc_colour = hex_code

    # set colour of the selected arc
    def set_selected_line_colour():
        nonlocal selected_line_colour
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        selected_line_colour = hex_code

    # Set font size
    def set_font_size(value):
        nonlocal graph_font_size
        #print(type(value))
        if value is not None:
            graph_font_size = int(value)

    # Set font type
    def set_font_type(choice):
        nonlocal graph_font
        graph_font = choice
        #print("Pre-test", graph_font)

    # Regenerate graph according to the new changes
    def regenerate_graph():
        from modify_body_frames.arc_modify_frame import ArcModify
        arc_diagram.set_background_colour(background_colour)
        arc_diagram.set_graph_colour(arc_colour)
        arc_diagram.set_node_selected_arc_colour(node_selected_arc_colour)
        arc_diagram.set_selected_line_colour(selected_line_colour)
        arc_diagram.set_font_type(graph_font)
        # print(graph_font_size)
        arc_diagram.set_font_size(graph_font_size)
        ArcModify.get_frame(root_parent, arc_diagram)

    # bg color selection
    bg_color_label = customtkinter.CTkLabel(master=modify_frame, text="BG Color :")
    bg_color_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    bg_color_btn = customtkinter.CTkButton(master=modify_frame,
                                           text="Choose",
                                           command=set_background_color
                                           )
    bg_color_btn.grid(row=0, column=0, pady=10, padx=10, sticky="e")

    # arc(normal) color selection
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Arc Color :")
    arc_color_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    arc_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_arc_color
                                            )
    arc_color_btn.grid(row=1, column=0, pady=10, padx=10, sticky="e")

    # arcs with selected node color selection
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Arc(Node selected) Color :")
    arc_color_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

    arc_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_node_selected_arc_colour
                                            )
    arc_color_btn.grid(row=2, column=0, pady=10, padx=10, sticky="e")

    # selected arc color selection
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Arc(Selected) Color :")
    arc_color_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    arc_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_selected_line_colour
                                            )
    arc_color_btn.grid(row=3, column=0, pady=10, padx=10, sticky="e")

    # change font size
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Font Size :")
    arc_color_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")

    slider = customtkinter.CTkSlider(master=modify_frame, from_=5, to=15, command=set_font_size,
                                     number_of_steps=10)
    slider.grid(row=4, column=0, pady=10, padx=10, sticky="e")

    # Font type selection
    font_type_label = customtkinter.CTkLabel(master=modify_frame, text="Font Type :")
    font_type_label.grid(row=5, column=0, pady=10, padx=10, sticky="w")

    font_type_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                 values=["sans-serif", "serif", "cursive", "fantasy", "monospace"],
                                                 command=set_font_type)
    font_type_menu.set("sans-serif")
    font_type_menu.grid(row=5, column=0, pady=10, padx=10, sticky="e")

    # regenerate graph button
    regenerate_graph_btn = customtkinter.CTkButton(master=modify_frame,
                                                   text="Apply Changes",
                                                   command=regenerate_graph
                                                   )
    regenerate_graph_btn.grid(row=10, column=1, columnspan=2, pady=10, padx=10)

    return modify_frame
