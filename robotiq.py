# robotiq.py
"""
Python script for contorlling the Robotiq Gripper
Functions:
    caclulateCrc()          - Calculates 2 crc bits given a list of int's
    buildCommandString()    - Given the necessary information, builds the correct command
    init()                  - Initializes the serial object and makes it global, activates the gripper
    setPosition()           - Sets the position of the gripper with given speed nad force. Returns the gripper's response
    setSpeed()              - Sets the global speed variable
    setForce()              - Sets the global force variable
    checkStatus()           - Reads all Status registers and returns a hex string. Needs to pe parsed.
    closeSerial()           - Closes the Serial Port

Variables
    speed       - The speed of the gripper from 0 to 255
    force       - The Force of the gripper from 0 to 255
    position    - The Position of the gripper from 0 to 255

Constants
    deviceId                            - The slave ID of the gripper
    readHoldingRegister                 - The function code for reading registers
    presetSingleRegister                - The function code for writing to a single register
    presetMultipleRegister              - The function code for writing to multiple registers
    masterReadWriteMultipleRegisters    - The function code for reading and writing to/from registers simultaneously
"""
import serial
import time
import binascii
import sys

"""Variables for Moving the gripper"""
speed = 0;
force = 0;
position = 0;
"""Variables for building command strings"""
deviceId = "09"
readHoldingRegister = "03"
presetSingleRegister = "06"
presetMultipleRegister = "10"
masterReadWriteMultipleRegisters = "17"
firstReadRegister = "07D0"
firstWriteRegister = "03E8"

"""CRC algorithm for building Command Strings"""
def calculateCrc(message):
    n = len(message)
    crc = int("ffff", 16)
    polynomial = int("a001", 16)

    for i in range(0, n):
        # print("i: ", i)
        crc = crc ^ message[i]
        for j in range(1, 9):
            # print("j: ", j)
            if crc & 1:
                crc = crc >> 1
                # print(crc)+
                crc = crc ^ polynomial
            else:
                crc = crc >> 1

    # print(crc)
    lowByte = crc & int("ff", 16)
    highByte = (crc & int("ff00", 16)) >> 8

    # print(message)
    #print(lowByte, highByte)
    out1 = format(lowByte, 'x')
    out2 = format(highByte, 'x')
    if len(out1) < 2:
        out1 = "0" + out1
    if len(out2) < 2:
        out2 = "0" + out2
    return [out1, out2]


"""Builds a command string"""
def buildCommandString(slaveId, functionCode, readRegister="", numReadRegisters="", writeRegister="",
                       numWriteRegisters="", numBytes="", inputBytes=""):
    while numReadRegisters != "" and len(str(numReadRegisters)) < 4:
        numReadRegisters = "0" + numReadRegisters
    while numWriteRegisters != "" and len(str(numWriteRegisters)) < 4:
        numWriteRegisters = "0" + numWriteRegisters
    while numBytes != "" and (len(str(numBytes)) < 2):
        numBytes = "0" + numBytes
    while readRegister != "" and (len(str(readRegister)) < 2):
        readRegister = "0" + readRegister
    while writeRegister != "" and (len(str(writeRegister)) < 2):
        writeRegister = "0" + writeRegister
    while functionCode != "" and (len(str(functionCode)) < 2):
        functionCode = "0" + functionCode

    output = str(slaveId) + str(functionCode) + str(readRegister) + str(numReadRegisters) + str(writeRegister) + str(
        numWriteRegisters) + str(numBytes) + str(inputBytes)
    crcInput = []
    for i in range(0, len(output), 2):
        crcInput.append(int(output[i:i + 2], 16))
    #print crcInput
    crc = calculateCrc(crcInput)
    output = output + str(crc[0]) + str(crc[1])
    return output

"""Initializes serial communcations and activates the gripper."""
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
        #print(data_raw)
        data = binascii.hexlify(data_raw)
       # print ("Response 1 ", data)
        time.sleep(0.01)

        ser.write(binascii.unhexlify("090307D0000185CF"))
        data_raw = ser.readline()
        #print(data_raw)
        data = binascii.hexlify(data_raw)
        #print ("Response 2 ", data)
        time.sleep(1)
    return ser

"""Open's and closes the gripper."""
def demo():
    # ser = init()
    while (True):
        #print ("Close gripper")
        setPosition(255)

        #print ("Open gripper")
        setPosition(0)


"""Sets the position of the gripper. Note that speed and force will always be the previous used unless specified"""
def setPosition(nPos, nSpeed=None, nForce=None):
    global speed
    global force
    global position
    if nPos != None:
        if nPos < 0 or nPos > 255:
            return 'Error: Speed must be between 0 and 255'
        position = nPos
    if nSpeed != None:
        if nSpeed < 0 or nSpeed > 255:
            return 'Error: Speed must be between 0 and 255'
        speed = nSpeed
    if nForce != None:
        if nForce < 0 or nForce > 255:
            return 'Error: Speed must be between 0 and 255'
        force = nForce

    strpos = hex(position)[2:]
    strSpeed = hex(speed)[2:]
    strForce = hex(force)[2:]

    while len(strpos) < 2:
        strpos = "0" + strpos
    while len(strSpeed) < 2:
        strSpeed = "0" + strSpeed
    while len(strForce) < 2:
        strForce = "0" + strForce

    #print(strpos)
    # strpos = "FFFFFF"
    commandString = buildCommandString(deviceId, presetMultipleRegister, "03E8", "3", "6",
                                       "090000" + strpos + strSpeed + strForce)
    #print(commandString)
    ser.write(binascii.unhexlify(commandString))
    time.sleep(.001)

    data_raw = ser.readline()
    #print(data_raw)
    data = binascii.hexlify(data_raw)
    #print ("Response 4 ", data)
    #time.sleep(2)
    return data

"""Sets the Global speed variable."""
def setSpeed(nSpeed):
    global speed
    speed = nSpeed

"""Sets the Global force variable."""
def setForce(nForce):
    global force
    force = nForce


def checkStatus():
    command = buildCommandString(deviceId, readHoldingRegister, readRegister=firstReadRegister, numReadRegisters="3")
    ser.write(binascii.unhexlify(command))
    return binascii.hexlify(ser.readline())

    # print buildCommandString(deviceId, "10", "03E8", "3", "6", "090000FFFFFF")
    # print buildCommandString(deviceId, "3", "07D0", "2")
    # print buildCommandString(deviceId, "10", writeRegister = "03E9", numWriteRegisters = "2", numBytes = "4", inputBytes = "60E63CC8")
    # print calculateCrc([9, 16, 3, 232, 0, 3, 6, 9, 0, 0, 255, 255, 255])

def closeSerial():
    ser.close();

# init()
# if __name__ == '__main__':
#     p = Process(target = setPosition, args = (position, speed, force));
#     p.start()
#     p.join()

# time.sleep(2)
# position = 0
# time.sleep(2)
# position = 255