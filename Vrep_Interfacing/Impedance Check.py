import pygds
import numpy as np

'''eeg_channels = [0]

d = pygds.GDS()
pygds.configure_demo(d, testsignal=False, acquire=1)

print ("Checking Impedance")
imps = d.GetImpedance()
print (imps)

d.Close()
del d'''
a = [1,2,3,4,5,6,7,8,9]
window = np.zeros((1, 3))
print (window)