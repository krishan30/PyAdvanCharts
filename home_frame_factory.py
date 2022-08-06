from sankey import Sankey
from chord_ import Chord_

class HomeFrameFactory():
    
    @staticmethod
    def get_home_frame(chart,root):
        
            if chart ==0:
                return Sankey.get_frame(root)
            elif chart ==1:
                return Chord_.get_frame(root)
            elif chart ==2:
                pass
                #return Directed()
           
          