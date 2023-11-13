# PracticeMonitor for RPi Zero
# robcranfill@gmail.com

import time

import mido

import PracticeDisplay2 as PracticeDisplay


BG_COLOR = "blue"
MIDI_EVENT_DELAY_MS = 100
SESSION_TIMEOUT_SEC =  10

# display shows
#   RUNNING TOTAL TIME
#   CURRENT SESSION TIME
#   SESSION NUMBER
#   NOTES THIS SESSION


# FIXME: better with no globals - how?

# for current session
g_session_start_time = None
g_session_note_count = 0

# for all time - or as long as the app has run (TODO: persistence)
g_total_session_count = 0
g_total_session_time = 0

g_event_time = time.time()
g_last_event_time = 0
g_in_session = False


def format_seconds(n_seconds):
    return f"00:{(n_seconds // 60):02}:{(n_seconds % 60):02}"

def check_midi(app, midi_in, display):
    global g_session_start_time
    global g_session_note_count
    global g_total_session_count
    global g_total_session_time
    global g_event_time
    global g_last_event_time
    global g_in_session

    # handle all MIDI messages
    for msg in midi_in.iter_pending():

        # OK, not *all* messages!
        if msg.type != 'note_on':
            # print(f"* ignoring: {msg}")
            continue

        g_session_note_count += 1
        display.set_notes_label(f"Notes: {g_session_note_count}")

        g_event_time = time.time()

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

    if g_in_session:

        g_now_time = time.time()
        current_session_time = g_now_time - g_session_start_time
        g_total_session_time += current_session_time

        display.set_time_total(format_seconds(int(g_total_session_time)))
        display.set_time_session(format_seconds(int(current_session_time)))

        # end session?
        if g_now_time - SESSION_TIMEOUT_SEC > g_last_event_time:
            g_in_session = False

            print(f"Ending session #{g_total_session_count}")
            print(  f"\n *** OUTPUT: {g_total_session_count}"
                  + f"\t{g_session_note_count}"
                  + f"\t{time.ctime(g_session_start_time)}"
                  + f"\t{time.ctime(g_now_time)}")
            
            g_last_event_time = g_now_time
            display.set_time_session_fg("black")


    # reschedule event
    app.after(MIDI_EVENT_DELAY_MS, check_midi, app, midi_in, display)


pd = PracticeDisplay.PracticeDisplay()
pd.set_session_label(f"Session: 0")
pd.set_notes_label(f"Notes: 0")

pd.set_time_session_fg("black")

app_window = pd.get_root()

midi_port = mido.open_input('MPKmini2:MPKmini2 MIDI 1 20:0')

app_window.after(MIDI_EVENT_DELAY_MS, check_midi, app_window, midi_port, pd)
app_window.mainloop()



