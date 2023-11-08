# MIDI and TK

from tkinter import *
import mido


BG_COLOR = "blue"
MIDI_EVENT_DELAY_MS = 1000


def build_gui():
    root = Tk()  # create a root widget
    root.title("Practice Monitor v 0.1")
    root.configure(bg=BG_COLOR)
    root.minsize(1400, 1000)  # width, height
    root.maxsize(1400, 1000)
    root.geometry("1400x1000+200+100")  # width x height + x + y


    label_time_total = Label(root, text="00:00:00", font=("Helvetica", 72), bg=BG_COLOR, fg="white")
    label_time_total.pack()

    label_sessions = Label(root, text="Sessions: 0", font=("Helvetica", 32), bg=BG_COLOR, fg="white")
    label_sessions.pack()

    return root


def check_midi(app, midi_in):

    print("check_midi")
    for msg in midi_in.iter_pending():
        print(msg)

    app.after(MIDI_EVENT_DELAY_MS, check_midi, app, midi_in)  # reschedule event


app_window = build_gui()

midi_port = mido.open_input('MPKmini2:MPKmini2 MIDI 1 20:0')



app_window.after(MIDI_EVENT_DELAY_MS, check_midi, app_window, midi_port)


app_window.mainloop()



