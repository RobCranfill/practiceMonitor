# MIDI and TK

from tkinter import *
import time

import mido

import PracticeDisplay3


BG_COLOR = "blue"
MIDI_EVENT_DELAY_MS = 100
SESSION_TIMEOUT_SEC =  10


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

# FIXME: no globals - how?
g_session_count = 0
g_session_note_count = 0
g_event_count = 0
g_last_event_time = 0
g_overall_start_time = time.time()
g_event_time = time.time()
g_session_data = {}
g_inSession = False


def check_midi(app, midi_in, display):
    global g_session_count
    global g_session_note_count
    global g_event_count
    global g_event_count
    global g_last_event_time
    global g_overall_start_time
    global g_event_time
    global g_session_data
    global g_inSession

    for msg in midi_in.iter_pending():

        if msg.type != 'note_on':
            # print("  ^^ ignoring")
            continue

        g_event_count += 1
        # print(f" {g_event_count} - {msg}")
        display.set_notes_label(f"Notes: {g_event_count}")

        g_session_note_count += 1
        # print(f" note #{g_session_note_count} of session {g_session_count} at {(event_time-g_overall_start_time):.0f}")

        g_event_time = time.time()
        if g_inSession:
            pass
        else:
            g_session_count += 1
            print(f"Starting session #{g_session_count}")
            g_session_note_count = 1
            g_session_start_time = g_event_time
            g_inSession = True
        g_last_event_time = g_event_time
    
    # print("done processing queue")

    if g_inSession:
        g_now_time = time.time()
        if g_now_time - SESSION_TIMEOUT_SEC > g_last_event_time:
            g_inSession = False
            print(f"Ending session #{g_session_count}")
            print(f"\n *** OUTPUT: {g_session_count}"
                  + "\t{g_session_note_count}"
                  + "\t{time.ctime(g_session_start_time)}"
                  + "\t{time.ctime(g_now_time)}")
            g_last_event_time = g_now_time


    # reschedule event
    app.after(MIDI_EVENT_DELAY_MS, check_midi, app, midi_in, display)


# app_window = build_gui()
pd = PracticeDisplay3.PracticeDisplay()
app_window = pd.get_root()

midi_port = mido.open_input('MPKmini2:MPKmini2 MIDI 1 20:0')

app_window.after(MIDI_EVENT_DELAY_MS, check_midi, app_window, midi_port, pd)
app_window.mainloop()



