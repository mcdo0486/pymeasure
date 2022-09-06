'''
IMPORTS
'''
import board
import usb_cdc
import digitalio
from time import monotonic_ns, sleep
'''
CONSTANTS
'''
DELAY = 0.01
PAUSE = 3
DEBUG = False
DISPLAY_COUNT = 2

'''
FUNCTIONS
'''
def log(msg):
    if DEBUG: print(msg)

def process_command(cmd, serial, pins):
    #log(cmd)
    cmd = cmd.split('.')
    mask = []
    out_str = ""
    if cmd[0] == "DEV" and len(cmd) == 3:
        if cmd[1] == '1':
            if cmd[2] == '0':
                mask = [False, False, False, False, False]
            elif cmd[2] == '1':
                mask = [False, False, False, True, False]
        elif cmd[1] == '2':
            if cmd[2] == '0':
                mask = [False, True, False, False, False]
            elif cmd[2] == '1':
                mask = [False, True, False, True, False]
        elif cmd[1] == '3':
            if cmd[2] == '0':
                mask = [True, False, False, False, False]
            elif cmd[2] == '1':
                mask = [True, False, False, False, True]
        elif cmd[1] == '4':
            if cmd[2] == '0':
                mask = [True, False, True, False, False]
            elif cmd[2] == '1':
                mask = [True, False, True, False, True]

        if len(mask):
            for idx, i in enumerate(mask):
                out_str += str(i)+", "
                pins[idx].value = i
                #sleep(.1)
            #serial.write((out_str + "\n").encode('utf-8'))
    #elif cmd[0] == 'DEV?':
    #    serial.write((out_str + "\n").encode('utf-8'))
    else:
        serial.write(b"BAD INPUT")


# DEV.1.0
# DEV.1.1

'''
RUNTIME START
'''
def loop():
    # Get the USB data feed object
    serial = usb_cdc.data

    g0 = digitalio.DigitalInOut(board.GP0)
    g0.direction = digitalio.Direction.OUTPUT
    g0.value = False
    g1 = digitalio.DigitalInOut(board.GP1)
    g1.direction = digitalio.Direction.OUTPUT
    g1.value = False

    # g2 & g3 are wired opposite
    g2 = digitalio.DigitalInOut(board.GP3)
    g2.direction = digitalio.Direction.OUTPUT
    g2.value = False
    # g2 & g3 are wired opposite
    g3 = digitalio.DigitalInOut(board.GP2)
    g3.direction = digitalio.Direction.OUTPUT
    g3.value = False

    g4 = digitalio.DigitalInOut(board.GP4)
    g4.direction = digitalio.Direction.OUTPUT
    g4.value = False

    pins = (g0,g1,g2,g3,g4)

    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    # Run-loop management Flags, etc.
    boot_released = False
    boot_pressed = False
    debounce_timer = 0
    last_display_update = 0
    in_data = bytearray()
    out_data = b'WAITING+++'
    out_index = 0
    # Run loop
    while True:
        # Get the nanosecond counter value
        now = monotonic_ns()       

        if now - last_display_update > 400000000:
            last_display_update = now

        # Check for incoming data
        if serial.in_waiting > 0:
            byte = serial.read(1)
            if byte == b'\n':
                #log(in_data.decode("utf-8"))
                process_command(in_data.decode("utf-8"), serial, pins)
                out_data = in_data
                out_data += b'  '
                in_data = bytearray()
                out_index = 0
            else:
                in_data += byte
                if len(in_data) == 129:
                    in_data = in_data[128] + in_data[1:127]

        led.value = not led.value
        sleep(.1)
        
loop()