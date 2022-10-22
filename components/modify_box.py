import customtkinter
import tkinter
from tkinter import colorchooser


def get_chart_home(frame):
    pass
    #frame.destroy()
    #ChordHome.get_frame(frame.master)



def get_modify_box(root):
    modify_frame=customtkinter.CTkFrame(master=root)

    modify_frame.rowconfigure((1, 2, 3,4,6), weight=1)
    modify_frame.rowconfigure((7,8,9,10,11,12), weight=5)
    modify_frame.columnconfigure((0, 1,2,3), weight=1)

    #function for color selection
    def get_color():
        # variable to store hexadecimal code of color
        color_code = colorchooser.askcolor(title ="Choose color")
        #print(color_code)
        
    
    #bg color selection
    bg_color_label = customtkinter.CTkLabel(master=modify_frame, text="BG Color :")
    bg_color_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    bg_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=get_color
                                )
    bg_color_btn.grid(row=0, column=0, pady=10,padx=10,sticky="e")

    #fg color selection
    fg_color_label = customtkinter.CTkLabel(master=modify_frame, text="FG Color :")
    fg_color_label.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    fg_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=get_color
                                )
    fg_color_btn.grid(row=0, column=1, pady=10,padx=10,sticky="e")

    #block color selection
    block_color_label = customtkinter.CTkLabel(master=modify_frame, text="Block Color :")
    block_color_label.grid(row=0, column=2, pady=10, padx=10, sticky="w")

    block_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=get_color
                                )
    block_color_btn.grid(row=0, column=2, pady=10,padx=10,sticky="e")

    #strip color selection
    strip_color_label = customtkinter.CTkLabel(master=modify_frame, text="Strip Color :")
    strip_color_label.grid(row=0, column=3, pady=10, padx=10, sticky="w")

    strip_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=get_color
                                )
    strip_color_btn.grid(row=0, column=3, pady=10,padx=10,sticky="e")

    #font style selection
    font_style_label = customtkinter.CTkLabel(master=modify_frame, text="Font Style :")
    font_style_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")


    font_style_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["Serif", "San-Serif", "Script"],
                                                    command=lambda : ())
    font_style_menu.grid(row=1, column=0, pady=10, padx=10, sticky="e")

    #font type selection
    font_type_label = customtkinter.CTkLabel(master=modify_frame, text="Font Type :")
    font_type_label.grid(row=1, column=1, pady=10, padx=10, sticky="w")


    font_type_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["Arial", "Times", "Poppins"],
                                                    command=lambda : ())
    font_type_menu.grid(row=1, column=1, pady=10, padx=10, sticky="e")

    #font size selection
    font_size_label = customtkinter.CTkLabel(master=modify_frame, text="Font size :")
    font_size_label.grid(row=1, column=2, pady=10, padx=10, sticky="w")


    font_size_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["8", "9", "10","11","12","14","18","24","30","36","48","60","72","96"],
                                                    command=lambda : ())
    font_size_menu.grid(row=1, column=2, pady=10, padx=10, sticky="e")

    #font color selection
    font_color_label = customtkinter.CTkLabel(master=modify_frame, text="Font Color :")
    font_color_label.grid(row=1, column=3, pady=10, padx=10, sticky="w")

    font_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=get_color
                                )
    font_color_btn.grid(row=1, column=3, pady=10,padx=10,sticky="e")

     #Text Alignment selection
    text_align_label = customtkinter.CTkLabel(master=modify_frame, text="Text Alignment :")
    text_align_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")


    text_align_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["Left", "Center", "Right"],
                                                    command=lambda : ())
    text_align_menu.grid(row=2, column=0, pady=10, padx=10, sticky="e")

     #label option selection
    label_option_label = customtkinter.CTkLabel(master=modify_frame, text="Label :")
    label_option_label.grid(row=2, column=1, pady=10, padx=10, sticky="w")


    label_option_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["Show", "Hide", "Hover"],
                                                    command=lambda : ())
    label_option_menu.grid(row=2, column=1, pady=10, padx=10, sticky="e")

    #weight option selection
    weight_option_label = customtkinter.CTkLabel(master=modify_frame, text="Weight :")
    weight_option_label.grid(row=2, column=2, pady=10, padx=10, sticky="w")


    weight_option_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["Show", "Hide", "Hover"],
                                                    command=lambda : ())
    weight_option_menu.grid(row=2, column=2, pady=10, padx=10, sticky="e")

    #Node margin selection
    node_margin_label = customtkinter.CTkLabel(master=modify_frame, text="Node margin :")
    node_margin_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")


    node_margin_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["8", "9", "10","11","12","14","18","24","30","36","48","60","72","96"],
                                                    command=lambda : ())
    node_margin_menu.grid(row=3, column=0, pady=10, padx=10, sticky="e")

    #sort lables
    sort_label = customtkinter.CTkLabel(master=modify_frame, text="Sort labels :")
    sort_label.grid(row=4, column=0, pady=10, padx=10, sticky="e")


    radio_var = tkinter.IntVar(0)

    def radiobutton_event():
        #print("radiobutton toggled, current value:", radio_var.get())
        pass

    sort_yes_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="Yes",
                                                command=radiobutton_event, variable= radio_var, value=1)

    sort_no_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="No",
                                                command=radiobutton_event, variable= radio_var, value=2)

    sort_yes_radio_btn.grid(row=4, column=1, pady=10, padx=10, sticky="w")
    sort_no_radio_btn.grid(row=4, column=1, pady=10, padx=80, sticky="w")

    #Block outline
    block_outline_label = customtkinter.CTkLabel(master=modify_frame, text="Block outline :")
    block_outline_label.grid(row=5, column=0, pady=10, padx=10, sticky="e")


    radio_var = tkinter.IntVar(0)

    def radiobutton_event():
        #print("radiobutton toggled, current value:", radio_var.get())
        pass

    block_out_yes_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="Yes",
                                                command=radiobutton_event, variable= radio_var, value=1)

    block_out_no_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="No",
                                                command=radiobutton_event, variable= radio_var, value=2)

    block_out_yes_radio_btn.grid(row=5, column=1, pady=10, padx=10, sticky="w")
    block_out_no_radio_btn.grid(row=5, column=1, pady=10, padx=80, sticky="w")

    #block outline color selection
    block_out_color_label = customtkinter.CTkLabel(master=modify_frame, text="Block Outline Color :")
    block_out_color_label.grid(row=5, column=2, pady=10, padx=10, sticky="w")

    block_out_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=get_color
                                )
    block_out_color_btn.grid(row=5, column=2, pady=10,padx=10,sticky="e")

    #Strip outline
    strip_outline_label = customtkinter.CTkLabel(master=modify_frame, text="Strip outline :")
    strip_outline_label.grid(row=6, column=0, pady=10, padx=10, sticky="e")


    radio_var = tkinter.IntVar(0)

    def radiobutton_event():
        #print("radiobutton toggled, current value:", radio_var.get())
        pass

    strip_out_yes_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="Yes",
                                                command=radiobutton_event, variable= radio_var, value=1)

    strip_out_no_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="No",
                                                command=radiobutton_event, variable= radio_var, value=2)

    strip_out_yes_radio_btn.grid(row=6, column=1, pady=10, padx=10, sticky="w")
    strip_out_no_radio_btn.grid(row=6, column=1, pady=10, padx=80, sticky="w")

    #strip outline color selection
    strip_out_color_label = customtkinter.CTkLabel(master=modify_frame, text="Strip Outline Color :")
    strip_out_color_label.grid(row=6, column=2, pady=10, padx=10, sticky="w")

    strip_out_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=get_color
                                )
    strip_out_color_btn.grid(row=6, column=2, pady=10,padx=10,sticky="e")

    #regenerate graph button
    regenerate_graph_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Apply Changes",
                                            command=lambda : get_chart_home(modify_frame)
                                )
    regenerate_graph_btn.grid(row=10, column=1,columnspan=2, pady=10,padx=10)


    return modify_frame
