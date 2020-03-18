# This code is interfaced between Python code and V-rep Simulation

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

print ("Program started")
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',20001,True,True,5000,5) # Connect to V-REP
if clientID!=-1:
    emptyBuff = bytearray()
    print ('Connected to remote API server')

    res, targetPosObj = vrep.simxGetObjectHandle(clientID, 'UR5_target', vrep.simx_opmode_oneshot_wait)
    res, currentTargetPos = vrep.simxGetObjectPosition(clientID, targetPosObj, -1, vrep.simx_opmode_oneshot_wait)
    print (currentTargetPos)
    
    vrep.simxSetObjectPosition(clientID, targetPosObj, -1, [currentTargetPos[0], currentTargetPos[1], currentTargetPos[2]- 0.1], vrep.simx_opmode_oneshot_wait)
  
    # Now send some data to V-REP in a non-blocking fashion:
    vrep.simxAddStatusbarMessage(clientID,'Hello V-REP!',vrep.simx_opmode_oneshot)

    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
