from body_frames.sankey_modify_frame import SankeyModify


class ModifyFrameFactory():
    
    @staticmethod
    def get_modify_frame(frame_no,root):
        
            if frame_no ==0:
                return SankeyModify.get_frame(root)
            elif frame_no ==1:
                pass
            elif frame_no ==2:
                pass
            
                #TODO :
                #return Directed()
           
          