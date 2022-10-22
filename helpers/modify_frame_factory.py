from body_frames.sankey_modify_frame import SankeyModify
from body_frames.chord_modify_frame import ChordModify
from body_frames.arc_modify_frame import ArcModify


class ModifyFrameFactory:

    @staticmethod
    def get_modify_frame(frame_no, root):

        if frame_no == 0:
            return SankeyModify.get_frame(root)
        elif frame_no == 1:
            return ChordModify.get_frame(root)
        elif frame_no == 2:
            return ArcModify.get_frame(root)
