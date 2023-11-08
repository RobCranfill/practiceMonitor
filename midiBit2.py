# first MIDI experiments, using MiDo

# std libs
import time

# un-std libs :-)
import mido


# # ultimately, present a GUI and ability to pick which device:
# print(f"{mido.get_input_names()}")

SESSION_TIMEOUT_SEC = 10

sessions_ = []

session_count = 0
session_note_count = 0

last_event_time = 0
overall_start_time = time.time()
event_time = time.time()
session_data = {}
inSession = False

print("{session_count}\t{session_note_count}\t{session_start_time}\t{session_send_time}")


with mido.open_input('MPKmini2:MPKmini2 MIDI 1 20:0') as inport:

    while True:

        # process all events
        # TODO: exclude non-keypress events?
        #
        for msg in inport.iter_pending():
            
            # print(msg)

            if msg.type != 'note_on':
                # print("  ^^ ignoring")
                continue

            session_note_count += 1
            # print(f" note #{session_note_count} of session {session_count} at {(event_time-overall_start_time):.0f}")

            event_time = time.time()
            if inSession:
                pass
            else:
                session_count += 1
                print(f"Starting session #{session_count}")
                session_note_count = 1
                session_start_time = event_time
                inSession = True
            last_event_time = event_time
        
        # print("done processing queue")

        if inSession:
            now_time = time.time()
            if now_time - SESSION_TIMEOUT_SEC > last_event_time:
                inSession = False
                print(f"Ending session #{session_count}")
                print(f"\n *** OUTPUT: {session_count}\t{session_note_count}\t{time.ctime(session_start_time)}\t{time.ctime(now_time)}")
                last_event_time = now_time

        # print("NOT waiting for next message....")
        time.sleep(0.1)
