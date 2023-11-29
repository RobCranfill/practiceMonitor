# test midi connect/re-connect

import mido
import signal
import sys
import time

global restart_flag
restart_flag = False

def handle_SIGUSR(sig, frame):
    global restart_flag
    print('setting restart_flag!')
    restart_flag = True

def get_midi_port(): # returns tuple of port and nice name

    # Get the proper MIDI input port.
    # Use the first one other than the system "Through" port.
    #
    inputs = mido.get_input_names()
    # print(f" ports: {inputs}")

    portName = None
    for pName in inputs:
        if pName.find("Through") == -1:
            portName = pName
            break
    if portName is None:
        print("Can't find non-Through port!")
        sys.exit(1)
    print(f"Using MIDI port {portName}")
    midi_port = mido.open_input(portName)
    simple_name = portName.split(":")[0]
    return midi_port, simple_name

if __name__ == "__main__":

    signal.signal(signal.SIGUSR1, handle_SIGUSR)

    try:

        port, name = get_midi_port()
        print(f"Connected to {name}")

        while True:

            if restart_flag:
                print("RESTART MIDI!")
                port, name = get_midi_port()
                print(f"Re-connected to {name}")
                restart_flag = False

            for msg in port.iter_pending(): # non-blocking queue
                print(msg)

            # print("sleeping...")
            # time.sleep(1)

    except Exception as e:
        print(e)
        sys.exit(1)
