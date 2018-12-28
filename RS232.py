#!/usr/bin/python3

# Decoder for the Benchmultimeter MS8050


import threading
import serial


def index_start_marker(it, val, val2):
    gen = (i for i, x in enumerate(it) if x >= val and x <=val2)
    try:
        return next(gen)
    except StopIteration:
        raise ValueError('{!r} is not in iterable'.format(val)) from None

def ser_read(ser):
    bytesToRead = ser.inWaiting()
    return(ser.read(bytesToRead))


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=2400,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
i=0
BYTE=[]
while i<10:
    for val  in ser_read(ser):  # Reads all available Data of the Serial
        BYTE.append(val)

    if (len(BYTE)>=14): # DATA is 14 BYTES long, differs from the Protocol description
        if (BYTE[0]>>4 == 10): # Checks for startmarker 0b1010xxxx
            print (BYTE)
        ## BYTE 0   # Start Marker and Range Information
            SPAN = BYTE[0]& 0b00001111   # deletes the start marker -> measuringrange
            print ('Measuring Range =',SPAN)
        ## BYTE 1   # HOLD, ORDER and Funtion Information
            HOLD =      BYTE[1]>>6 & 0b00000001 # Hold marker is B6
            ORDER =     BYTE[1]>>5 & 0b00000001 # Order marker is B5    (no idea what this bit serves)
            FUNKTION=   BYTE[1]    & 0b00011111 # set Funktion is range from B0 to B4
            print ('HOLD =',HOLD)
            print ('ORDER =',ORDER)
            print ('FUNKTION =',FUNKTION)
        ## BYTE 2   # NEGATIVE, HAND/AUTO, PRESS, RELATVE/ABSLOUTE, MAX/MIN Information
            NEGATIVE =  BYTE[2]>>5  & 0b00000001 # NEGATIVE marker is B5
            HAND =      BYTE[2]>>4  & 0b00000001 # HAND/AUTO marker is B4
            PRESS =     BYTE[2]>>3  & 0b00000001 # PRESS marker is B3   (no idea what this bit serves)
            RELATVE =   BYTE[2]>>2  & 0b00000001 # RELATVE/ABSLOUTE marker is B2
            MAXMIN =    BYTE[2]     & 0b00000011 # MAX/MIN is range from B0 to B1
            print ('NEGATIVE=',NEGATIVE)
            print ('HAND=',HAND)
            print ('PRESS=',PRESS)
            print ('RELATVE=',RELATVE)
            print ('MAXMIN=',MAXMIN)
        ## BYTE 4-8 # Measured value
            VALUE=''
            for i in BYTE[3:8]:
                VALUE +=""+ str(i)
            print ('VALUE =',VALUE)
            del BYTE[:14]  # Clears the Dataset of the Array
            i+=1
        else:              # Clears corrupted Data of the Array
            del BYTE[:index_start_marker(BYTE,160,166)]
            print ('Corrupted Data cleared')
