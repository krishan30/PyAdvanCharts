import customtkinter
import tkinter
from tkinter import colorchooser

def get_sankey_modify_box(root,root_parent, sankey_diagram):
    modify_frame=customtkinter.CTkFrame(master=root)

    modify_frame.rowconfigure((1, 2, 3,4,6), weight=1)
    modify_frame.rowconfigure((7,8,9,10,11,12), weight=5)
    modify_frame.columnconfigure((0, 1,2), weight=1)

    # Attributes of the graph
    font_size = sankey_diagram.get_label_font_size()
    weight_font_size = sankey_diagram.get_weight_font_size()
    background_colour=sankey_diagram.get_bg_color()
    graph_font=sankey_diagram.get_font_family()
    block_color_palette,strip_color_palette=sankey_diagram.get_pallete()
    show_label_txt=sankey_diagram.get_show_label_txt()
    show_weight_txt=sankey_diagram.get_show_weight_txt()
    font_color=sankey_diagram.get_font_color()
    block_out_color=sankey_diagram.get_block_out_color()
    strip_out_color=sankey_diagram.get_strip_out_color()
    title=sankey_diagram.get_title()

    show_block_out=False
    show_strip_out=False
    if block_out_color!=None:
        show_block_out=True
    if strip_out_color!=None:
        show_strip_out=True

    block_alpha=sankey_diagram.get_block_alpha()
    strip_alpha=sankey_diagram.get_strip_alpha()
    block_v_m=sankey_diagram.get_block_v_m()
    block_h_m=sankey_diagram.get_block_h_m()

    # Set label font size
    def set_label_font_size(value):
        nonlocal font_size
        #print(value)
        if value is not None:
            font_size = int(value)

    # Set weight font size
    def set_weight_font_size(value):
        nonlocal weight_font_size
        #print(value)
        if value is not None:
            weight_font_size = int(value)

    # set background colour
    def set_background_color():
        nonlocal background_colour
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        background_colour = hex_code

    # Set font type
    def set_font_type(choice):
        nonlocal graph_font
        graph_font = choice
       
    #set color palate of block
    def set_block_color_palete(choice):
        nonlocal block_color_palette
        block_color_palette = choice

    #set color palate of strip
    def set_strip_color_palete(choice):
        nonlocal strip_color_palette
        strip_color_palette = choice

       
    def set_show_label_txt(choice):
        nonlocal show_label_txt
        if choice=="Show":
            show_label_txt=True
        else:
            show_label_txt=False
       
    
    def set_show_weight_txt(choice):
        nonlocal show_weight_txt
        if choice=="Show":
            show_weight_txt=True
        else:
            show_weight_txt=False
     

    # set font colour
    def set_font_color():
        nonlocal font_color
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        font_color = hex_code

    #set outline color for block
    def set_block_out_color():
        nonlocal show_block_out
        nonlocal block_out_color
        show_block_out=True
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        block_out_color = hex_code

    #set outline color for strip
    def set_strip_out_color():
        nonlocal show_strip_out
        nonlocal strip_out_color
        show_strip_out=True
        color_code = colorchooser.askcolor(title="Choose color")
        rgb_values, hex_code = color_code
        strip_out_color = hex_code

    #set alpha value for block
    def set_block_alpha(value):
        nonlocal block_alpha
        #print(value)
        if value is not None:
            block_alpha = value

    #set alpha value for strip
    def set_strip_alpha(value):
        nonlocal strip_alpha
        #print(value)
        if value is not None:
            strip_alpha = value

    #set vertical margin for block
    def set_block_v_m(value):
        nonlocal block_v_m
        #print(value)
        if value is not None:
            block_v_m = value/10

    #set horizontal margin for block
    def set_block_h_m(value):
        nonlocal block_h_m
        #print(value)
        if value is not None:
            block_h_m = value
            
    # Regenerate graph according to the new changes
    def regenerate_graph():
        from modify_body_frames.sankey_modify_frame import SankeyModify
        sankey_diagram.set_label_font_size(font_size)
        sankey_diagram.set_weight_font_size(weight_font_size)
        sankey_diagram.set_bg_color(background_colour)
        sankey_diagram.set_font_family(graph_font)
        sankey_diagram.set_pallete(block_color_palette,strip_color_palette)
        sankey_diagram.set_font_color(font_color)
        sankey_diagram.set_show_weight_txt(show_weight_txt)
        sankey_diagram.set_show_label_txt(show_label_txt)
        sankey_diagram.set_block_out_color(block_out_color)
        sankey_diagram.set_strip_out_color(strip_out_color)
        sankey_diagram.set_block_alpha(block_alpha)
        sankey_diagram.set_strip_alpha(strip_alpha)
        sankey_diagram.set_block_v_m(block_v_m)
        sankey_diagram.set_block_h_m(block_h_m)
        nonlocal title
        if new_title_text.get()!="":
            title=new_title_text.get()
        
        sankey_diagram.set_title(title)

        if show_block_out==False:
            sankey_diagram.remove_block_out()
        if show_strip_out==False:
            sankey_diagram.remove_strip_out()
        
        SankeyModify.get_frame(root_parent, sankey_diagram)
        


    
    #bg color selection
    bg_color_label = customtkinter.CTkLabel(master=modify_frame, text="BG Color :")
    bg_color_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    bg_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_background_color,
                                            hover_color=background_colour
                                )
    bg_color_btn.grid(row=0, column=0, pady=10,padx=10,sticky="e")

    
    #block color selection
    block_color_label = customtkinter.CTkLabel(master=modify_frame, text="Block Color :")
    block_color_label.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    block_color_btn = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["hls","Paired","Set2","tab10","husl","rocket","mako","flare","crest","magma","viridis","magma"],
                                                    command=set_block_color_palete

                                )
    block_color_btn.set(block_color_palette)
    block_color_btn.grid(row=0, column=1, pady=10,padx=10,sticky="e")

    #strip color selection
    strip_color_label = customtkinter.CTkLabel(master=modify_frame, text="Strip Color :")
    strip_color_label.grid(row=0, column=2, pady=10, padx=10, sticky="w")

    strip_color_btn = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["hls","Paired","Set2","tab10","husl","rocket","mako","flare","crest","magma","viridis","magma"],
                                                    command=set_strip_color_palete)
    strip_color_btn.set(strip_color_palette)                            
    strip_color_btn.grid(row=0, column=2, pady=10,padx=10,sticky="e")

    #font style selection
    font_style_label = customtkinter.CTkLabel(master=modify_frame, text="Font Style :")
    font_style_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")


    font_style_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["sans-serif", "serif", "cursive", "fantasy", "monospace"],
                                                    command=set_font_type)
    font_style_menu.set(graph_font)                                                
    font_style_menu.grid(row=1, column=0, pady=10, padx=10, sticky="e")

    
    #label font size selection
    font_size_label = customtkinter.CTkLabel(master=modify_frame, text="Label Font size :   "+ str(font_size))
    font_size_label.grid(row=1, column=1, pady=10, padx=10, sticky="w")

    label_font_size_slider = customtkinter.CTkSlider(master=modify_frame, from_=5, to=16, command=set_label_font_size,
                                     number_of_steps=12)
    label_font_size_slider.set(font_size)                                 
    label_font_size_slider.grid(row=1, column=1, pady=10, padx=10, sticky="e")

    #weight font size selection
    font_size_weight = customtkinter.CTkLabel(master=modify_frame, text="Weight Font size :   "+str(weight_font_size))
    font_size_weight.grid(row=1, column=2, pady=10, padx=10, sticky="w")

    weight_font_size_slider = customtkinter.CTkSlider(master=modify_frame, from_=5, to=10, command=set_weight_font_size,
                                     number_of_steps=7)
    weight_font_size_slider.set(weight_font_size)                                 
    weight_font_size_slider.grid(row=1, column=2, pady=10, padx=10, sticky="e")

   

    #font color selection
    font_color_label = customtkinter.CTkLabel(master=modify_frame, text="Font Color :")
    font_color_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

    font_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_font_color,
                                            hover_color=font_color
                                )
    font_color_btn.grid(row=2, column=0, pady=10,padx=10,sticky="e")

    

     #label option selection
    label_option_label = customtkinter.CTkLabel(master=modify_frame, text="Label :")
    label_option_label.grid(row=2, column=1, pady=10, padx=10, sticky="w")


    label_option_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["Show", "Hide"],
                                                    command=set_show_label_txt)
    if show_label_txt:
        label_option_menu.set("Show")
    else:
        label_option_menu.set("Hide")
    label_option_menu.grid(row=2, column=1, pady=10, padx=10, sticky="e")

    #weight option selection
    weight_option_label = customtkinter.CTkLabel(master=modify_frame, text="Weight :")
    weight_option_label.grid(row=2, column=2, pady=10, padx=10, sticky="w")


    weight_option_menu = customtkinter.CTkOptionMenu(master=modify_frame,
                                                    values=["Show", "Hide"],
                                                    command=set_show_weight_txt)
    if show_weight_txt:
        weight_option_menu.set("Show")
    else:
        weight_option_menu.set("Hide")
    weight_option_menu.grid(row=2, column=2, pady=10, padx=10, sticky="e")

    #Node vertical margin selection
    node_vertical_margin_label = customtkinter.CTkLabel(master=modify_frame, text="Node vertical margin :   "+str( float(round(block_v_m,3)) ))
    node_vertical_margin_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")


    node_vertical_margin_menu = customtkinter.CTkSlider(master=modify_frame, from_=0, to=1, command=set_block_v_m,
                                     number_of_steps=10)
    node_vertical_margin_menu.set(block_v_m*10)                                 
    node_vertical_margin_menu.grid(row=3, column=0, pady=10, padx=10, sticky="e")

    #Node horizontal margin selection
    node_horizontal_margin_label = customtkinter.CTkLabel(master=modify_frame, text="Node horizontal margin :   "+str(block_h_m)  )
    node_horizontal_margin_label.grid(row=3, column=1, pady=10, padx=10, sticky="w")


    node_horizontal_margin_menu = customtkinter.CTkSlider(master=modify_frame, from_=0, to=1, command=set_block_h_m,
                                     number_of_steps=20)
    node_horizontal_margin_menu.set(block_h_m)
    node_horizontal_margin_menu.grid(row=3, column=1, pady=10, padx=10, sticky="e")


    #label alpha selection
    alpha_label = customtkinter.CTkLabel(master=modify_frame, text="Label Alpha :   "+str( float(round(block_alpha,3)) ))
    alpha_label.grid(row=3, column=2, pady=10, padx=10, sticky="w")

    alpha_label_slider = customtkinter.CTkSlider(master=modify_frame, from_=0, to=1, command=set_block_alpha,
                                     number_of_steps=20)
    alpha_label_slider.set(block_alpha)
    alpha_label_slider.grid(row=3, column=2, pady=10, padx=10, sticky="e")

    #strip alpha selection
    alpha_strip = customtkinter.CTkLabel(master=modify_frame, text="Strip Alpha :   "+str( float(round(strip_alpha,3)) ))
    alpha_strip.grid(row=4, column=0, pady=10, padx=10, sticky="w")

    alpha_strip_slider = customtkinter.CTkSlider(master=modify_frame, from_=0, to=1, command=set_strip_alpha,
                                     number_of_steps=10)
    alpha_strip_slider.set(strip_alpha)
    alpha_strip_slider.grid(row=4, column=0, pady=10, padx=10, sticky="e")

    #title entry
    new_title_label = customtkinter.CTkLabel(master=modify_frame, text="New Title:")
    new_title_label.grid(row=4, column=1, pady=10, padx=10)

    new_title_text = customtkinter.CTkEntry(master=modify_frame, placeholder_text=title)
    new_title_text.grid(row=4, column=1, pady=10, padx=10, sticky="e")
   
    #Block outline
    block_outline_label = customtkinter.CTkLabel(master=modify_frame, text="Block outline :")
    block_outline_label.grid(row=5, column=0, pady=10, padx=10, sticky="e")


    
    radio_var=tkinter.IntVar(0)
    def add_block_out():
        nonlocal show_block_out
        show_block_out=True

    def remove_block_out():
        nonlocal show_block_out
        show_block_out=False

    block_out_yes_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="Yes",
                                                command=add_block_out, variable= radio_var, value=1)

    block_out_no_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="No",
                                                command=remove_block_out, variable= radio_var, value=2)

    block_out_yes_radio_btn.grid(row=5, column=1, pady=10, padx=10, sticky="w")
    block_out_no_radio_btn.grid(row=5, column=1, pady=10, padx=80, sticky="w")

    if show_block_out:
        block_out_yes_radio_btn.select()
    else:
        block_out_no_radio_btn.select()

    #block outline color selection
    block_out_color_label = customtkinter.CTkLabel(master=modify_frame, text="Block Outline Color :")
    block_out_color_label.grid(row=5, column=2, pady=10, padx=10, sticky="w")

    block_out_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_block_out_color,
                                            hover_color=block_out_color
                                )
    block_out_color_btn.grid(row=5, column=2, pady=10,padx=10)

    #Strip outline
    strip_outline_label = customtkinter.CTkLabel(master=modify_frame, text="Strip outline :")
    strip_outline_label.grid(row=6, column=0, pady=10, padx=10, sticky="e")


    
    radio_var_2=tkinter.IntVar(0)
    def add_strip_out():
        nonlocal show_strip_out
        show_strip_out=True
    def remove_strip_out():
        nonlocal show_strip_out
        show_strip_out=False
    

    strip_out_yes_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="Yes",
                                                command=add_strip_out, variable= radio_var_2, value=1)

    strip_out_no_radio_btn = customtkinter.CTkRadioButton(master=modify_frame, text="No",
                                                command=remove_strip_out, variable= radio_var_2, value=2)

    if show_strip_out:
        strip_out_yes_radio_btn.select()
    else:
        strip_out_no_radio_btn.select()
    strip_out_yes_radio_btn.grid(row=6, column=1, pady=10, padx=10, sticky="w")
    strip_out_no_radio_btn.grid(row=6, column=1, pady=10, padx=80, sticky="w")

    #strip outline color selection
    strip_out_color_label = customtkinter.CTkLabel(master=modify_frame, text="Strip Outline Color :")
    strip_out_color_label.grid(row=6, column=2, pady=10, padx=10, sticky="w")

    strip_out_color_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Choose",
                                            command=set_strip_out_color,
                                            hover_color=strip_out_color
                                )
    strip_out_color_btn.grid(row=6, column=2, pady=10,padx=10)

    #regenerate graph button
    regenerate_graph_btn = customtkinter.CTkButton(master=modify_frame,
                                            text="Apply Changes",
                                            command=regenerate_graph 
                                )
    regenerate_graph_btn.grid(row=7, column=1,columnspan=1, pady=10,padx=10)


    return modify_frame
