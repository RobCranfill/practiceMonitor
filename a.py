# MIDI hacking part 1

import board
import simpleio
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

#  midi channel setup
midi_in_channel = 1
midi_out_channel = 1

#  USB midi setup
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0
)

# # gate output pin
# gate = DigitalInOut(board.A1)
# gate.direction = Direction.OUTPUT

# #  i2c setup
# i2c = board.I2C()  # uses board.SCL and board.SDA
# # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
# #  dac setup over i2c
# dac = adafruit_mcp4725.MCP4725(i2c)


while True:

    #  read incoming midi messages
    msg = midi.receive()

    #  if a midi msg comes in...
    if msg is not None:

        #  if it's noteon...
        if isinstance(msg, NoteOn):
            print(f"Note ON {msg}")

        #  if it's noteoff...
        elif isinstance(msg, NoteOff):
            print(f"Note OFF {msg}")
