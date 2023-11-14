# PracticeMonitor for RPi Zero
# robcranfill@gmail.com

# standard libs
import sys
import time

# installed libs
import mido

# our code
import PracticeDisplay2 as PracticeDisplay


BG_COLOR = "blue"
MIDI_EVENT_DELAY_S = 0.1
SESSION_TIMEOUT_SEC =  10




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

def main_loop(display, midi_in):

    global g_session_start_time
    global g_session_note_count
    global g_total_session_count
    global g_total_session_time
    global g_event_time
    global g_last_event_time
    global g_in_session


    while True:

        print("looping")

        # process all events
        #
        notes_in_queue = 0 # just for fun and debugging
        for msg in midi_in.iter_pending(): # non-blocking queue

            notes_in_queue += 1
            print(f"{notes_in_queue}: {msg}")

            # OK, not *all* messages!
            if msg.type != 'note_on':
                # print(f"* ignoring: {msg}")
                continue

            g_session_note_count += 1
            display.set_notes_label(f"Notes: {g_session_note_count}")

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
        
        print(f"done processing queue of {notes_in_queue}")

        if g_in_session:

            g_now_time = int(time.time())
            if g_now_time > g_last_event_time:

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

        print("Done. Sleeping")
        time.sleep(MIDI_EVENT_DELAY_S)

    # end main_loop


pd = PracticeDisplay.PracticeDisplay()
pd.set_session_label(f"Session: 0")
pd.set_notes_label(f"Notes: 0")
pd.set_time_session_fg("black")


# 'MPKmini2:MPKmini2 MIDI 1 20:0'
try:
    
    # TODO: figure this out
    inputs = mido.get_input_names()
    # portName = inputs[1]
    portName = None
    for i in inputs:
        if i.find("MPK") != -1:
            portName = i
    if portName is None:
        print("Can't find MPK!")
        sys.exit(1)
    print(f"Using MIDI port {portName}")
    midi_port = mido.open_input(portName)
except Exception as e:
    print(e)
    sys.exit(1)

# Mainly for keyboard interrupt?
try:
    main_loop(pd, midi_port)
except Exception as e:
    print(e)
    pd.set_backlight_on(False)
