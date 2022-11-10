from tkinter import colorchooser, CENTER, SE, W, E

import customtkinter



def get_chord_modify_box(root, root_parent, chord_diagram, right_frame_width):
    modify_frame = customtkinter.CTkFrame(master=root)

    modify_frame.rowconfigure((1, 2, 3, 4, 6), weight=1)
    modify_frame.rowconfigure((7, 8, 9, 10, 11, 12), weight=5)
    modify_frame.columnconfigure((0, 1, 2, 3), weight=1)

    # bg_color_btn = customtkinter.CTkButton(master=modify_frame,
    # text="Choose",
    # command=set_background_theme
    # )
    # bg_color_btn.grid(row=0, column=0, pady=10, padx=10, sticky="e")
    # arc(normal) color selection
    # set graph(default arcs) colour
    def set_chord_font_color():
        color_code = colorchooser.askcolor(title="Choose a colour")
        rgb_values, hex_code = color_code
        chord_diagram.change_font_colour(hex_code)

    def set_chord_background_color():
        color_code = colorchooser.askcolor(title="Choose a colour")
        rgb_values, hex_code = color_code
        chord_diagram.change_background_colour(hex_code)

    def set_chord_title_font_colour():
        color_code = colorchooser.askcolor(title="Choose a colour")
        rgb_values, hex_code = color_code
        chord_diagram.change_title_font_colour(hex_code)

    def regenerate_graph():
        from modify_body_frames.chord_modify_frame import ChordModify
        title = new_title_text.get()
        if title:
            chord_diagram.change_title(title)
        ChordModify.get_frame(root_parent, chord_diagram, right_frame_width)

    chart_modification_label = customtkinter.CTkLabel(master=modify_frame, text="Chart Customization",
                                                      text_font=("serif", 18))
    chart_modification_label.grid(row=0, column=0, columnspan=4, padx=50, pady=10)

    chart_configuration_label = customtkinter.CTkLabel(master=modify_frame, text="Chart Modifications",
                                                       text_font=("serif", 15))
    chart_configuration_label.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="w")
    options = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
    # bg color selection
    bg_color_label = customtkinter.CTkLabel(master=modify_frame, text="Chart Colour Theme:", anchor=E)
    bg_color_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
    diagram_theme_dropdown_menu = customtkinter.CTkOptionMenu(master=modify_frame, values=options,
                                                              command=chord_diagram.change_attribute_colour_map)
    diagram_theme_dropdown_menu.set(chord_diagram.get_attribute_colour_map())
    diagram_theme_dropdown_menu.grid(row=2, column=0, pady=10, padx=10, sticky="e")

    font_color_label = customtkinter.CTkLabel(master=modify_frame, text="Label Font colour:", anchor=E)
    font_color_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    font_color_btn = customtkinter.CTkButton(master=modify_frame,
                                             text="Choose", command=set_chord_font_color
                                             )
    font_color_btn.grid(row=3, column=0, pady=10, padx=10, sticky="e")

    font_type_label = customtkinter.CTkLabel(master=modify_frame, text="Label Font Type:", anchor=E)
    font_type_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")

    font_type_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                 values=["sans-serif", "serif", "cursive", "fantasy",
                                                         "monospace"],
                                                 command=chord_diagram.change_font_type
                                                 )
    font_type_menu.set(chord_diagram.get_font_type())
    font_type_menu.grid(row=4, column=0, pady=10, padx=10, sticky="e")
    # arcs with selected node color selection
    chord_background_color_label = customtkinter.CTkLabel(master=modify_frame, text="Chart Background Color:", anchor=E)
    chord_background_color_label.grid(row=5, column=0, pady=10, padx=10, sticky="w")

    chord_background_color_btn = customtkinter.CTkButton(master=modify_frame,
                                                         text="Choose", command=set_chord_background_color
                                                         )
    chord_background_color_btn.grid(row=5, column=0, pady=10, padx=10, sticky="e")

    title_configuration_label = customtkinter.CTkLabel(master=modify_frame, text="Title Modifications",
                                                       text_font=("serif", 15), anchor=W)
    title_configuration_label.grid(row=1, column=3, columnspan=2, pady=10, padx=10, sticky="w")
    new_title_label = customtkinter.CTkLabel(master=modify_frame, text="New Title:", anchor=E)
    new_title_label.grid(row=2, column=3, pady=10, padx=10, sticky="w")

    new_title_text = customtkinter.CTkEntry(master=modify_frame, placeholder_text=chord_diagram.get_title())
    new_title_text.grid(row=2, column=3, pady=10, padx=10, sticky="e")
    # selected arc color selection
    title_font_color_label = customtkinter.CTkLabel(master=modify_frame, text="Title Font Color:", anchor=E)
    title_font_color_label.grid(row=3, column=3, pady=10, padx=10, sticky="w")

    title_font_color_btn = customtkinter.CTkButton(master=modify_frame,
                                                   text="Choose", command=set_chord_title_font_colour
                                                   )
    title_font_color_btn.grid(row=3, column=3, pady=10, padx=10, sticky="e")

    # change font size
    title_font_type_label = customtkinter.CTkLabel(master=modify_frame, text="Title Font Type:", anchor=E)
    title_font_type_label.grid(row=4, column=3, pady=10, padx=10, sticky="w")

    title_font_type_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                       values=["sans-serif", "serif", "cursive", "fantasy",
                                                               "monospace"],
                                                       command=chord_diagram.change_title_font_type
                                                       )
    title_font_type_menu.set(chord_diagram.get_title_font_type())
    title_font_type_menu.grid(row=4, column=3, pady=10, padx=10, sticky="e")

    # Font type selection
    title_font_size_label = customtkinter.CTkLabel(master=modify_frame, text="Title Font Size:", anchor=E)
    title_font_size_label.grid(row=5, column=3, pady=10, padx=10, sticky="w")

    title_font_size_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                       values=[str(i) for i in range(5, 41)],
                                                       command=chord_diagram.change_title_font_size
                                                       )
    title_font_size_menu.set(str(chord_diagram.get_title_font_size()))
    title_font_size_menu.grid(row=5, column=3, pady=10, padx=10, sticky="e")
    # regenerate graph button
    regenerate_graph_btn = customtkinter.CTkButton(master=modify_frame,
                                                   text="Apply Changes", command=regenerate_graph,height=40, width=180)
    regenerate_graph_btn.grid(row=8, column=0, columnspan=4, pady=10, padx=10)

    return modify_frame
