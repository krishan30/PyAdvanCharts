import tkinter
from tkinter import Y, ttk
import tkinter.messagebox
import customtkinter
import components.custom_table as custom_table
from helpers.graphs import *
import PySimpleGUI as sg
import pandas as pd

from components.upload_box import get_upload_box


class ChordHome:

    @staticmethod
    def get_frame(root, chord_diagram, right_frame_width):
        # set home frame grid
        main_frame = customtkinter.CTkFrame(master=root)
        main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # create canvas inside main_frame in left side
        my_canvas = tkinter.Canvas(main_frame, background="grey")
        my_canvas.pack(side=tkinter.LEFT, anchor="nw", fill=tkinter.BOTH, expand=1, )

        # create Scrollbar inside main_frame in right side
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
        scrollbar.pack(side=tkinter.RIGHT, fill=Y)

        # connect scrollbar with canvas
        my_canvas.configure(yscrollcommand=scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # create content frame and put it inside canvas
        frame_right = customtkinter.CTkFrame(master=my_canvas, width=right_frame_width, height=1500)
        frame_right.grid_propagate(0)  # give static fixed size to frame_right
        my_canvas.create_window((0, 0), window=frame_right, anchor="nw")

        frame_right.rowconfigure((1, 2, 3, 4, 6), weight=1)
        frame_right.rowconfigure((7, 8, 9, 10, 11, 12), weight=5)
        frame_right.columnconfigure((0, 1, 2, 3), weight=1)

        chart_title = customtkinter.CTkLabel(master=frame_right,
                                             text="Chord Diagram",
                                             text_font=("Roboto Medium", 16),

                                             )  # font name and size in px
        chart_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # function for navigate to bottom part(upload box)
        def go_bottom():
            my_canvas.yview_moveto('1.0')

        create_chart_btn = customtkinter.CTkButton(master=frame_right,
                                                   text="Create Chord",
                                                   command=go_bottom
                                                   )
        create_chart_btn.grid(row=0, column=2, columnspan=2, pady=10, padx=10)

        data_table = custom_table.get_table(frame_right)
        data_table.grid(row=1, column=0, columnspan=2, rowspan=4, pady=2, padx=20, sticky="nswe")

        # ==================Play with different graphs========================

        # draw_simple_matplotlib_chart(frame_right)
        draw_chord(frame_right, chord_diagram).get_tk_widget().grid(row=1, column=2, columnspan=2, rowspan=4, pady=2,
                                                                    padx=20,
                                                                    sticky="ns")

        # draw_simple_seaborn_chart(frame_right)
        # draw_iris_data(frame_right)

        # function for open chart in a new window
        def open_graph():
            figure = chord_diagram.generate_graph()

            window = customtkinter.CTkToplevel(root)
            window.geometry("800x500")
            window.title("Sample Chord chart")

            chart = FigureCanvasTkAgg(figure, window)
            chart.get_tk_widget().pack(anchor=tkinter.N, fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)

        # function for download the sample csv file
        def download_sample():
            location = sg.popup_get_file("Choose file location",
                                         title="Save sample file as",
                                         default_path="",
                                         default_extension=".csv",
                                         save_as=True,
                                         multiple_files=False,
                                         file_types=(('ALL Files', '*.* *'),),
                                         no_window=False,
                                         size=(None, None),
                                         button_color=None,
                                         background_color=None,
                                         text_color=None,
                                         icon=None,
                                         font=None,
                                         no_titlebar=False,
                                         grab_anywhere=False,
                                         keep_on_top=None,
                                         location=(None, None),
                                         relative_location=(None, None),
                                         initial_folder=None,
                                         image=None,
                                         files_delimiter=";",
                                         modal=True,
                                         history=False,
                                         show_hidden=True,
                                         history_setting_filename=None)

            df = pd.read_csv("./csv_samples/sankey_sample.csv")

            dataFrame = pd.DataFrame({'from': df['from'], 'to': df['to'], 'weight': df['weight']
                                      }, index=range(len(df['from'])))
            dataFrame.to_csv(location)

        download_btn = customtkinter.CTkButton(master=frame_right,
                                               text="Download",
                                               command=download_sample

                                               )  # font name and size in px
        download_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

        open_graph_btn = customtkinter.CTkButton(master=frame_right,
                                                 text="Open",
                                                 command=open_graph
                                                 )
        open_graph_btn.grid(row=5, column=2, columnspan=2, pady=10, padx=10)

        text_frame = tkinter.Text(frame_right, padx=20, pady=10, width=10, height=8, background="#A7C2E0",
                                  wrap=tkinter.CHAR)
        text_frame.insert(tkinter.END,
                          "A chord diagram represents flows or connections between several entities (called nodes). Each entity is represented by a fragment on the outer part of the circular layout.Then, arcs are drawn between each entities. The size of the arc is proportional to the importance of the flow.")
        text_frame.grid(row=6, column=0, columnspan=4, pady=20, padx=20, sticky="ew")

        # upload frame in the bottom
        upload_frame = get_upload_box(frame_right, root, 1, right_frame_width)
        upload_frame.grid(row=7, column=0, rowspan=4, columnspan=4, pady=100, padx=100, sticky="nswe")
        upload_frame.grid_propagate(0)

        """
        #modify frame in the bottom
        modify_frame=customtkinter.CTkFrame(master=frame_right)
        modify_frame.grid(row=12, column=0, rowspan=4,columnspan=4,pady=100,padx=200)
        modify_frame.grid_propagate(0)
        """
        return main_frame
