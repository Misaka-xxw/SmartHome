import time, network, urequests, ujson
import ssd1306
from machine import Pin, PWM, SoftI2C, RTC, Timer
from random import randint, random
from Wifi import Wifi
wifi=Wifi()
wifi.wifi_connect()
