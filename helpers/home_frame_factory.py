from body_frames.sankey_home_frame import SankeyHome

from body_frames.sankey_modify_frame import SankeyModify
class HomeFrameFactory():
    
    @staticmethod
    def get_home_frame(frame_no,root):
        
            if frame_no ==0:
                return SankeyHome.get_frame(root)
            elif frame_no ==1:
                return SankeyHome.get_frame(root)
            elif frame_no ==2:
                return SankeyModify.get_frame(root)
                pass
                #TODO :Return Directed chart frame
                #return Directed()
           
          