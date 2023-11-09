# MIDI and TK

from tkinter import *
import mido

import PracticeDisplay3


BG_COLOR = "blue"
MIDI_EVENT_DELAY_MS = 100


def build_gui():
    root = Tk()  # create a root widget
    root.title("Practice Monitor v 0.1")
    root.configure(bg=BG_COLOR)
    root.minsize(1400, 600)  # width, height
    root.maxsize(1400, 600)
    root.geometry("1400x600+200+100")  # width x height + x + y


    label_time_total = Label(root, text="00:00:00", font=("Helvetica", 72), bg=BG_COLOR, fg="white")
    label_time_total.pack()

    label_sessions = Label(root, text="Sessions: 0", font=("Helvetica", 32), bg=BG_COLOR, fg="white")
    label_sessions.pack()

    label_notes = Label(root, text="Notes: 0", font=("Helvetica", 32), bg=BG_COLOR, fg="white")
    label_notes.pack()

    return root


g_event_count = 0

def check_midi(app, midi_in, display):
    global g_event_count

    for msg in midi_in.iter_pending():
        g_event_count += 1
        print(f" {g_event_count} - {msg}")
        display.set_time_total(f"Count: {g_event_count}")

    app.after(MIDI_EVENT_DELAY_MS, check_midi, app, midi_in, display)  # reschedule event


# app_window = build_gui()
pd = PracticeDisplay3.PracticeDisplay()
app_window = pd.get_root()

midi_port = mido.open_input('MPKmini2:MPKmini2 MIDI 1 20:0')

app_window.after(MIDI_EVENT_DELAY_MS, check_midi, app_window, midi_port, pd)
app_window.mainloop()



