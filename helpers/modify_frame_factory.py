from modify_body_frames.sankey_modify_frame import SankeyModify
from modify_body_frames.chord_modify_frame import ChordModify
from modify_body_frames.arc_modify_frame import ArcModify



class ModifyFrameFactory:

    @staticmethod
    def get_modify_frame(frame_no, root, chart_diagram):
        print(frame_no)
        if frame_no == 0:
            return SankeyModify.get_frame(root,chart_diagram)
        elif frame_no == 1:
            return ChordModify.get_frame(root, chart_diagram)
        elif frame_no == 2:
            return ArcModify.get_frame(root,chart_diagram)
