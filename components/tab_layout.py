import customtkinter

from helpers.home_frame_factory import HomeFrameFactory

def  get_tab_frame(root):
    
    frame_left = customtkinter.CTkFrame(master=root,
                                                 width=180,
                                                 corner_radius=0)
    frame_left.grid(row=0, column=0, sticky="nswe")


    def change_appearance_mode( new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)



    def select_chart_1():
        root.frame_right=HomeFrameFactory.get_home_frame(0,root)
          
    def select_chart_2():
        root.frame_right=HomeFrameFactory.get_home_frame(1,root)
     
    def select_chart_3():
        root.frame_right=HomeFrameFactory.get_home_frame(2,root)
       
    
    # configure grid layout (1x11)
    frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
    frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
    frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
    frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

    heading_label = customtkinter.CTkLabel(master=frame_left,
                                            text="Select Chart",
                                            text_font=("Roboto Medium", -16))  # font name and size in px
    heading_label.grid(row=1, column=0, pady=10, padx=10)

    sankey_button = customtkinter.CTkButton(master=frame_left,
                                            text="Sankey Chart",
                                            command=select_chart_1)
    sankey_button.grid(row=2, column=0, pady=10, padx=20)

    chord_button = customtkinter.CTkButton(master=frame_left,
                                            text="Chord Diagram",
                                            command=select_chart_2)
    chord_button.grid(row=3, column=0, pady=10, padx=20)

    directed_button = customtkinter.CTkButton(master=frame_left,
                                            text="Force directed graph",
                                            command=select_chart_3)
    directed_button.grid(row=4, column=0, pady=10, padx=20)

    label_mode = customtkinter.CTkLabel(master=frame_left, text="Theme")
    label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

    theme_optionmenu = customtkinter.CTkOptionMenu(master=frame_left,
                                                    values=["Light", "Dark", "System"],
                                                    command=change_appearance_mode)
    theme_optionmenu.grid(row=10, column=0, pady=10, padx=20, sticky="w")


    # set default values
    theme_optionmenu.set("Dark")
        
    return frame_left