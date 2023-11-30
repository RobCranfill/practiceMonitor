# PracticeMonitor for RPi Zero
# robcranfill@gmail.com

# /mnt/pizero2w/proj/practiceMonitor/pmZero.py

# standard libs
import json
import os
import signal
import sys
import time

# installed libs
import board
import digitalio
import mido

# our code
import PracticeDisplayLCD as PracticeDisplay


# pseudo-constants
OUTPUT_JSON = True
JSON_KEY_TS     = "SeshNumber"
JSON_KEY_START  = "SeshStart"
JSON_KEY_END    = "SeshEnd"
JSON_KEY_NOTES  = "SeshNotes"

BG_COLOR = "blue"
MIDI_EVENT_DELAY_S = 0.01
SESSION_TIMEOUT_SEC =  10


# global flag to keep running or die; for SIGTERM
g_run = True

def handle_signal(signum, frame):
    global g_run

    if signum == signal.SIGINT:
        print(f"Caught SIGINT. Stopping.")
        g_run = False
    elif signum == signal.SIGUSR1:
        print(f"Caught SIGUSR1. handle it!")
        get_midi_port_and_name()
    else:
        print(f"Caught ANOTHER SIGNAL??? {signum}")


def output_record(total_sessions, session_start_sec, session_end_sec, session_notes):

    if OUTPUT_JSON:
        one_record = [{ JSON_KEY_TS:    total_sessions,
                        JSON_KEY_START: time.ctime(session_start_sec),
                        JSON_KEY_END:   time.ctime(session_end_sec),
                        JSON_KEY_NOTES: session_notes
                        }]
        print(one_record)
    else:
        print(f"\n *** OUTPUT: {total_sessions}"
            + f"\t{time.ctime(session_start_sec)}"
            + f"\t{time.ctime(session_end_sec)}"
            + f"\t{session_notes}"
            )


def set_up_shutdown_button():
    button_23 = digitalio.DigitalInOut(board.D23)
    button_23.switch_to_input()
    return button_23

def set_up_other_button():
    button_24 = digitalio.DigitalInOut(board.D24)
    button_24.switch_to_input()
    return button_24

def check_other_button(b, d):
    pushed = not b.value
    if pushed:
        print("Button 24 pressed")
        d.show_image("simple1a.png")
        time.sleep(1) # debounce


def check_shutdown_button(b, d):
    pushed = not b.value
    if pushed:
        # If running from console, gives time to hit <ctrl>C 
        print("Shutting down in 10! ^C to abort!")

        d.draw_text_in_color(4, "shutting down!", "#FF0000")
        d.update_display()

        for i in range(10, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
            pushed = not b.value
            if pushed:
                print("\nAborting shutdown!")
                d.draw_text_in_color(4, "aborting shutdown!", "#00FF00")
                d.update_display()

                time.sleep(1) # debounce

                d.draw_text_in_color(4, "", "#000000")
                d.update_display()

                return
        d.clear_display()
        d.set_backlight_on(False)
        os.system('sudo poweroff')


def main_loop(disp, midi_port):

    # when this goes False, we stop procesing events
    global g_run

    shutdown_button = set_up_shutdown_button()
    other_button = set_up_other_button()

    # for current session
    session_start_time = None
    session_note_count = 0 # TODO: also total notes?

    # for all time - or as long as the app has run (TODO: persistence)
    total_session_count = 0
    total_practice_time = 0

    event_time = int(time.time())
    last_event_time = 0
    in_session = False

    display.update_display()

    while g_run and True:

        display_changed = False

        # print("Looking for MIDI events...")

        # process all events
        #
        notes_in_queue = 0 # just for fun and debugging
        queue_start = time.time()

        for msg in midi_port.iter_pending(): # non-blocking queue

            notes_in_queue += 1
            # print(f"{notes_in_queue}: {msg}")

            # OK, not *all* messages!
            if msg.type != 'note_on':
                # print(f"* ignoring: {msg}")
                continue

            session_note_count += 1
            disp.set_notes_label(f"Notes: {session_note_count}")
            display_changed = True

            event_time = int(time.time())

            # start a new session?
            if not in_session:

                in_session = True
                total_session_count += 1
                print(f"Starting session #{total_session_count}")

                disp.set_session_label(f"Session {total_session_count}")
                # disp.set_time_session_fg("white")
                display_changed = True

                session_note_count = 1
                session_start_time = event_time

            last_event_time = event_time
        
        # if notes_in_queue > 0:
        #     print(f"done processing MIDI queue of {notes_in_queue}")
        if notes_in_queue > 0:
            print(f"Processed {notes_in_queue} MIDI notes in {(time.time()-queue_start):0.2f}")


        if in_session:

            now_time = int(time.time())
            if now_time > last_event_time:

                current_session_time = now_time - session_start_time

                # FIXME: this is wrong. so wrong.
                # disp.show_elapsed_time(int(total_practice_time + current_session_time))

                disp.show_session_time(int(current_session_time))
                display_changed = True

                # end session?
                if now_time - SESSION_TIMEOUT_SEC > last_event_time:
                    in_session = False

                    # update total_practice_time; TODO: persist this
                    total_practice_time += current_session_time
                    disp.show_elapsed_time(total_practice_time)
                    disp.set_notes_label(f"Notes: {session_note_count}")

                    print(f"Ending session #{total_session_count}")

                    output_record(total_session_count, session_start_time, now_time, session_note_count)

                    last_event_time = now_time

                    # WTF was this?
                    # disp.set_time_session_fg("black")

        if display_changed:
            display.update_display()

        check_shutdown_button(shutdown_button, disp)
        check_other_button(other_button, disp)

        # print(f"Done. Sleeping {MIDI_EVENT_DELAY_S} seconds.")
        time.sleep(MIDI_EVENT_DELAY_S)

    # end main_loop


# return (port, name)
def get_midi_port_and_name():

    # Get the proper MIDI input port.
    # Use the first one other than the system "Through" port.
    #
    inputs = mido.get_input_names()
    # print(f" ports: {inputs}")

    port_name = None
    for pName in inputs:
        if pName.find("Through") == -1:
            port_name = pName
            break
    if port_name is None:
        print("Can't find non-Through port!")
        sys.exit(1)
    print(f"Using MIDI port {port_name}")
    midi_port = mido.open_input(port_name)
    return midi_port, port_name


if __name__ == "__main__":

    # set up signal handlers; kill and usr1 (for reloading MIDI list)
    signal.signal(signal.SIGINT,  handle_signal)
    signal.signal(signal.SIGUSR1, handle_signal)


    display = PracticeDisplay.PracticeDisplay()
    display.show_elapsed_time(0)
    display.show_session_time(0)
    display.set_session_label("Session: 0")
    display.set_notes_label("Notes: 0")
    # display.set_time_session_fg("black")

    try:
        


        # show the device connected to
        display.set_device_name(portName.split(":")[0])

    except Exception as e:
        print(e)
        sys.exit(1)

    # Mainly for keyboard interrupt, while running from console (in dev)
    try:
        main_loop(display, midi_port)
    except KeyboardInterrupt:
        print("Got KeyboardInterrupt !")
        display.set_backlight_on(False)
        print("\nDone!")
