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


def format_seconds(n_seconds):
    return f"00:{(n_seconds // 60):02}:{(n_seconds % 60):02}"

def main_loop(display, midi_in):

    # for current session
    session_start_time = None
    session_note_count = 0

    # for all time - or as long as the app has run (TODO: persistence)
    total_session_count = 0
    total_practice_time = 0

    event_time = int(time.time())
    last_event_time = 0
    in_session = False

    while True:

        # print("Looking for MIDI events...")

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

            session_note_count += 1
            display.set_notes_label(f"Notes: {session_note_count}")

            event_time = int(time.time())

            # start a new session?
            if not in_session:

                in_session = True
                total_session_count += 1
                print(f"Starting session #{total_session_count}")

                display.set_session_label(f"Session: {total_session_count}")
                display.set_time_session_fg("white")

                session_note_count = 1
                session_start_time = event_time

            last_event_time = event_time
        
        # if notes_in_queue > 0:
        #     print(f"done processing MIDI queue of {notes_in_queue}")

        if in_session:

            now_time = int(time.time())
            if now_time > last_event_time:

                current_session_time = now_time - session_start_time

                # WRONG! FIXME:
                # ONLY UPDATE THIS WHEN SESSION ENDS
                # total_practice_time = current_session_time

                display.set_time_total(format_seconds(int(total_practice_time + current_session_time)))
                display.set_time_session(format_seconds(int(current_session_time)))

                # end session?
                if now_time - SESSION_TIMEOUT_SEC > last_event_time:
                    in_session = False

                    # update total_practice_time; TODO: persist this
                    total_practice_time += current_session_time
                    
                    print(f"Ending session #{total_session_count}")
                    print(  f"\n *** OUTPUT: {total_session_count}"
                        + f"\t{session_note_count}"
                        + f"\t{time.ctime(session_start_time)}"
                        + f"\t{time.ctime(now_time)}")
                    
                    last_event_time = now_time
                    display.set_time_session_fg("black")

        # print(f"Done. Sleeping {MIDI_EVENT_DELAY_S} seconds.")
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
