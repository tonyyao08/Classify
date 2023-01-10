# run this
# sudo apt-get update && sudo apt-get install python3-gpiozero python-gpiozero
import RPi.GPIO as GPIO
from gpiozero import Button
from picamera import PiCamera
from time import sleep

button = Button(2)
camera = PiCamera()
run = True
while run:
    button.wait_for_press()
    camera.start_preview()
    sleep(5)
    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()
