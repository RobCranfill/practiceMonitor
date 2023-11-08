# first TK experiments

from tkinter import *
from tkinter import ttk

root_widget = Tk()
frame = ttk.Frame(root_widget, padding=10, name="cran")
frame.grid()

# ttk.Label(frame, text="Hello Cran!").grid(column=0, row=0)

label = ttk.Label(
    frame,
    text="Hello, Cranface!",
    foreground="white",  # Set the text color to white
    background="black"   # Set the background color to black
    )
label.grid(column=0, row=0)

ttk.Button(frame, text="Quit", command=root_widget.destroy).grid(column=1, row=1)

root_widget.mainloop()


