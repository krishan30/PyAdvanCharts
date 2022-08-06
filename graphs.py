import pandas as pd
import numpy as np
import seaborn as sns
from string import ascii_letters
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




def draw_simple_matplotlib_chart(root):
    x = np.linspace(0, 10, 100)
    y = 4 + 2 * np.sin(2 * x)   

    figure = plt.figure(figsize = (3,2), dpi = 100)
    a=figure.add_subplot(111).plot(x, y, linewidth=2.0)
  
    
    chart = FigureCanvasTkAgg(figure, root)
    chart.get_tk_widget().grid(row=1, column=2,columnspan=2, rowspan=4, pady=2, padx=20, sticky="ns")

def draw_simple_seaborn_chart(root):
    sns.set(style="white")

    # Generate a large random dataset
    rs = np.random.RandomState(33)
    d = pd.DataFrame(data=rs.normal(size=(100, 26)),
                     columns=list(ascii_letters[26:]))

    # Compute the correlation matrix
    corr = d.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(3, 2))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    canvas = FigureCanvasTkAgg(f, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=2,columnspan=2, rowspan=4, pady=2, padx=20, sticky="ns")

def draw_iris_data(root):
    df = pd.read_csv('https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv')
    df_setosa = df.loc[df['species']=='setosa']
    df_virginica = df.loc[df['species'] == 'virginica']
    df_versicolor = df.loc[df['species'] == 'versicolor']

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(3, 2))

    plt.plot(df_setosa['sepal_length'], np.zeros_like(df_setosa['sepal_length']), 'D')
    plt.plot(df_virginica['sepal_length'], np.zeros_like(df_virginica['sepal_length']), 'D')
    plt.plot(df_versicolor['sepal_length'], np.zeros_like(df_versicolor['sepal_length']), 'D')
    plt.xlabel('Petal length')
    
    canvas = FigureCanvasTkAgg(f, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=2,columnspan=2, rowspan=4, pady=2, padx=20, sticky="ns")

from mne_connectivity.viz import plot_connectivity_circle
def draw_chord(root):

    N = 20  # Number of nodes
    node_names = [f"N{i}" for i in range(N)]  # List of labels [N]

    # Random connectivity
    ran = np.random.rand(N,N)
    con = np.where(ran > 0.9, ran, np.nan)  # NaN so it doesn't display the weak links
    # Set up the matplotlib figure
    fig = plt.figure(num=None, figsize=(3, 2), facecolor='grey')
    f, ax = plot_connectivity_circle(con, node_names,fig=fig) 
    
   
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=2,columnspan=2, rowspan=4, pady=2, padx=20, sticky="ns")


from tkinterweb import HtmlFrame
from chord import Chord
def draw_chord_1(root):
    frame = HtmlFrame(root) #create HTML browser
    
    # reading data from csv
    df = pd.read_csv("housing.csv")
    # List of columns to delete and then dropping them.
    #delete = ['ZN', 'INDUS', 'CHAS', 'DIS','RAD','PTRATIO','B','LSTAT']
    #df.drop(delete, axis=1, inplace=True)
    # Now, matrix contains a 6x6 matrix of the values.
    matrix = df.corr()
    # Replacing negative values with 0’s, as features can be negatively correlated.
    matrix[matrix < 0] = 0
    # Multiplying all values by 100 for clarity, since correlation values lie b/w 0 and 1.
    matrix = matrix.multiply(100).astype(int)
    # Converting the DataFrame to a 2D List, as it is the required input format.
    matrix = matrix.values.tolist()

    # Names of the features.
    names = ["Crime Rate","N-Oxide","Number of rooms","Older buildings","Property Tax","Median Price"]
   
    Chord(matrix, names).to_html()
    frame.load_file("file:///C:/Users/wextr/Desktop/PyAdvanCharts/out.html")
    #frame.load_website("http://tkhtml.tcl.tk/tkhtml.html") #load a website
    frame.grid(row=1, column=2,columnspan=2, rowspan=4, pady=2, padx=20)

import plotly.express as px    
def draw_plotly(root):
    frame = HtmlFrame(root) #create HTML browser
    
    df = px.data.iris()
    fig = px.parallel_coordinates(
    df, 
    color="species_id", 
    labels={"species_id": "Species","sepal_width": "Sepal Width", "sepal_length": "Sepal Length", "petal_width": "Petal Width", "petal_length": "Petal Length", },
    color_continuous_scale=px.colors.diverging.Tealrose,
    color_continuous_midpoint=2)

    # Hide the color scale that is useless in this case
    fig.update_layout(coloraxis_showscale=False)

    fig.write_html("plotly_chord.html")
    frame.load_file("file:///C:/Users/wextr/Desktop/PyAdvanCharts/iframe.html")
    #frame.load_website("http://tkhtml.tcl.tk/tkhtml.html") #load a website
    frame.grid(row=1, column=2,columnspan=2, rowspan=4, pady=2, padx=20, sticky="ns")