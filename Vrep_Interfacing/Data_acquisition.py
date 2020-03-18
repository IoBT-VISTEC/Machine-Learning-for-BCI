import pygds 
import numpy as np
import ssvep_cca as fr
import vrep
import socket
import struct
import time
import matplotlib.pyplot as plt
import scipy.fftpack
from pygds import Scope
import threading

import numpy as np
import scipy
from scipy.signal import butter, lfilter
from scipy.fftpack import fft, fftfreq
from random import randint
import scipy.signal
from scipy import signal
import pandas as pd
import time
from math import sqrt
import xarray as xr
from pprint import pprint
from functools import reduce
from matplotlib import pyplot as plt
from IPython.display import display, Markdown
import math
import pylab
import operator
import matplotlib.pyplot as plt

try:
    import vrep
except:
    print ('--------------------------------------------------------------')
    print ('"vrep.py" could not be imported. This means very probably that')
    print ('either "vrep.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "vrep.py"')
    print ('--------------------------------------------------------------')
    print ('')
    
####################################################
#               Function Declaration               #
####################################################

# Get Robot & Gripper handle
def InitializeRemoteAPI(clientId):
    if clientId!=-1:
        print ('Connected to remote API server')
        res, robotTargetHandle = vrep.simxGetObjectHandle(clientId, 'UR5_target', vrep.simx_opmode_oneshot_wait)
        res, robotGripperHandle = vrep.simxGetObjectHandle(clientId, 'RG2_openCloseJoint', vrep.simx_opmode_oneshot_wait)

        return robotTargetHandle, robotGripperHandle
    else:
        print ('Failed connecting to remote API server')

# Moving the target position by vectorXYZ
def robotMove(clientId, robotTargetHandle, vectorXYZ, stepSize):     
        res, currentTargetPos = vrep.simxGetObjectPosition(clientId, robotTargetHandle, -1, vrep.simx_opmode_oneshot_wait)

        finalPosX = currentTargetPos[0] + vectorXYZ[0]
        finalPosY = currentTargetPos[1] + vectorXYZ[1]
        finalPosZ = currentTargetPos[2] + vectorXYZ[2]

        # Limit the boundary of Y & Z axis of the UR5 robot
        # by checking the desired position
        if finalPosY > -0.425 and finalPosY < 0.425:
            movingPermissionY = 1
        else:
            movingPermissionY = 0

        if finalPosZ > 0.3 and finalPosZ < 0.9:
            movingPermissionZ = 1
        else:
            movingPermissionZ = 0

        # Moving robot to the desired position in every point of the path
        for i in range(0, stepSize):
            xPos = currentTargetPos[0] + (vectorXYZ[0]*(i+1)/stepSize)
            yPos = currentTargetPos[1] + ((vectorXYZ[1]*(i+1)/stepSize) * movingPermissionY)
            zPos = currentTargetPos[2] + ((vectorXYZ[2]*(i+1)/stepSize) * movingPermissionZ)
            vrep.simxSetObjectPosition(clientId, robotTargetHandle, -1, [xPos, yPos, zPos], vrep.simx_opmode_oneshot_wait)    

# Command the robot to Grip (if condition = 1) & Release (if condition = 0)
def robotGripRelease(clientId, robotTargetHandle, gripperHandle, condition):
    # Gripping
    if condition == 1:
        robotMove(clientId, robotTargetHandle, [-0.2, 0, 0], 50)
        time.sleep(2)
        vrep.simxSetJointTargetVelocity(clientId, gripperHandle, -0.05, vrep.simx_opmode_oneshot_wait)
        time.sleep(2)
        robotMove(clientId, robotTargetHandle, [0.2, 0, 0], 50)
        time.sleep(2)

    # Releasing  
    else:
        robotMove(clientId, robotTargetHandle, [-0.2, 0, 0], 50)
        time.sleep(2)
        vrep.simxSetJointTargetVelocity(clientId, gripperHandle, 0.05, vrep.simx_opmode_oneshot_wait)
        time.sleep(2)
        robotMove(clientId, robotTargetHandle, [0.2, 0, 0], 50)
        time.sleep(2)
        
def TerminateRemoteAPI(clientId):
    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientId)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientId)

    print ('Program ended')

def RobotThread(answer):
    answer = str(answer)
    if answer == '5.45':
        #print ('LEFT')
        robotMove(clientID, robotTargetHandle, [0, -0.05, 0], 50)
    elif answer == '6.67':
        #print ('RIGHT')
        robotMove(clientID, robotTargetHandle, [0, 0.05, 0], 50)
    elif answer == '7.5':
        #print ('UP')
        robotMove(clientID, robotTargetHandle, [0, 0, 0.05], 50)
    elif answer == '8.57':
        #print ('DOWN')
        robotMove(clientID, robotTargetHandle, [0, 0, -0.05], 50)
    else:
        print ('do nothing')

    '''elif str(fbcca_result) == '6':
        #print ('gripping')
        robotGripRelease(clientID, robotTargetHandle, robotGripperHandle, 1)
    elif str(fbcca_result) == '7.5':
        #print ('releasing')
        robotGripRelease(clientID, robotTargetHandle, robotGripperHandle, 0)         
    elif str(fbcca_result) == '6.67':
        print ('stop')'''

####################################################
#             TCP server initialization            #
####################################################
'''HOST = '127.0.0.1'
PORT = 8055

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
conn, addr = server.accept()
if conn:
    print ('Connected by', addr)
else:
    print ('No connection')
    
conn.send(bytes(str(fbcca_result), encoding='utf-8'))'''

####################################################
#               Vrep initialization               #
####################################################

print ("Program started")
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',20001,True,True,5000,5) # Connect to V-REP

robotTargetHandle, robotGripperHandle = InitializeRemoteAPI(clientID)

# Set initial position of the robot 
vrep.simxSetObjectPosition(clientID, robotTargetHandle, robotTargetHandle, [0, 0, 0.05], vrep.simx_opmode_oneshot_wait)
time.sleep(1)
vrep.simxSetObjectPosition(clientID, robotTargetHandle, robotTargetHandle, [0, 0.2, 0], vrep.simx_opmode_oneshot_wait)
time.sleep(1)

####################################################
#                EEG Configuration                 #
####################################################

# choose EEG channels from 0 - 15 channels 
eeg_channels = [0, 1, 2]

d = pygds.GDS()
pygds.configure_demo(d, testsignal=False, acquire=1)

# Enable only the chosen EEG channels
BP = [x for x in d.GetBandpassFilters()[0] if x['SamplingRate'] == d.SamplingRate] 
N = [x for x in d.GetNotchFilters()[0] if x['SamplingRate'] == d.SamplingRate] 
for i, ch in enumerate(d.Channels):
    if i not in eeg_channels:
        ch.Acquire = 0         
    if N:         
        ch.NotchFilterIndex = N[0]['NotchFilterIndex']
    if BP:
        ch.BandpassFilterIndex = BP[19]['BandpassFilterIndex'] 

for c in d.Configs:
    c.CommonGround = [1]*4
    c.CommonReference = [1]*4

d.SetConfiguration()

####################################################
#                  Main section                    #
####################################################

# CCA constant
PI = np.pi
sampling_frequency = 256
candidate_frequency = [5.45, 6.67, 7.5, 8.57, 9, 9.5, 10, 10.5, 11.5, 12]
reference_signal_phase = 0

ref_signal = {}
for frequency in candidate_frequency:
    signal = fr.generate_reference_signal(
            frequency=frequency,
            sampling_frequency=sampling_frequency,
            total_time=1,
            max_harmonic=6,
            phase=reference_signal_phase
    )
    ref_signal[frequency] = pd.DataFrame(signal)

print ("Start acquire data")
window = np.zeros((0, len(eeg_channels)))

'''try:
    scope = Scope(1/d.SamplingRate, xlabel='t/s', ylabel=u'V/μV',               
                    title="Internal Signal Channels: %s") 
    # get data to scope 
    d.GetData(d.SamplingRate, more=scope) 
finally:
    print ("Classification Finish!!")
    TerminateRemoteAPI(clientID)
    d.Close() 
    #server.close()
    del d'''


try:
    while True:
        raw_data = d.GetData(d.SamplingRate)     

        cca = fr.classify_cca(raw_data, ref_signal)
        cca_result = cca["result"]

        x = threading.Thread(target=RobotThread, args=(cca_result,))
        x.start()

        print (cca_result)

        #window = window[d.SamplingRate:d.SamplingRate*3, 0:len(eeg_channels)]
        #window = np.zeros((0, len(eeg_channels)))
            
finally:
    print ("Classification Finish!!")
    TerminateRemoteAPI(clientID)
    d.Close() 
    #server.close()
    del d


