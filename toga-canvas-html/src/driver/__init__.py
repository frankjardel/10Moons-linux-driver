# Proper test driver for the 10moons graphics tablet

import os

# Specification of the device https://python-evdev.readthedocs.io/en/latest/
# from evdev import UInput, ecodes, AbsInfo
import evdev
# Establish usb communication with device
import usb.core
import keyboard


def start():
    config = {'xinput_name': '10moons-pen', 'vendor_id': 2290, 'product_id': 26641,
     'pen': {'max_x': 4096, 'max_y': 4096, 'max_pressure': 2047, 'resolution_x': 20, 'resolution_y': 30},
     'actions': {'pen': 'BTN_TOOL_PEN', 'sylus': 'BTN_STYLUS', 'pen_touch': 'BTN_TOUCH',
                 'tablet_buttons': ['KEY_LEFTCTRL+KEY_Z', 'KEY_LEFTCTRL+KEY_A', 'KEY_C', 'KEY_D']}}


    # Get the required ecodes from configuration
    required_ecodes = []
    for k, v in config["actions"].items():
        if isinstance(v, list):
            required_ecodes.extend(v)
        else:
            required_ecodes.append(v)

    temp = []
    for c in required_ecodes:
        temp.extend([evdev.ecodes.ecodes[x] for x in c.split("+")])
    required_ecodes = temp

    pen_events = {
        evdev.ecodes.EV_KEY: required_ecodes,
        evdev.ecodes.EV_ABS: [
            #AbsInfo input: value, min, max, fuzz, flat
            (evdev.ecodes.ABS_X, evdev.AbsInfo(0, 0, config['pen']['max_x'], 0, 0, config["pen"]["resolution_x"])),
            (evdev.ecodes.ABS_Y, evdev.AbsInfo(0, 0, config['pen']['max_y'], 0, 0, config["pen"]["resolution_y"])),
            (evdev.ecodes.ABS_PRESSURE, evdev.AbsInfo(0, 0, config['pen']['max_pressure'], 0, 0, 0))
        ],
    }

    # Find the device
    dev = usb.core.find(idVendor=config["vendor_id"], idProduct=config["product_id"])
    # Select end point for reading second interface [2] for actual data
    # I don't know what [0] and [1] are used for
    ep = dev[0].interfaces()[2].endpoints()[0]
    # Reset the device (don't know why, but till it works don't touch it)
    dev.reset()

    # Drop default kernel driver from all devices
    for j in [0, 1, 2]:
        if dev.is_kernel_driver_active(j):
            dev.detach_kernel_driver(j)

    # Set new configuration
    dev.set_configuration()

    vpen = evdev.UInput(events=pen_events, name=config["xinput_name"], version=0x3)

    pressed = -1

    # Infinite loop
    while True:
        try:
            data = dev.read(ep.bEndpointAddress, ep.wMaxPacketSize)
            if data[1] in [192, 193]: # Pen actions
                pen_x = config['pen']['max_x'] - (data[5] * 255 + data[4])
                pen_y = data[3] * 255 + data[2]
                pen_pressure = data[7] * 255 + data[6]
                vpen.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_X, pen_x)
                vpen.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_Y, pen_y)
                vpen.write(evdev.ecodes.EV_ABS, evdev.ecodes.ABS_PRESSURE, pen_pressure)
                if data[1] == 192: # Pen touch
                    vpen.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_TOUCH, 0)
                else:
                    vpen.write(evdev.ecodes.EV_KEY, evdev.ecodes.BTN_TOUCH, 1)
            elif data[0] == 2: # Tablet button actions
                # press types: 0 - up; 1 - down; 2 - hold
                press_type = 1
                if data[1] == 2: # First button
                    pressed = 0
                elif data[1] == 4: # Second button
                    pressed = 1
                elif data[3] == 44: # Third button
                    pressed = 2
                elif data[3] == 43: # Fourth button
                    pressed = 3
                else:
                    press_type = 0

                key_codes = config["actions"]["tablet_buttons"][pressed].split("+")

                for key in key_codes:
                    act = evdev.ecodes.ecodes[key]

                    if pressed == 0:
                        keyboard.press('ctrl+shift+l')

                    if pressed == 1:
                        keyboard.press('ctrl+shift+p')

                    if pressed == 2:
                        keyboard.press_and_release('ctrl+z')

                    if pressed == 3:
                        keyboard.press_and_release('ctrl+shift+z')

                    if press_type == 0:
                        keyboard.release('ctrl+shift+l')
                        keyboard.release('ctrl+shift+p')

                    vpen.write(evdev.ecodes.EV_KEY, act, press_type)
            # Flush
            vpen.syn()
        except usb.core.USBError as e:
            if e.args[0] == 19:
                vpen.close()
                raise Exception('Device has been disconnected')
