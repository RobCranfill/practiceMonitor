# practice monitor - desktop version
# for Python 3.x, Linux, keyboard plugged into desktop
# robcranfill@gmail.com

# stdlibs
import sys
from tkinter import *
import time

# added libs (see requirements.txt)
import mido

# our code
import PracticeDisplay5 as PracticeDisplay


# TODO: how to configure this? discover?
MIDI_DEVICE_NAME = "MPKmini2:MPKmini2 MIDI 1 20:0"

BG_COLOR = "blue"
MIDI_EVENT_DELAY_MS = 100
SESSION_TIMEOUT_SEC =  10




# ------ FIXME: better with no globals - how?

# for all time - or as long as the app has run (TODO: persistence across invocations)
g_total_session_count = 0
g_running_total_time = 0

g_event_time = time.time()
g_last_event_time = 0
g_in_session = False

# for current session
g_session_start_time = None
g_session_note_count = 0

# ------ end of globals


def format_seconds(n_seconds):
    return f"00:{(n_seconds // 60):02}:{(n_seconds % 60):02}"


# Our main MIDI processing loop.
# This is called by the TKinter event loop, and calls itself again when done.
#
def check_midi(app, midi_in, display):
    global g_event_time         # all times are integer - good enough for this!
    global g_session_start_time
    global g_session_note_count
    global g_total_session_count
    global g_running_total_time
    global g_last_event_time
    global g_in_session

    # first handle all MIDI messages
    for msg in midi_in.iter_pending():

        # OK, not *all* messages!
        if msg.type != 'note_on':
            # print(f"* ignoring: {msg}")
            continue

        g_event_time = int(time.time())

        # start a new session?
        if not g_in_session:
            g_total_session_count += 1

            print(f"Starting session #{g_total_session_count}")
            display.set_session_label(f"Session: {g_total_session_count}")
            display.set_time_session_fg("white")

            g_session_note_count = 1
            g_session_start_time = g_event_time
            g_in_session = True

        g_last_event_time = g_event_time
    
    # print("done processing queue")

    # Then update the display; we only need to do that inside a session (right?)
    if g_in_session:

        # we will only update g_running_total_time at the end of each session

        g_now_time = int(time.time())
        if g_last_event_time != g_now_time:

            current_session_time = g_now_time - g_session_start_time

            display.set_time_total(format_seconds(g_running_total_time + current_session_time))
            display.set_time_session(format_seconds(current_session_time))

        # end session?
        if g_now_time - SESSION_TIMEOUT_SEC > g_last_event_time:
            g_in_session = False

            # update g_running_total_time; TODO: persist this
            g_running_total_time += current_session_time

            print(f"Ending session #{g_total_session_count}")
            print(  f"\n *** OUTPUT: {g_total_session_count}"
                + f"\t{g_session_note_count}"
                + f"\t{time.ctime(g_session_start_time)}"
                + f"\t{time.ctime(g_now_time)}")
            
            g_last_event_time = g_now_time
            display.set_time_session_fg("black")


    # reschedule event
    app.after(MIDI_EVENT_DELAY_MS, check_midi, app, midi_in, display)


# Code start
#
pd = PracticeDisplay.PracticeDisplay()
pd.set_session_label(f"Session: 0")
pd.set_notes_label(f"Notes: 0")

pd.set_time_session_fg("black")

app_window = pd.get_root()

try:
    midi_port = mido.open_input(MIDI_DEVICE_NAME)
except Exception as e:
    print(e)
    print("No MIDI device '{MIDI_DEVICE_NAME}'? Stopping.")
    sys.exit(1)

app_window.after(MIDI_EVENT_DELAY_MS, check_midi, app_window, midi_port, pd)
app_window.mainloop()

