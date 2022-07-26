import tkinter
from tkinter import filedialog, Y, ttk, messagebox
import customtkinter
from modify_box_frames.arc_modify_box import get_arc_modify_box
from helpers.graphs import *


class ArcModify:

    @staticmethod
    def get_frame(root, arc_diagram, right_frame_width):

        arc_diagram = arc_diagram

        # set home frame grid
        main_frame = customtkinter.CTkFrame(master=root)
        main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        #create canvas inside main_frame in left side
        my_canvas=tkinter.Canvas(main_frame,background="grey")
        
        #create Scrollbar inside main_frame in right side
        scrollbar=ttk.Scrollbar(main_frame,orient="vertical",command=my_canvas.yview)
        scrollbar.pack(side=tkinter.RIGHT,fill=Y)

        #create Scrollbar inside main_frame in right side
        scrollbar_y=ttk.Scrollbar(main_frame,orient="horizontal",command=my_canvas.xview)
        scrollbar_y.pack(side=tkinter.BOTTOM,fill=tkinter.X)
         
        
        my_canvas.pack(side=tkinter.LEFT,anchor="nw",fill=tkinter.BOTH,expand=1,)
        
        #connect scrollbar with canvas
        my_canvas.configure(yscrollcommand=scrollbar.set ,xscrollcommand=scrollbar_y.set)
        my_canvas.bind('<Configure>', lambda e : my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # create content frame and put it inside canvas
        frame_right = customtkinter.CTkFrame(master=my_canvas, width=right_frame_width, height=1500)
        frame_right.grid_propagate(0)  # give static fixed size to frame_right
        my_canvas.create_window((0, 0), window=frame_right, anchor="nw")

        frame_right.rowconfigure((1, 2, 3, 4, 6), weight=1)
        frame_right.rowconfigure((7, 8, 9, 10, 11, 12), weight=5)
        frame_right.columnconfigure((0, 1, 2, 3), weight=1)

        chart_title = customtkinter.CTkLabel(master=frame_right,
                                             text="Arc Diagram",
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
        create_chart_btn.grid(row=0, column=2, columnspan=2, pady=10, padx=100)

        draw_arc_diag(frame_right, arc_diagram).get_tk_widget().grid(row=1, column=0, columnspan=4, rowspan=4, pady=2,
                                                                     padx=20,
                                                                     sticky="ns")

        # function for open chart in a new window
        def open_graph():
            figure = arc_diagram.generate_chart()

            window = customtkinter.CTkToplevel(root)
            window.geometry("800x500")
            window.title(arc_diagram.get_title())

            chart = FigureCanvasTkAgg(figure, window)
            chart.get_tk_widget().pack(anchor=tkinter.N, fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)

        # function for download the graph
        def download_sample():
            location = filedialog.asksaveasfile(initialdir='.\\', title='Insert File',
                                                filetypes=[("PNG", ".png")], parent=root)

            if location is not None:
                arc_diagram.save_image(f"{location.name}.png")
                messagebox.showinfo("Chart Save", "Save Completed", parent=root)
            else:
                pass

        download_btn = customtkinter.CTkButton(master=frame_right,
                                               text="Save Chart",
                                               command=download_sample

                                               )  # font name and size in px
        download_btn.grid(row=5, column=1, rowspan=1, columnspan=2, pady=10, padx=10)

        open_graph_btn = customtkinter.CTkButton(master=frame_right,
                                                 text="Full Screen View",
                                                 command=open_graph
                                                 )
        open_graph_btn.grid(row=0, column=3, columnspan=2, pady=10, padx=10)

        # modify frame in the bottom
        modify_frame = get_arc_modify_box(frame_right, root, arc_diagram, right_frame_width)
        modify_frame.grid(row=7, column=0, rowspan=5, columnspan=4, pady=5, padx=20, sticky="nwse")
        modify_frame.grid_propagate(0)

        return main_frame
