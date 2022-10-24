from tkinter import messagebox


class ErrorHandler:

    def __init__(self):
        pass

    @classmethod
    def handle_errors(cls, error_title, error_message,parent_window):
        messagebox.showerror(error_title, error_message,parent=parent_window)

    @classmethod
    def handle_invalid_errors(cls, invalid_error_title, invalid_error_message,parent_window):
        messagebox.showinfo(invalid_error_title, invalid_error_message,parent=parent_window)

