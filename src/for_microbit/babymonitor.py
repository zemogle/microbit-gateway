from microbit import *
import radio

radio.config(group=0)
radio.on()

display.show("-")

while True:

    try:
        msg = radio.receive()
        if msg is not None:
            if len(msg) > 0:
                if msg == 'W':
                    display.show(Image.MEH)
                elif msg == 'Q':
                    display.show(Image.ASLEEP)
                elif msg == 'C':
                    display.show(Image.ANGRY)
                else:
                    display.show(Image.SKULL)
    except:
        display.show("X")
        radio.off()
        sleep(250)
        radio.on()
        display.show("-")
