import ctypes
import sys

import customtkinter

from helpers.home_frame_factory import HomeFrameFactory
import components.tab_layout as tab_layout

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.iconbitmap("pac3.ico")

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        self.width = self.winfo_screenwidth() // scaleFactor
        self.height = self.winfo_screenheight()//scaleFactor

        self.left_frame_width = self.width * 0.174
        self.right_frame_width = self.width * 0.826

        self.title("PyAdvanceCharts")
        self.geometry(f"{self.width}x{self.height}")

        self.minsize(self.width * 0.75, self.height * 0.75)
        self.state('zoomed')

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_right = HomeFrameFactory.get_home_frame(0, self, self.right_frame_width)  # declare home
        self.frame_left = tab_layout.get_tab_frame(self, self.left_frame_width,
                                                   self.right_frame_width)  # declare vertical tab


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", sys.exit)
    app.mainloop()
