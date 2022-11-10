from tkinter import filedialog, DISABLED, NORMAL, ACTIVE
from tkinter.messagebox import IGNORE
import customtkinter
import tkinter
from charts.arc_diagram import ArcDiagram
from charts.sankey_chart import SankeyChart
from helpers.InputManager import InputManager
from helpers.DataPreprocesser import DataPreprocessor
from tkinter import messagebox
from helpers.modify_frame_factory import ModifyFrameFactory
from charts.chord_chart import ChordChart
import pandas as pd

"""
input_frame -> validate_file_frame -> preprocess_frame -> generate_chart_frame
"""


def get_upload_box(root, master, type, right_frame_width):
    # full frame(parent of all child frames)
    upload_frame = customtkinter.CTkFrame(master=root)

    # get file from user
    def upload(frame):

        # give location of selected file
        global file
        file = filedialog.askopenfilename(initialdir='.\\', title='Insert File',
                                          filetypes=[("CSV files", ".csv"), ("Excel files", ".xlsx"),
                                                     ("Excel other file type", ".xls")], parent=root)

        if file:
            data_frame = InputManager.read_input(file, root)
            if isinstance(data_frame, str):
                pass
            else:
                frame.destroy()
                create_validate_file_frame(data_frame)
        else:
            pass
    
    def download_predefined():
            location=filedialog.asksaveasfile(initialdir='.\\', title='Insert File',
                                          filetypes=[("CSV", ".csv")], parent=root)

            df = pd.read_csv("./csv_samples/predefined_sample.csv")
 
            dataFrame = pd.DataFrame({'Source': df['Source'], 'Target':df['Target'], 'Weight': df['Weight']
                              }, index=range(20))
            dataFrame.to_csv(f"{location.name}.csv")

    def create_input_frame():
        file_input_frame = customtkinter.CTkFrame(master=upload_frame)

        file_input_frame.rowconfigure((1, 2, 3,4,6), weight=1)
        file_input_frame.columnconfigure((0, 1,2), weight=1)

        file_input_frame.pack(padx=100, pady=100, fill=tkinter.BOTH)
        upload_guide_txt = customtkinter.CTkLabel(master=file_input_frame,
                                                  text="Please upload your CSV file in predefined format",
                                                  text_font=("Roboto Medium", -16),

                                                  )
        upload_guide_txt.grid(row=0, column=1, pady=10,padx=10)
        # upload_icon = ImageTk.PhotoImage(Image.open("C:/Users/ACER/PyAdvanCharts/components/upload_1.png").resize((20,20), Image.ANTIALIAS))
        download_predefined_btn=customtkinter.CTkButton(master=file_input_frame,
                                             text="Download predefined file",
                                             command=download_predefined
                                             )
        download_predefined_btn.grid(row=3, column=1, pady=10,padx=10)
        upload_btn = customtkinter.CTkButton(master=file_input_frame,
                                             text="Upload",
                                             command=lambda: upload(file_input_frame)
                                             )

        upload_btn.grid(row=5, column=1, pady=10,padx=10)

    create_input_frame()

    # function for navigate to initial user file upload frame
    def goto_upload(frame):
        value = messagebox.askyesno("Confirm", "Are you sure?", parent=root)
        if value:
            frame.destroy()
            create_input_frame()
        else:
            pass

    # navigate to next frame from validate_file_frame
    def next_valid(frame, data_frame):
        value = messagebox.askyesno("Confirm", "Do you wish to proceed?", parent=root)
        if value:
            frame.destroy()
            generate_chart(data_frame)
        else:
            frame.destroy()
            create_input_frame()

    def create_validate_file_frame(data_frame):
        # TODO Validate input file in predefined format

        data_info, data_frame = DataPreprocessor.data_cleaner(data_frame)

        validate_file_frame = customtkinter.CTkFrame(master=upload_frame)
        validate_file_frame.pack(padx=100, pady=100, fill=tkinter.BOTH)

        validate_file_frame.rowconfigure((1, 2, 3,4,6), weight=1)
        validate_file_frame.columnconfigure((0, 1,2), weight=1)
        validate_txt = customtkinter.CTkLabel(master=validate_file_frame,
                                              text=data_info,
                                              text_font=("Roboto Medium", -16),

                                              )
        validate_txt.grid(row=0, column=1, pady=10,padx=10)

        next_valid_btn = customtkinter.CTkButton(master=validate_file_frame,
                                                 text="Proceed",
                                                 command=lambda: next_valid(validate_file_frame, data_frame)
                                                 )
        next_valid_btn.grid(row=3, column=1, pady=10,padx=10)
        cancel_btn = customtkinter.CTkButton(master=validate_file_frame,
                                             text="Cancel",
                                             command=lambda: goto_upload(validate_file_frame)
                                             )
        cancel_btn.grid(row=5, column=1, pady=10,padx=10)

    def generate_chart(data_frame):
        chart_diagram = None
        if type == 0:
            chart_diagram=SankeyChart(file)
        elif type == 1:
            chart_diagram = ChordChart(data_frame=data_frame)
        elif type == 2:
            chart_diagram = ArcDiagram(data_frame=data_frame)
        master.frame_right = ModifyFrameFactory.get_modify_frame(type, master, chart_diagram, right_frame_width)

    return upload_frame


"""
 def create_preprocess_frame():
        # TODO Preprocess the file
        preprocess_frame = customtkinter.CTkFrame(master=upload_frame, bg_color="#3D3B3B", fg_color="#524E4E",
                                                  border_color="#D9D9D9")
        preprocess_frame.pack(padx=100, pady=100, fill=tkinter.BOTH)
        preprocess_guide_txt = customtkinter.CTkLabel(master=preprocess_frame,
                                                      text="Your file has 4 rows with null values do you want to delete it?",
                                                      text_font=("Roboto Medium", -16),

                                                      )
        preprocess_guide_txt.pack(pady=20, padx=100)

        delete_btn = customtkinter.CTkButton(master=preprocess_frame,
                                             text="Delete",
                                             command=lambda: delete(preprocess_frame)
                                             )
        delete_btn.pack(pady=20, padx=10)

        goto_upload_btn = customtkinter.CTkButton(master=preprocess_frame,
                                                  text="Previous",
                                                  command=lambda: goto_upload(preprocess_frame)
                                                  )
        goto_upload_btn.pack(pady=20, padx=10)
        
        
# delete null value containing rows and navigate to generate_chart_frame
    def delete():
        # logic to delete rows
        # TODO Logic to delete rows

        #frame.destroy()

        # logic to create next frame
        generate_chart_frame = customtkinter.CTkFrame(master=upload_frame, bg_color="#3D3B3B", fg_color="#524E4E",
                                                      border_color="#D9D9D9")
        generate_chart_frame.pack(padx=100, pady=100, fill=tkinter.BOTH)
        generate_chart_guide_txt = customtkinter.CTkLabel(master=generate_chart_frame,
                                                          text="Choose options of your graph",
                                                          text_font=("Roboto Medium", -16),

                                                          )
        generate_chart_guide_txt.pack(pady=20, padx=100)


        generate_btn = customtkinter.CTkButton(master=generate_chart_frame,
                                               text="Generate chart",
                                               command=lambda: generate_chart(generate_chart_frame)
                                               )
        generate_btn.pack(pady=20, padx=10)

        goto_upload_btn = customtkinter.CTkButton(master=generate_chart_frame,
                                                  text="Cancel",
                                                  command=lambda: goto_upload(generate_chart_frame)
                                                  )
        goto_upload_btn.pack(pady=20, padx=10)
        

"""
