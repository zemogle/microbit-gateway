from microbit import *
import radio

radio.config(group=0)
radio.on()

display.show("-")

pin_val = False
while True:

    if pin0.is_touched():
        display.show(Image.HAPPY)
        radio.send("H")
    else:
        display.clear()
    sleep(50)

    try:
        msg = radio.receive()
        if msg is not None:
            if len(msg) > 0:
                display.show(msg)
    except:
        display.show("X")
        radio.off()
        sleep(250)
        radio.on()
        display.show("-")
