from body_frames.sankey_home_frame import SankeyHome
from body_frames.arc_home_frame import ArcHome


from body_frames.sankey_modify_frame import SankeyModify
from body_frames.arc_modify_frame import ArcModify


class HomeFrameFactory():
    
    @staticmethod
    def get_home_frame(frame_no,root):
        
            if frame_no ==0:
                return SankeyHome.get_frame(root)
            elif frame_no ==1:
                return ChordHome.get_frame(root)
            elif frame_no ==2:

                return ArcHome.get_frame(root)

           
