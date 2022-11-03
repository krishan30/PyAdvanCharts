from collections import defaultdict

#import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns



class SankeyChart:

    def __init__(self, path):
        self.path=path
        
        self.init_datas()
    

    def set_color(self,block_palette,strip_palette):
        self.block_colorDict = {}
        colorPalette = sns.color_palette(block_palette, len(self.allLabels))
        for i, label in enumerate(self.allLabels):
            self.block_colorDict[label] = colorPalette[i]

        self.strip_colorDict = {}
        colorPalette = sns.color_palette(strip_palette, len(self.allLabels))
        for i, label in enumerate(self.allLabels):
            self.strip_colorDict[label] = colorPalette[i]

    def init_datas(self):
        df = pd.read_csv(self.path)

        self.font_size=11
        self.weight_font_size=6
        self.font_family="serif"
        self.block_palette="hls"
        self.strip_palette="hls"
        self.strip_alpha=0.65
        self.block_alpha=0.85
        self.aspect=4
        self.bg_color='white'
        self.font_color='black'
        self.graph_param=(6,6)
        self.show_weight_txt=True
        self.show_label_txt=True
        self.block_out_color=None
        self.strip_out_color=None
        self.block_vertical_margin=0.02
        self.block_h_m=0

        self.from_=df['Source']
        self.to=df['Target']
        self.weight=df['Weight']

        #remove index
        """
        if isinstance(self.from_, pd.Series):
            self.from_ = self.from_.reset_index(drop=True)
        if isinstance(self.to, pd.Series):
            self.to = self.to.reset_index(drop=True)
        """
        # Create Dataframe
        self.dataFrame = pd.DataFrame({'from_': self.from_, 'to': self.to, 'weight': self.weight
                              }, index=range(len(self.from_)))

    def find_labels(self):

        # Identify all labels that appear 'from' or 'to'
        self.allLabels = pd.Series(np.r_[self.dataFrame.from_.unique(), self.dataFrame.to.unique()]).unique()
        self.set_color(self.block_palette,self.strip_palette)
        # Identify from labels
        self.fromLabels = pd.Series(self.dataFrame.from_.unique()).unique()
       
        # Identify to labels
        self.toLabels = pd.Series(self.dataFrame.to.unique()).unique()
        #print(self.fromLabels)
        #print(self.toLabels)
    
    # Find height of each strip
    def strip_height(self):
        self.strips = defaultdict()
        for fromLabel in self.fromLabels:
            dict = {}
            for toLabel in self.toLabels:
                dict[toLabel] = self.dataFrame[(self.dataFrame.from_ == fromLabel) & (self.dataFrame.to == toLabel)].weight.sum()

            self.strips[fromLabel] = dict
            
        #print(self.strips)
       

    #find y positions of vertical blocks 
    def block_position(self):
        self.fromHeights = defaultdict()
        for i, fromLabel in enumerate(self.fromLabels):
            myD = {}
            myD['from_'] = self.dataFrame[self.dataFrame.from_ == fromLabel].weight.sum()
            if i == 0:
                myD['bottom'] = 0
                myD['top'] = myD['from_']
            else:
                myD['bottom'] = self.fromHeights[self.fromLabels[i - 1]]['top'] + self.block_vertical_margin * self.dataFrame.weight.sum()
                myD['top'] = myD['bottom'] + myD['from_']
                self.topEdge = myD['top']
            self.fromHeights[fromLabel] = myD

        
        self.toHeights = defaultdict()
        for i, toLabel in enumerate(self.toLabels):
            myD = {}
            myD['to'] = self.dataFrame[self.dataFrame.to == toLabel].weight.sum()
            if i == 0:
                myD['bottom'] = 0
                myD['top'] = myD['to']
            else:
                myD['bottom'] = self.toHeights[self.toLabels[i - 1]]['top'] + self.block_vertical_margin * self.dataFrame.weight.sum()
                myD['top'] = myD['bottom'] + myD['to']
                self.topEdge = myD['top']
            self.toHeights[toLabel] = myD
        
        #print(self.fromHeights)
        #print(self.toHeights)

    #
    def draw_blocks(self):
        self.xMax = self.topEdge / self.aspect
        for fromLabel in self.fromLabels:
        
            plt.fill_between(
                [-0.02 * self.xMax, 0], #x
                2 * [self.fromHeights[fromLabel]['bottom']], # y bottom
                2 * [self.fromHeights[fromLabel]['bottom'] + self.fromHeights[fromLabel]['from_']], #y top
                color=self.block_colorDict[fromLabel],
                alpha=self.block_alpha,
                 edgecolor=self.block_out_color
            )

            if self.show_label_txt:
                plt.text(
                    -0.05 * self.xMax,  #x
                    self.fromHeights[fromLabel]['bottom'] + 0.5 * self.fromHeights[fromLabel]['from_'], #middle of vertical bar
                    fromLabel,    #text
                    {'ha': 'right', 'va': 'center'}, #horizontal alignment,vertical alignment
                    fontsize=self.font_size
                )
        for toLabel in self.toLabels:
            plt.fill_between(
                [self.xMax, 1.02 * self.xMax], 2 * [self.toHeights[toLabel]['bottom']],
                2 * [self.toHeights[toLabel]['bottom'] + self.toHeights[toLabel]['to']],
                color=self.block_colorDict[toLabel],
                alpha=self.block_alpha,
                edgecolor=self.block_out_color
            )

            if self.show_label_txt:
                plt.text(
                    1.05 * self.xMax,
                    self.toHeights[toLabel]['bottom'] + 0.5 * self.toHeights[toLabel]['to'],
                    toLabel,
                    {'ha': 'left', 'va': 'center'},
                    fontsize=self.font_size
                )
    
    #draw strips and weight text on strips
    def draw_strips(self):
        for fromLabel in self.fromLabels:
            for toLabel in self.toLabels:
   
                if len(self.dataFrame[(self.dataFrame.from_ == fromLabel) & (self.dataFrame.to == toLabel)]) > 0:
                    
                    #y values for bottom edge of strip
                    ys_b = np.array(50 * [self.fromHeights[fromLabel]['bottom']] + 50 * [self.toHeights[toLabel]['bottom']])
                    ys_b = np.convolve(ys_b, 0.05 * np.ones(20), mode='valid')
                    ys_b = np.convolve(ys_b, 0.05 * np.ones(20), mode='valid')

                    #y values for top edge of strip
                    ys_t = np.array(50 * [self.fromHeights[fromLabel]['bottom'] + self.strips[fromLabel][toLabel]] + 50 * [self.toHeights[toLabel]['bottom'] + self.strips[fromLabel][toLabel]])
                    ys_t = np.convolve(ys_t, 0.05 * np.ones(20), mode='valid')
                    ys_t = np.convolve(ys_t, 0.05 * np.ones(20), mode='valid')


                    #draw weight txt
                    y_t_f=self.fromHeights[fromLabel]['bottom']+self.strips[fromLabel][toLabel]/2
                    if self.show_weight_txt:
                        plt.text(
                            0.05 * self.xMax,  #x
                            y_t_f, #middle of strip
                            self.dataFrame[(self.dataFrame.from_ == fromLabel) & (self.dataFrame.to == toLabel)].weight.sum(),    #text
                            {'ha': 'right', 'va': 'center'}, #horizontal alignment,vertical alignment
                            fontsize=self.weight_font_size
                        )

                    y_t_t=self.toHeights[toLabel]['bottom']+self.strips[fromLabel][toLabel]/2
                    if self.show_weight_txt:
                        plt.text(
                            0.95 * self.xMax,  #x
                            y_t_t, #middle of strip
                            self.dataFrame[(self.dataFrame.from_ == fromLabel) & (self.dataFrame.to == toLabel)].weight.sum(),    #text
                            {'ha': 'right', 'va': 'center'}, #horizontal alignment,vertical alignment
                            fontsize=self.weight_font_size
                        )


                    # Update bottom edges at each label so next strip starts at the right place
                    self.fromHeights[fromLabel]['bottom'] += self.strips[fromLabel][toLabel]
                    self.toHeights[toLabel]['bottom'] += self.strips[fromLabel][toLabel]

                    plt.fill_between(
                        np.linspace(self.block_h_m, self.xMax-self.block_h_m, len(ys_b)), #numeric sequence between 0 and xMax with length of len(ysd)
                        ys_b, ys_t, alpha=self.strip_alpha,color=self.strip_colorDict[fromLabel], edgecolor=self.strip_out_color
                    )

    def generate_chart(self):
        plt.rcParams['figure.facecolor'] = self.bg_color
        plt.rcParams['text.color'] = self.font_color
        self.find_labels()
        self.strip_height()
        self.block_position()
        
        self.figure=plt.figure()
        plt.rc('text', usetex=False)
        plt.rc('font', family=self.font_family)

        self.draw_blocks()
        self.draw_strips()
        #plt.rcParams['figure.facecolor'] = self.bg_color
        
        plt.gca().axis('off') #get the current Axes and remove it
        plt.gcf().set_size_inches(self.graph_param)
        return self.figure
    
    def save_image(self,location):
            plt.savefig(location, bbox_inches="tight", dpi=150)

    #functions for chart modification
    def set_pallete(self,block_palette,strip_palette):
        self.block_palette=block_palette
        self.strip_palette=strip_palette
        self.set_color(block_palette,strip_palette)

    def set_label_font_size(self,size):
        self.font_size=size
    
    def set_weight_font_size(self,size):
        self.weight_font_size=size

    def set_font_family(self,family):
        self.font_family=family
    
    def set_block_alpha(self,alpha):
        self.block_alpha=alpha
    
    def set_strip_alpha(self,alpha):
        self.strip_alpha=alpha
    
    def set_aspect(self,aspect):
        self.aspect=aspect
    
    def set_bg_color(self,color):
        self.bg_color=color
    
    def set_font_color(self,color):
        self.font_color=color

    def set_block_out_color(self,color):
        self.block_out_color=color    

    def set_strip_out_color(self,color):
        self.strip_out_color=color

    def set_graph_param(self,param):
        self.graph_param=param
    
    def set_show_weight_txt(self,boolean):
        self.show_weight_txt=boolean
    
    def set_show_label_txt(self,boolean):
        self.show_label_txt=boolean

    def set_block_v_m(self,value):
        self.block_vertical_margin=value
    
    def set_block_h_m(self,value):
        self.block_h_m=value
    


    def get_pallete(self):
        return self.block_palette,self.strip_palette

    def get_label_font_size(self):
        return self.font_size
    
    def get_weight_font_size(self):
        return self.weight_font_size

    def get_font_family(self):
        return self.font_family
    
    def get_block_alpha(self):
        return self.block_alpha
    
    def get_strip_alpha(self):
        return self.strip_alpha
    
    def get_aspect(self):
        return self.aspect
    
    def get_bg_color(self):
        return self.bg_color
    
    def get_font_color(self):
        return self.font_color
    
    def get_block_out_color(self):
        return self.block_out_color

    def get_strip_out_color(self):
        return self.strip_out_color

    def get_graph_param(self):
        return self.graph_param
    
    def get_show_weight_txt(self):
        return self.show_weight_txt
    
    def get_show_label_txt(self):
        return self.show_label_txt
    def get_block_v_m(self):
        return self.block_vertical_margin
    def get_block_h_m(self):
        return self.block_h_m
    def remove_block_out(self):
        self.block_out_color=None
    
    def remove_strip_out(self):
        self.strip_out_color=None