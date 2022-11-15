import tkinter
import customtkinter
from tkinter import filedialog, Y, ttk, messagebox
import tkinter.messagebox
import customtkinter
import components.custom_table as custom_table
from helpers.graphs import *
import pandas as pd

from components.upload_box import get_upload_box


class ArcHome():

    @staticmethod
    def get_frame(root, arc_diagram, right_frame_width):

        # arc_diagram = ArcDiagram("./csv_samples/arc_sample.csv")

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
        chart_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # function for navigate to bottom part(upload box)
        def go_bottom():
            my_canvas.yview_moveto('1.0')

        create_chart_btn = customtkinter.CTkButton(master=frame_right,
                                                   text="Create Arc",
                                                   command=go_bottom
                                                   )
        create_chart_btn.grid(row=0, column=2, columnspan=2, pady=10, padx=10)

        data_table = custom_table.get_table_for_arc(frame_right)
        data_table.grid(row=1, column=0, columnspan=2, rowspan=4, pady=2, padx=20, sticky="nswe")

        # ==================Play with different graphs========================

        # draw_simple_matplotlib_chart(frame_right)
        draw_arc_diag(frame_right, arc_diagram).get_tk_widget().grid(row=1, column=2, columnspan=2, rowspan=4, pady=2, padx=20,
                                                      sticky="ns")

        # draw_simple_seaborn_chart(frame_right)
        # draw_iris_data(frame_right)

        # function for open chart in a new window
        def open_graph():
            # arc_diagram = ArcDiagram("./csv_samples/arc_sample.csv")
            figure = arc_diagram.generate_chart()

            window = customtkinter.CTkToplevel(root)
            window.geometry("800x500")
            window.title("Sample arc diagram")

            chart = FigureCanvasTkAgg(figure, window)
            chart.get_tk_widget().pack(anchor=tkinter.N, fill=tkinter.BOTH, expand=True, side=tkinter.LEFT)

        #function for download the sample csv file
        def download_sample():
            location=filedialog.asksaveasfile(initialdir='.\\', title='Insert File',
                                          filetypes=[("CSV", ".csv")], parent=root)

            df = pd.read_csv("./csv_samples/arc_diagram.csv")
 
            dataFrame = pd.DataFrame({'Source': df['Source'], 'Target':df['Target'], 'Weight': df['Weight']
                              }, index=range(len(df['Source'])))
            if location is not None:
                dataFrame.to_csv(f"{location.name}.csv")
                messagebox.showinfo("CSV File", "Save Completed", parent=root)
            else:
                pass

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
        text_frame.insert(tkinter.END, "An arc diagram is a special kind of network graph. "
                                       "It is consituted by nodes that represent entities and by links that show "
                                       "relationships between entities. In arc diagrams, nodes are displayed along a "
                                       "single axis and links are represented with arcs. Thickness of the lines are vary "
                                       "according to the amount of wight between two nodes related.\n\n"
                                       "Nodes are in sorted order and viewer can find required node by following the "
                                       "order from the leftmost node to the rightmost node in the graph. This diagram makes "
                                       "easier to make clusters of data based on relationship between them. This chart type "
                                       "useful to visualize interactions between two objects(people) such as interactions "
                                       "between two accounts in a social media network.")
        text_frame.grid(row=6, column=0, columnspan=4, pady=20, padx=20, sticky="ew")

        # upload frame in the bottom
        upload_frame = get_upload_box(frame_right, root, 2, right_frame_width)
        upload_frame.grid(row=7, column=0, rowspan=4, columnspan=4, pady=100, padx=100, sticky="nswe")
        upload_frame.grid_propagate(0)

        """
        #modify frame in the bottom
        modify_frame=customtkinter.CTkFrame(master=frame_right)
        modify_frame.grid(row=12, column=0, rowspan=4,columnspan=4,pady=100,padx=200)
        modify_frame.grid_propagate(0)
        """
        return main_frame
