import customtkinter
from tkinter import colorchooser


def get_arc_modify_box(root, background_colour="white"):
    modify_frame = customtkinter.CTkFrame(master=root)

    modify_frame.rowconfigure((1, 2, 3, 4, 6), weight=1)
    modify_frame.rowconfigure((7, 8, 9, 10, 11, 12), weight=5)
    modify_frame.columnconfigure((0, 1, 2, 3), weight=1)

    # Attributes of the graph
    background_colour = background_colour

    # set background colour
    def set_background_color():
        global background_colour
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        background_colour = hex_code

    # set background colour
    def set_arc_color():
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        arc_colour = hex_code

    # set background colour
    def set_arc_selected_color():
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        selected_arc_colour = hex_code

    # Set font size
    def set_font_size(value):
        font_size = value

    # Set font type
    def set_font_type(choice):
        font_type = choice

    def regenerate_graph():
        # from helpers.modify_frame_factory import ModifyFrameFactory
        # root.frame_right=ModifyFrameFactory.get_modify_frame(2, root, "red")
        pass

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

    # selected arc color selection
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Arc(Selected) Color :")
    arc_color_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

    arc_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_arc_selected_color
                                            )
    arc_color_btn.grid(row=2, column=0, pady=10, padx=10, sticky="e")

    # change font size
    arc_color_label = customtkinter.CTkLabel(master=modify_frame, text="Font Size :")
    arc_color_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    slider = customtkinter.CTkSlider(master=modify_frame, from_=5, to=15, command=set_font_size)
    slider.grid(row=3, column=0, pady=10, padx=10, sticky="e")

    # Font type selection
    font_type_label = customtkinter.CTkLabel(master=modify_frame, text="Font Type :")
    font_type_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")

    font_type_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                  values=["Serif", "San-Serif", "Script"],
                                                  command=lambda: set_font_type)
    font_type_menu.grid(row=4, column=0, pady=10, padx=10, sticky="e")

    # regenerate graph button
    regenerate_graph_btn = customtkinter.CTkButton(master=modify_frame,
                                                   text="Apply Changes",
                                                   command=regenerate_graph
                                                   )
    regenerate_graph_btn.grid(row=10, column=1, columnspan=2, pady=10, padx=10)

    return modify_frame
