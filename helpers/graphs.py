import pandas as pd
import numpy as np
import seaborn as sns
from string import ascii_letters
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from charts.sankey_chart import SankeyChart
from charts.chord_chart import ChordChart


#function for drawing our sankey chart
def draw_sankey(root):
    sankeychart=SankeyChart("./csv_samples/sankey_sample.csv")
    figure = sankeychart.generate_chart()
   
    chart = FigureCanvasTkAgg(figure, root)
    return chart
    #chart.get_tk_widget().grid(row=1, column=2,columnspan=2, rowspan=4, pady=2, padx=20, sticky="ns")

#function for drawing  chord chart
def draw_chord(root):
    chord_chart=ChordChart("./csv_samples/sankey_sample.csv")
    figure = chord_chart.generate_graph()
    chart = FigureCanvasTkAgg(figure, root)
    return chart



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

