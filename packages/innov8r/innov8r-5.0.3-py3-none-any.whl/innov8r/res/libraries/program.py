from machine import Pin
import time
led2 = Pin(2, Pin.OUT)
while True:
    led2.value(0)
    time.sleep(1)
    led2.value(1)
    time.sleep(1)
