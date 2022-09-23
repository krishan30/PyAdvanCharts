from collections import defaultdict

#import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import seaborn as sns



class SankeyChart:

    def __init__(self, path):
        self.path=path
    
    def init_datas(self):
        df = pd.read_csv(self.path)
        self.from_=df['from']
        self.to=df['to']
        self.weight=df['weight']

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
                myD['bottom'] = self.fromHeights[self.fromLabels[i - 1]]['top'] + 0.02 * self.dataFrame.weight.sum()
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
                myD['bottom'] = self.toHeights[self.toLabels[i - 1]]['top'] + 0.02 * self.dataFrame.weight.sum()
                myD['top'] = myD['bottom'] + myD['to']
                self.topEdge = myD['top']
            self.toHeights[toLabel] = myD
        
        #print(self.fromHeights)
        #print(self.toHeights)

    #
    def draw_blocks(self):
        self.xMax = self.topEdge / 4
        for fromLabel in self.fromLabels:
        
            plt.fill_between(
                [-0.02 * self.xMax, 0], #x
                2 * [self.fromHeights[fromLabel]['bottom']], # y bottom
                2 * [self.fromHeights[fromLabel]['bottom'] + self.fromHeights[fromLabel]['from_']], #y top
                #color=,
                alpha=0.99
            )
            plt.text(
                -0.05 * self.xMax,  #x
                self.fromHeights[fromLabel]['bottom'] + 0.5 * self.fromHeights[fromLabel]['from_'], #middle of vertical bar
                fromLabel,    #text
                {'ha': 'right', 'va': 'center'}, #horizontal alignment,vertical alignment
                fontsize=14
            )
        for toLabel in self.toLabels:
            plt.fill_between(
                [self.xMax, 1.02 * self.xMax], 2 * [self.toHeights[toLabel]['bottom']],
                2 * [self.toHeights[toLabel]['bottom'] + self.toHeights[toLabel]['to']],
                #color=,
                alpha=0.99
            )
            plt.text(
                1.05 * self.xMax,
                self.toHeights[toLabel]['bottom'] + 0.5 * self.toHeights[toLabel]['to'],
                toLabel,
                {'ha': 'left', 'va': 'center'},
                fontsize=14
            )
    #plot weight texts
    def draw_weight_txt(self):

        

        pass
    #
    def draw_strips(self):
        for fromLabel in self.fromLabels:
            for toLabel in self.toLabels:
               #TODO : Need to create curve lines and fill the gaps between them
                
                if len(self.dataFrame[(self.dataFrame.from_ == fromLabel) & (self.dataFrame.to == toLabel)]) > 0:
                    
                    #y values for bottom edge of strip
                    ys_b =np.linspace(self.fromHeights[fromLabel]['bottom'], self.toHeights[toLabel]['bottom'], 20)

                    #y values for top edge of strip
                    ys_t =np.linspace(self.fromHeights[fromLabel]['bottom']+ self.strips[fromLabel][toLabel], self.toHeights[toLabel]['bottom']+ self.strips[fromLabel][toLabel], 20)

                    #draw weight txt
                    y_t_f=self.fromHeights[fromLabel]['bottom']+self.strips[fromLabel][toLabel]/2
                    plt.text(
                        0.05 * self.xMax,  #x
                        y_t_f, #middle of strip
                        self.dataFrame[(self.dataFrame.from_ == fromLabel) & (self.dataFrame.to == toLabel)].weight.sum(),    #text
                        {'ha': 'right', 'va': 'center'}, #horizontal alignment,vertical alignment
                        fontsize=6
                    )

                    y_t_t=self.toHeights[toLabel]['bottom']+self.strips[fromLabel][toLabel]/2
                    plt.text(
                        0.95 * self.xMax,  #x
                        y_t_t, #middle of strip
                        self.dataFrame[(self.dataFrame.from_ == fromLabel) & (self.dataFrame.to == toLabel)].weight.sum(),    #text
                        {'ha': 'right', 'va': 'center'}, #horizontal alignment,vertical alignment
                        fontsize=6
                    )


                    # Update bottom edges at each label so next strip starts at the right place
                    self.fromHeights[fromLabel]['bottom'] += self.strips[fromLabel][toLabel]
                    self.toHeights[toLabel]['bottom'] += self.strips[fromLabel][toLabel]
                   
                    plt.plot(np.linspace(0, self.xMax, len(ys_b)),ys_b)
                    plt.plot(np.linspace(0, self.xMax, len(ys_t)),ys_t)

    def generate_chart(self):
        self.init_datas()
        self.find_labels()
        self.strip_height()
        self.block_position()

        self.figure=plt.figure()
        plt.rc('text', usetex=False)
        plt.rc('font', family='serif')

        self.draw_blocks()
        self.draw_strips()

        #plt.gca().axis('off') #get the current Axes and remove it
        plt.gcf().set_size_inches(6, 6)
        return self.figure
       