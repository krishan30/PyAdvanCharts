from body_frames.sankey_modify_frame import SankeyModify
from body_frames.chord_modify_frame import ChordModify
from body_frames.arc_modify_frame import ArcModify
from charts.arc_diagram import ArcDiagram


class ModifyFrameFactory:

    @staticmethod
    def get_modify_frame(frame_no, root, chart_diagram, right_frame_width):

        if frame_no == 0:
            return SankeyModify.get_frame(root, chart_diagram, right_frame_width)
        elif frame_no == 1:
            return ChordModify.get_frame(root, chart_diagram, right_frame_width)
        elif frame_no == 2:
            return ArcModify.get_frame(root, chart_diagram, right_frame_width)
