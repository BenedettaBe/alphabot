import RPi.GPIO as GPIO
from AlphaBot import AlphaBot

DR = 16
DL = 19

GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

while True:
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
    if((DL_status == 1) and (DR_status == 1)):
        print("entrambi accesi")
    elif((DL_status == 1) and (DR_status == 0)):
        print("sinistro acceso")
    elif((DL_status == 0) and (DR_status == 1)):
        print("destro acceso")
    else:
        print("entrambi spenti")