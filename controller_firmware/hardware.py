# AI&P Final project [Create M6 2022-2023]
# controller_firmware/hardware.py
#
# Copyright 2022-2023 Jakub Stachurski
# Copyright 2022-2023 Natalia Bueno Donadeu
#
# Imports
from machine import Pin, I2C, ADC, PWM
from time import sleep_ms
from data import ControllerData
from micropython import const
from mpu6500 import MPU6500

class Hardware:
    PIN_SW1 = const(18)
    PIN_SW2 = const(19) 
    PIN_JX  = const(35)
    PIN_JY  = const(34)
    PIN_JA  = const(12) 
    PIN_SCL = const(22) 
    PIN_SDA = const(21)
    PIN_BZ  = const(23)
    
    HW_SW1 = None
    HW_SW2 = None
    HW_JX = None 
    HW_JY = None 
    HW_JA = None
    HW_BZ = None
    
    HW_I2C = None
    HW_MPU6500 = None 
    
    @classmethod 
    def init(cls):
        cls.HW_SW1 = Pin(cls.PIN_SW1, Pin.IN)
        cls.HW_SW2 = Pin(cls.PIN_SW2, Pin.IN)
        cls.HW_JA =  Pin(cls.PIN_JA, Pin.OUT)
        
        cls.HW_I2C = I2C(0, scl=Pin(PIN_SCL), sda=Pin(PIN_SDA))
        cls.HW_MPU6500 = MPU6500(cls.HW_I2C)
        
        cls.HW_BZ = PWM(Pin(cls.PIN_BZ), freq=440, duty=0)
        
        cls.HW_JX = ADC(Pin(cls.PIN_JX), atten=ADC.ATTN_11DB)
        cls.HW_JY = ADC(Pin(cls.PIN_JY), atten=ADC.ATTN_11DB)
        
    @classmethod
    def writeData(cls, data: ControllerData):
        data.sw1 = cls.HW_SW1.value()
        data.sw2 = cls.HW_SW2.value()
        
        cls.HW_JA.value(1)
        sleep_ms(5)
        
        data.x = cls.HW_JX.read() / 4095.0
        data.y = cls.HW_JY.read() / 4095.0
        
        cls.HW_JA.value(0)
        
        data.ax, data.ay, data.az = cls.HW_MPU6500.acceleration
        data.gx, data.gy, data.gz = cls.HW_MPU6500.gyro
    
    @classmethod
    def setBuzzer(cls, freq, duty):
        cls.HW_BZ.freq(freq)
        cls.HW_BZ.duty(duty)
        
        
        
        
        
        
        
        
        
