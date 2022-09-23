
import customtkinter
import tkinter
import PySimpleGUI as sg


from helpers.graphs import draw_sankey
from helpers.modify_frame_factory import ModifyFrameFactory


"""
input_frame -> validate_file_frame -> preprocess_frame -> generate_chart_frame
"""
def get_upload_box(root,master):

    #full frame(parent of all child frames)
    upload_frame=customtkinter.CTkFrame(master=root)

    #get file from user
    def upload(frame):
        #give location of selected file
        location=sg.popup_get_file("Choose file location",
                    title = "Upload your file",
                    default_path = "",
                    default_extension = ".csv",
                    save_as = False,
                    multiple_files = False,
                    file_types = (('ALL Files', '*.* *'),),
                    no_window = False,
                    size = (None, None),
                    button_color = None,
                    background_color = None,
                    text_color = None,
                    icon = None,
                    font = None,
                    no_titlebar = False,
                    grab_anywhere = False,
                    keep_on_top = None,
                    location = (None, None),
                    relative_location = (None, None),
                    initial_folder = None,
                    image = None,
                    files_delimiter = ";",
                    modal = True,
                    history = False,
                    show_hidden = True,
                    history_setting_filename = None)
        frame.destroy()
        create_validate_file_frame()
    
    
    def create_input_frame():
        file_input_frame=customtkinter.CTkFrame(master=upload_frame,bg_color="#3D3B3B",fg_color="#524E4E",border_color="#D9D9D9")
        file_input_frame.pack(padx=100,pady=100,fill=tkinter.BOTH)
        upload_guide_txt = customtkinter.CTkLabel(master=file_input_frame,
                                                    text="Please upload your CSV file in predefined format",
                                                    text_font=("Roboto Medium", -16),
                                                
                                                    )  
        upload_guide_txt.pack(pady=100,padx=100)
        upload_btn = customtkinter.CTkButton(master=file_input_frame,
                                                    text="Upload",
                                                    command=lambda: upload(file_input_frame)
                                        )
    
        upload_btn.pack(pady=40,padx=10)
    
    create_input_frame()
    
    #function for navigate to initial user file upload frame
    def goto_upload(frame):
        frame.destroy()
        create_input_frame()
        

    #navigate to next frame from validate_file_frame
    def next_valid(frame):
        frame.destroy()
        create_preprocess_frame()
       

    def create_validate_file_frame():
        #TODO Validate input file in predefined format
        validate_file_frame=customtkinter.CTkFrame(master=upload_frame,bg_color="#3D3B3B",fg_color="#524E4E",border_color="#D9D9D9")
        validate_file_frame.pack(padx=100,pady=100,fill=tkinter.BOTH)
        validate_txt = customtkinter.CTkLabel(master=validate_file_frame,
                                                    text="Your file has predefined format you are good to go :)",
                                                    text_font=("Roboto Medium", -16),
                                                
                                                    )  
        validate_txt.pack(pady=20,padx=100)

        next_valid_btn = customtkinter.CTkButton(master=validate_file_frame,
                                                text="Next",
                                                command=lambda : next_valid(validate_file_frame)
                                    )
        next_valid_btn.pack(pady=20,padx=10)

        goto_upload_btn = customtkinter.CTkButton(master=validate_file_frame,
                                                text="Previous",
                                                command=lambda: goto_upload(validate_file_frame)
                                    )
        goto_upload_btn.pack(pady=20,padx=10)

    def create_preprocess_frame():
        #TODO Preprocess the file
        preprocess_frame=customtkinter.CTkFrame(master=upload_frame,bg_color="#3D3B3B",fg_color="#524E4E",border_color="#D9D9D9")
        preprocess_frame.pack(padx=100,pady=100,fill=tkinter.BOTH)
        preprocess_guide_txt = customtkinter.CTkLabel(master=preprocess_frame,
                                                    text="Your file has 4 rows with null values do you want to delete it?",
                                                    text_font=("Roboto Medium", -16),
                                                
                                                    )  
        preprocess_guide_txt.pack(pady=20,padx=100)

        delete_btn = customtkinter.CTkButton(master=preprocess_frame,
                                                text="Delete",
                                                command=lambda : delete(preprocess_frame)
                                    )
        delete_btn.pack(pady=20,padx=10)

        goto_upload_btn = customtkinter.CTkButton(master=preprocess_frame,
                                                text="Previous",
                                                command=lambda: goto_upload(preprocess_frame)
                                    )
        goto_upload_btn.pack(pady=20,padx=10)

    #delete null value containing rows and navigate to generate_chart_frame
    def delete(frame):
        #logic to delete rows
        #TODO Logic to delete rows

        frame.destroy()

        #logic to create next frame
        generate_chart_frame=customtkinter.CTkFrame(master=upload_frame,bg_color="#3D3B3B",fg_color="#524E4E",border_color="#D9D9D9")
        generate_chart_frame.pack(padx=100,pady=100,fill=tkinter.BOTH)
        generate_chart_guide_txt = customtkinter.CTkLabel(master=generate_chart_frame,
                                                    text="Choose options of your graph",
                                                    text_font=("Roboto Medium", -16),
                                                
                                                    )  
        generate_chart_guide_txt.pack(pady=20,padx=100)

        

        generate_btn = customtkinter.CTkButton(master=generate_chart_frame,
                                                text="Generate chart",
                                                command=lambda : generate_chart(generate_chart_frame)
                                    )
        generate_btn.pack(pady=20,padx=10)

        goto_upload_btn = customtkinter.CTkButton(master=generate_chart_frame,
                                                text="Previous",
                                                command=lambda: goto_upload(generate_chart_frame)
                                    )
        goto_upload_btn.pack(pady=20,padx=10)
   
    def generate_chart(frame):
        """
        frame.destroy()
        chart_frame=customtkinter.CTkFrame(master=upload_frame,bg_color="#3D3B3B",fg_color="#524E4E",border_color="#D9D9D9")
        chart_frame.pack(fill=tkinter.BOTH)
        """
        #draw_sankey(chart_frame)
        master.frame_right=ModifyFrameFactory.get_modify_frame(0,master)

    return upload_frame
