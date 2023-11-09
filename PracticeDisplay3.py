# for PracticeMonitor

from tkinter import *

BG_COLOR = "blue"

class PracticeDisplay():

    def __init__(self):

        root = Tk()  # create a root widget
        root.title("Practice Monitor v 0.1")
        root.configure(bg=BG_COLOR)
        root.minsize(1400, 600)  # width, height
        root.maxsize(1400, 600)
        root.geometry("1400x600+200+100")  # width x height + x + y

        self.label_time_total = Label(root, text="00:00:00", font=("Helvetica", 72), bg=BG_COLOR, fg="white")
        self.label_time_total.pack()

        self.label_time_session = Label(root, text="00:00:00", font=("Helvetica", 72), bg=BG_COLOR, fg="white")
        self.label_time_session.pack()

        self.label_sessions = Label(root, text="Sessions: 0", font=("Helvetica", 32), bg=BG_COLOR, fg="white")
        self.label_sessions.pack()

        self.label_notes = Label(root, text="Notes: 0", font=("Helvetica", 32), bg=BG_COLOR, fg="white")
        self.label_notes.pack()

        self.root = root


    def get_root(self):
        return self.root
    
    def set_time_total(self, label_string):
        self.label_time_total["text"] = label_string

    def set_time_session(self, label_string):
        self.label_time_session["text"] = label_string

    def set_time_session_fg(self, str_color):
        self.label_time_session["fg"] = str_color

    def set_session_label(self, label_string):
        self.label_sessions["text"] = label_string

    def set_notes_label(self, label_string):
        self.label_notes["text"] = label_string

