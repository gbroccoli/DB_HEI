from tkinter import Tk, Label


class MainWindow(Tk):

    def __init__(self, title: str = "Университет"):
        super().__init__()
        self.title = title
        self.geometry("1280x720")
        self.focus_force()

        self.label = Label(
            self,
            text="Test"
        )

        self.label.grid(
            row=0,
            column=0
        )