from home_body_frames.sankey_home_frame import SankeyHome
from home_body_frames.chord_home_frame import ChordHome
from home_body_frames.arc_home_frame import ArcHome


class HomeFrameFactory():

    @staticmethod
    def get_home_frame(frame_no, root, right_frame_width):

        if frame_no == 0:
            return SankeyHome.get_frame(root, right_frame_width)
        elif frame_no == 1:
            return ChordHome.get_frame(root, right_frame_width)
        elif frame_no == 2:
            return ArcHome.get_frame(root, right_frame_width)
