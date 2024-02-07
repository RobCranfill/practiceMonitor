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
import RPi.GPIO as GPIO


# pseudo-constants
OUTPUT_JSON = True
JSON_KEY_TS     = "SeshNumber"
JSON_KEY_START  = "SeshStart"
JSON_KEY_END    = "SeshEnd"
JSON_KEY_NOTES  = "SeshNotes"

SESSION_TIMEOUT_SEC =  10

MIDI_EVENT_DELAY_S = 0.01
MENU_EVENT_DELAY_S = 1

BUTTON_A_pin = 24
BUTTON_B_pin = 23


# global flag to keep running or die; for SIGTERM
g_run = True

# set in response to SIGUSR1
g_rescan_midi = False

# global display/function mode
g_menu_mode = False

# button handler needs to use globals :-/
g_display = None 


# Handle either keyboard interrupt (ctrl-C), in which case we die gracefully;
# or SIGUSR1, which causes us to re-scan the MIDI bus
#
def handle_signal(signum, frame):
    global g_run
    global g_rescan_midi

    if signum == signal.SIGINT:
        print("Caught SIGINT. Stopping.")
        g_run = False
    elif signum == signal.SIGUSR1:
        print("Caught SIGUSR1. Rescanning...")
        g_rescan_midi = True
    else:
        print(f"Caught some other signal: {signum}")


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


def set_up_buttons():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    normal_mode_buttons()


# top button = enter menu mode; bottom button = nothing (for now)
def normal_mode_buttons():

    GPIO.remove_event_detect(BUTTON_A_pin)
    GPIO.remove_event_detect(BUTTON_B_pin)

    GPIO.add_event_detect(BUTTON_A_pin, GPIO.FALLING, callback=begin_menu_mode, bouncetime=300)
    # GPIO.add_event_detect(BUTTON_B_pin, GPIO.FALLING, callback=button_handler_lower, bouncetime=300)


# top button = "do it", bottom button = move cursor down
def begin_menu_mode(event_channel):
    global g_display
    global g_menu_mode
    global g_menu_data

    print("begin_menu_mode!")

    GPIO.remove_event_detect(event_channel)
    GPIO.add_event_detect(BUTTON_A_pin, GPIO.FALLING, callback=menu_mode_button_upper, bouncetime=300)
    GPIO.add_event_detect(BUTTON_B_pin, GPIO.FALLING, callback=menu_mode_button_lower, bouncetime=300)

    g_menu_data = (
            {"text": "Resume",  "action": exit_menu_mode}, 
            {"text": "Two",     "action": handle_action_2}, 
            {"text": "Three",   "action": handle_action_3}
            )
    g_display.start_menu_mode(g_menu_data)

    print("Exiting begin_menu_mode")
    g_menu_mode = True


def exit_menu_mode(channel):
    global g_menu_mode
    print(f"exit_menu_mode({channel})")
    normal_mode_buttons()
    g_menu_mode = False

def handle_action_2(channel):
    print(f"handle_action_2({channel})")

def handle_action_3(channel):
    print(f"handle_action_3({channel})")


# Execute selected action
def menu_mode_button_upper(channel):
    global g_display
    global g_menu_data

    # TODO: make this a method?
    selected_item = g_menu_data[g_display.menu_item_selected]
    print(f"handle_button_upper! execute {selected_item}")
    f = selected_item["action"]
    f(channel)

# Move down the menu
def menu_mode_button_lower(unused_channel):
    global g_display
    print("handle_button_lower!")
    g_display.select_next_item()


def main_loop(display, midi_port):

    # when this goes False, we stop processing events
    global g_run

    # if MIDI changes, we will find out this way via signal handler
    global g_rescan_midi

    # If we are handling the menu, ignore MIDI events?
    global g_menu_mode


    set_up_buttons()


    # for current session
    session_start_time = None
    session_note_count = 0 # TODO: also total notes?

    # for all time - or as long as the app has run (TODO: persistence)
    total_session_count = 0
    total_practice_time = 0

    event_time = int(time.time())
    last_event_time = 0
    in_session = False

    # old_run_mode_menu = g_run_mode_menu

    # Paint first time
    display.update_display()

    while g_run:

        if g_menu_mode:

            # TODO: if in a session?

            print(f"Sleeping {MENU_EVENT_DELAY_S} sec in menu mode. Needed?")
            time.sleep(MENU_EVENT_DELAY_S)
            continue

        if g_rescan_midi:
            midi_port, port_name = get_midi_port_and_name()
            display.set_device_name(port_name)
            g_rescan_midi = False

        # if old_run_mode_menu != g_run_mode_menu:
        #     print(f"Changing g_run_mode_menu: {g_run_mode_menu}")
        #     display.set_menu_mode(g_run_mode_menu)
        #     old_run_mode_menu = g_run_mode_menu

        #     # TODO: DO WE IGNORE ALL MIDI MESSAGES WHEN IN MENU MODE? FOR NOW, YES

        #     continue

        # FIXME: Is this extra???
        # display.update_display()

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
            display.set_notes_label(f"Notes: {session_note_count}")
            display_changed = True

            event_time = int(time.time())

            # start a new session?
            if not in_session:

                in_session = True
                total_session_count += 1
                print(f"Starting session #{total_session_count}")

                display.set_session_label(f"Session {total_session_count}")
                # disp.set_time_session_fg("white")
                display_changed = True

                session_note_count = 1
                session_start_time = event_time

            last_event_time = event_time
        
        # if notes_in_queue > 0:
        #     print(f"Processed {notes_in_queue} MIDI notes in {(time.time()-queue_start):0.2f}")


        if in_session:

            now_time = int(time.time())
            if now_time > last_event_time:

                current_session_time = now_time - session_start_time

                # FIXME: this is wrong. so wrong.
                # disp.show_elapsed_time(int(total_practice_time + current_session_time))

                display.show_session_time(int(current_session_time))
                display_changed = True

                # end session?
                if now_time - SESSION_TIMEOUT_SEC > last_event_time:
                    in_session = False

                    # update total_practice_time; TODO: persist this
                    total_practice_time += current_session_time
                    display.show_elapsed_time(total_practice_time)
                    display.set_notes_label(f"Notes: {session_note_count}")

                    print(f"Ending session #{total_session_count}")

                    output_record(total_session_count, session_start_time, now_time, session_note_count)

                    last_event_time = now_time

                    # WTF was this?
                    # display.set_time_session_fg("black")

        if display_changed:
            display.update_display()

        # print(f"Done. Sleeping {MIDI_EVENT_DELAY_S} seconds.")
        time.sleep(MIDI_EVENT_DELAY_S)

        #### end while g_run

    # end main_loop


def set_up_iot(key):

    # show first and last 4 chars
    kl = len(key)
    key_masked = key[:4] + "*"*(kl-8) + key[kl-4:]
    print(f"AIO key: {key_masked}")    


# return (port, name)
def get_midi_port_and_name():

    print("Rescanning MIDI....")

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
        print("*********************************")
        print("Can't find non-through MIDI port!")
        print("*********************************")
        # TODO: er, return something so we can exit nice up top
        # TODO: or throw an exception?
        return None

    print(f"Using MIDI port {port_name}")
    midi_port = mido.open_input(port_name)
    short_name = port_name.split(":")[0]
    return midi_port, short_name


def set_up_display():

    disp = PracticeDisplay.PracticeDisplay()
    disp.show_elapsed_time(0)
    disp.show_session_time(0)
    disp.set_session_label("Session: 0")
    disp.set_notes_label("Notes: 0")
    # disp.set_time_session_fg("black")
    return disp


def main(args):
    global g_display

    print(f" GPIO.VERSION {GPIO.VERSION}")

    if len(args) > 1:
        set_up_iot(args[1])

    # set up signal handlers; kill and usr1 (for reloading MIDI device list)
    signal.signal(signal.SIGINT,  handle_signal)
    signal.signal(signal.SIGUSR1, handle_signal)

    display = set_up_display()
    g_display = display


    try:
        midi_ports = get_midi_port_and_name()
        if midi_ports is not None:
            midi_port, port_name = midi_ports
            display.set_device_name(port_name)

            # Main event-handling loop.
            #
            main_loop(display, midi_port)

    except Exception as e:
        print(f"Got exception {e}")

    finally:

        print("PM exiting; cleaning up...")
        # FIXME: Destroying display object is supposed to suffice.
        # display.set_backlight_on(False) # this doesn't work either!?!?
        display = None
        g_display = None


        # # FIXME: This is the polite thing to do, but doesn't work? throws exception also
        # # Perhaps the LCD object should take care of all this in its deinit code?
        # try:
        #     GPIO.cleanup()
        # except:
        #     pass

        print("Done!")

if __name__ == "__main__":
    main(sys.argv)
