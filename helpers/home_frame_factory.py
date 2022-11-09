from body_frames.sankey_home_frame import SankeyHome
from body_frames.chord_home_frame import ChordHome
from body_frames.arc_home_frame import ArcHome
from charts.arc_diagram import ArcDiagram
from charts.chord_chart import ChordChart
from charts.sankey_chart import SankeyChart


class HomeFrameFactory():

    @staticmethod
    def get_home_frame(frame_no, root, right_frame_width):

        if frame_no == 0:
            return SankeyHome.get_frame(root, right_frame_width)
        elif frame_no == 1:
            return ChordHome.get_frame(root, ChordChart(path="./csv_samples/sankey_sample.csv"), right_frame_width)
        elif frame_no == 2:
            return ArcHome.get_frame(root, ArcDiagram(path="./csv_samples/arc_sample.csv"), right_frame_width)
