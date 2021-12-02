import socket
import numpy as np
import math

#Communication settings
UDP_IP = "10.24.93.248"
UDP_PORT = 1234
sock = socket.socket(socket.AF_INET, #Internet
                     socket.SOCK_DGRAM) #UDP

#Simulation Settings
time = 2000
dt = 0.01
timeSeries = np.arange(0,time,dt)

#System description
A = np.identity(6, dtype=int)
B_t = np.array([[1,0],[0,0],[0,1]])
M = np.array([[25.8,0,0],[0,33.8,6.2],[0,6.2,2.76]])
M_ = np.linalg.inv(M)
B = dt * np.concatenate((np.array([[0,0],[0,0],[0,0]]),np.dot(M_,B_t)),axis=0)
C = np.identity(6, dtype=int)

#System parameters
m22 = 33.8
m23 = 6.2
m32 = 6.2
m11 = 25.8
Xu = -12
Xuu = -2.1
Yv = -17
Yvv = -4.5
Yr = -0.2
Nv = -0.5
Nr = -0.5
Nrr = -0.1


#System inputs
u = np.array([[5],[0]])


#Initialization of system states
x = np.array([[0],[0],[0],[0],[0],[0]])


#Simulation loop
for t in range(len(timeSeries)):

    c13 = -m22*x[4,0] - ((m23+m32)/2)*x[5,0]
    c23 = m11*x[3,0]
    Cv = np.array([[0,0,c13],[0,0,c23],[-c13,-c23,0]])
    Dv = -1*np.array([[Xu+Xuu*abs(x[3,0]),0,0],[0,Yv+Yvv*abs(x[4,0]),Yr],[0,Nv,Nr+Nrr*abs(x[5,0])]])

    
    #States 
    x = np.dot(A,x) + dt*np.concatenate((np.array([[math.cos(x[2,0])*x[3,0]-math.sin(x[2,0])*x[4,0]],
                           [math.sin(x[2,0])*x[3,0]+math.cos(x[2,0])*x[4,0]],
                           [x[5,0]]]),np.dot(-M_,np.dot((Cv+Dv),np.array([[x[3,0]],[x[4,0]],[x[5,0]]])))),axis=0) + np.dot(B,u)


  
    #Data formatting
    s = str("{0:.6f}".format(x[0,0])).zfill(10)+","+str("{0:.6f}".format(x[1,0])).zfill(10)
    s_b = bytes(s,encoding="ascii")
  
    #Real-time Communication
    print("Sending...") 
    sock.sendto(s_b, (UDP_IP, UDP_PORT))
   

print("Done!")







