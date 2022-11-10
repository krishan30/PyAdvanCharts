import tkinter
from tkinter import filedialog, Y, ttk, messagebox
import customtkinter
from modify_box_frames.chord_modify_box import get_chord_modify_box
from helpers.graphs import *
import pandas as pd


class ChordModify:

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
                                             text="Chart View",
                                             text_font=("Roboto Medium", 16),

                                             )  # font name and size in px
        chart_title.grid(row=0, column=1, columnspan=2, pady=10, padx=10)

        # function for navigate to bottom part(upload box)
        def go_bottom():
            my_canvas.yview_moveto('0.45')

        create_chart_btn = customtkinter.CTkButton(master=frame_right,
                                                   text="Modify",
                                                   command=go_bottom
                                                   )
        create_chart_btn.grid(row=0, column=2, columnspan=2, pady=10, padx=150)

        draw_chord(frame_right, chord_diagram).get_tk_widget().grid(row=1, column=0, columnspan=4, rowspan=4, pady=2,
                                                                    padx=20,
                                                                    sticky="ns")

        # function for open chart in a new window
        def open_graph():
            figure = chord_diagram.generate_graph()

            window = customtkinter.CTkToplevel(root)
            window.geometry("800x500")
            window.title("Chord Chart Full View")

            chart = FigureCanvasTkAgg(figure, window)
            chart.get_tk_widget().pack(anchor=tkinter.N, fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)

        # function for download the sample csv file
        def save_chart():
            location = filedialog.asksaveasfile(initialdir='.\\', title='Save Chart',
                                                filetypes=[("PNG", ".png")], parent=root)
            if location is not None:
                chord_diagram.save_image(f"{location.name}.png")
                messagebox.showinfo("Chart Save", "Save Completed",parent=root)
            else:
                pass

        save_chart_btn = customtkinter.CTkButton(master=frame_right,
                                                 text="Save Chart",
                                                 command=save_chart

                                                 )  # font name and size in px
        save_chart_btn.grid(row=5, column=1, rowspan=1, columnspan=2, pady=10, padx=10)

        open_graph_btn = customtkinter.CTkButton(master=frame_right,
                                                 text="Full Screen View",
                                                 command=open_graph
                                                 )
        open_graph_btn.grid(row=0, column=3, columnspan=2, pady=10, padx=10)

        """
        #upload frame in the bottom
        upload_frame=get_upload_box(frame_right)
        upload_frame.grid(row=7, column=0, rowspan=4,columnspan=4,pady=10,padx=20)
        upload_frame.grid_propagate(0)
        """

        # modify frame in the bottom
        modify_frame = get_chord_modify_box(frame_right, root, chord_diagram, right_frame_width)
        modify_frame.grid(row=7, column=0, rowspan=4, columnspan=4, pady=5, padx=20, sticky="nwse")
        modify_frame.grid_propagate(0)

        return main_frame