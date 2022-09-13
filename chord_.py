import tkinter
from tkinter import Y, ttk
import tkinter.messagebox
import customtkinter
import custom_table
from graphs import *

class Chord_():

    @staticmethod   
    def  get_frame(root):
        def progressar():
            pass
        
        #set home frame grid
        main_frame = customtkinter.CTkFrame(master=root)
        main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        #create canvas inside main_frame in left side
        my_canvas=tkinter.Canvas(main_frame,background="grey")
        my_canvas.pack(side=tkinter.LEFT,anchor="nw",fill=tkinter.BOTH,expand=1,)
        
        #create Scrollbar inside main_frame in right side
        scrollbar=ttk.Scrollbar(main_frame,orient="vertical",command=my_canvas.yview)
        scrollbar.pack(side=tkinter.RIGHT,fill=Y)

        #connect scrollbar with canvas
        my_canvas.configure(yscrollcommand=scrollbar.set)
        my_canvas.bind('<Configure>', lambda e : my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        
        #create content frame and put it inside canvas
        frame_right = customtkinter.CTkFrame(master=my_canvas,width=1300,height=1500)
        frame_right.grid_propagate(0)   #give static fixed size to frame_right
        my_canvas.create_window((0,0),window=frame_right,anchor="nw")

        frame_right.rowconfigure((1, 2, 3,4,6), weight=1)
        frame_right.rowconfigure((7,8,9,10,11,12), weight=5)
        frame_right.columnconfigure((0, 1,2,3), weight=1)
    

        chart_title = customtkinter.CTkLabel(master=frame_right,
                                                text="Chord Diagram",
                                                text_font=("Roboto Medium", -16),
                                                
                                                )  # font name and size in px
        chart_title.grid(row=0, column=0, pady=10)

        create_chart_btn = customtkinter.CTkButton(master=frame_right,
                                                text="Create Chord Diagram",
                                                command=progressar
                                    )
        create_chart_btn.grid(row=0, column=3, pady=10)

        data_table=custom_table.get_table(frame_right)
        data_table.grid(row=1, column=0,columnspan=2, rowspan=4, pady=2, padx=10, sticky="nswe")

        #==================Play with different graphs========================

        #draw_simple_matplotlib_chart(frame_right)
        #draw_simple_seaborn_chart(frame_right)
        draw_iris_data(frame_right)
        #draw_chord(frame_right)
        #draw_chord_1(frame_right)
        #draw_plotly(frame_right)

        file_name_label = customtkinter.CTkLabel(master=frame_right,
                                                text="exmple.csv",
                                                text_font=("Roboto Medium", -16),
                                                anchor="center",
                                                text_color="blue"
                                                )  # font name and size in px
        file_name_label.grid(row=5, column=0,columnspan=2, pady=1,padx=10)

        open_graph_btn = customtkinter.CTkButton(master=frame_right,
                                                text="Open",
                                                command=lambda : draw_simple_matplotlib_chart(frame_right)
                                    )
        open_graph_btn.grid(row=5, column=3, pady=10)


        text_frame=tkinter.Text(frame_right,padx=20,width=10,height=8,background="#A7C2E0",wrap=tkinter.CHAR)
        text_frame.insert(tkinter.END,"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
        text_frame.grid(row=6, column=0,columnspan=4, pady=1,padx=20,sticky="ew")

        upload_frame=customtkinter.CTkFrame(master=frame_right, height=280)
        upload_frame.grid(row=7, column=0, rowspan=4,columnspan=4,pady=10,padx=20)
        upload_frame.grid_propagate(0)
    

        #TODO we need to implement kirusan's upload box
        label_3 = customtkinter.CTkLabel(master=upload_frame,
                                                text="Kirusan's upload box",
                                                text_font=("Roboto Medium", -16),
                                            
                                                )  
        label_3.pack(pady=230,padx=260)

        return main_frame