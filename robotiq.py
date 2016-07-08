# robotiq.py
import serial
import time
import binascii
import sys

speed = 0;
force = 0;
position = 0;
ser = 0
"""Variables for building command strings"""
deviceId = "09"
readHoldingRegister = "03"
presetSingleRegister = "06"
presetMultipleRegister = "10"
masterReadWriteMultipleRegisters = "17"

"""This CRC algoritm generates the last 2 bytes of the command string
    input is an int array holding all the parameters of the message
    output is """
def calculateCrc(message):
    n = len(message)
    crc = int("ffff", 16)
    polynomial = int("a001", 16)

    for i in range(0, n):
        #print("i: ", i)
        crc = crc ^ message[i]
        for j in range(1, 9):
            #print("j: ", j)
            if crc & 1:
                crc = crc >> 1
                #print(crc)+
                crc = crc ^ polynomial
            else:
                crc = crc >> 1

    #print(crc)
    lowByte = crc & int("ff", 16)
    highByte = (crc & int("ff00", 16)) >> 8

    #print(message)
    print(lowByte, highByte)
    out1 = format(lowByte, 'x')
    out2 = format(highByte, 'x')
    if len(out1) < 2:
        out1 = "0" + out1
    if len(out2) < 2:
        out2 = "0" + out2
    return [out1, out2]


"""Builds a command string. Doesn't work for all function codes at the moment
    Should work for PresetMultipleRegisters"""
def buildCommandString(slaveId, functionCode, register, numRegisters, numBytes, bytes):
    while len(numRegisters) < 4:
        numRegisters = "0" + numRegisters
    while(len(numBytes) < 2):
        numBytes = "0" + numBytes
    output = slaveId + functionCode + register + numRegisters + numBytes + bytes
    crcInput = []
    for i in range(0, len(output), 2):
        crcInput.append(int(output[i:i+2], 16))
    print crcInput
    crc = calculateCrc(crcInput)
    output = output + str(crc[0]) + str(crc[1])
    return output

def init():
    # type: () -> object
    reload(sys)
    sys.setdefaultencoding('utf-8')
    global ser
    ser = serial.Serial(port='COM9', baudrate=115200, timeout=1,
                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
    counter = 0
    while counter < 1:
        counter = counter + 1
        ser.write(binascii.unhexlify("091003E80003060000000000007330"))
        data_raw = ser.readline()
        print(data_raw)
        data = binascii.hexlify(data_raw)
        print ("Response 1 ", data)
        time.sleep(0.01)

        ser.write(binascii.unhexlify("090307D0000185CF"))
        data_raw = ser.readline()
        print(data_raw)
        data = binascii.hexlify(data_raw)
        print ("Response 2 ", data)
        time.sleep(1)
    return ser

def demo():
    #ser = init()
    while (True):
        print ("Close gripper")
        ser.write(binascii.unhexlify("091003E8000306090000FFFFFF4229"))
        data_raw = ser.readline()
        print(data_raw)
        data = binascii.hexlify(data_raw)
        print ("Response 3 ", data)
        time.sleep(2)

        print ("Open gripper")
        ser.write(binascii.unhexlify("091003E800030609000000FFFF7219"))
        data_raw = ser.readline()
        print(data_raw)
        data = binascii.hexlify(data_raw)
        print ("Response 4 ", data)
        time.sleep(2)

def setPosition(pos):
    if(pos < 0 or pos > 255):
        return 'Error: Position must be between 0 and 255'
    strpos = hex(pos)[2:]
    while(len(strpos) < 2):
        strpos = "0" + strpos

    print(strpos)
    #strpos = "FFFFFF"
    commandString = buildCommandString(deviceId, presetMultipleRegister, "03E8", "3", "6", "090000" + strpos + "FFFF")
    print(commandString)
    ser.write(binascii.unhexlify(commandString))
    data_raw = ser.readline()
    print(data_raw)
    data = binascii.hexlify(data_raw)
    print ("Response 4 ", data)
    time.sleep(2)

init()
#setPosition(0)
#setPosition(50)
setPosition(255)
setPosition(120)
setPosition(255)
setPosition(120)
#setPosition(255)
#print buildCommandString(deviceId, "10", "03E8", "3", "6", "090000FFFFFF")
#print calculateCrc([9, 16, 3, 232, 0, 3, 6, 9, 0, 0, 255, 255, 255])