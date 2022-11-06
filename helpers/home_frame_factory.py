from home_body_frames.sankey_home_frame import SankeyHome
from home_body_frames.chord_home_frame import ChordHome
from home_body_frames.arc_home_frame import ArcHome
from charts.arc_diagram import ArcDiagram
from charts.chord_chart import ChordChart

class HomeFrameFactory():
    
    @staticmethod
    def get_home_frame(frame_no,root):
        
            if frame_no ==0:
                return SankeyHome.get_frame(root)
            elif frame_no ==1:
                return ChordHome.get_frame(root,ChordChart("./csv_samples/sankey_sample.csv"))
            elif frame_no ==2:
                return ArcHome.get_frame(root, ArcDiagram("./csv_samples/arc_sample.csv"))