# -*- coding: utf-8 -*-

# Import libraries 
import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d 
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.ticker import MaxNLocator
import matplotlib.ticker as plticker

  
  
# Creating dataset 
x = [1,2,3,4,5,6,7,8,9,10,11,12,13]
y1000 = [1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]
y2000 = [2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000]
y3000 = [3000,3000,3000,3000,3000,3000,3000,3000,3000,3000,3000,3000,3000]
y4000 = [4000,4000,4000,4000,4000,4000,4000,4000,4000,4000,4000,4000,4000]
y5000 = [5000,5000,5000,5000,5000,5000,5000,5000,5000,5000,5000,5000,5000]
y6000 = [6000,6000,6000,6000,6000,6000,6000,6000,6000,6000,6000,6000,6000]
y7000 = [7000,7000,7000,7000,7000,7000,7000,7000,7000,7000,7000,7000,7000]
y8000 = [8000,8000,8000,8000,8000,8000,8000,8000,8000,8000,8000,8000,8000]
y9000 = [9000,9000,9000,9000,9000,9000,9000,9000,9000,9000,9000,9000,9000]
y10000 = [10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000,10000]

z1000 = [204,13,232,28,241,13,250,16,3,0,0,0,0]
z2000 = [414,49,446,62,449,54,455,64,7,0,0,0,0]
z3000 = [593,105,615,146,633,122,632,141,13,0,0,0,0]
z4000 = [737,198,12,791,214,14,761,214,12,826,209,11,1]
z5000 = [884,282,21,934,296,22,934,307,34,961,302,21,2]
z6000 = [1022,365,45,1063,391,44,1093,391,49,1068,422,37,10]
z7000 = [1125,466,70,1191,495,65,1201,520,81,1210,501,52,23]
z8000 = [1249,571,101,1319,603,89,1297,630,110,1323,587,101,20]
z9000 = [1358,689,127,1406,687,164,1379,709,172,1426,713,116,54]
z10000 = [1543,785,204,1526,768,155,1548,765,157,1532,781,167,69]


# Creating figure 
fig = plt.figure(figsize = (10, 7)) 
ax = plt.axes(projection ="3d") 


# Creating plot 

ax.bar3d(x, y10000, 0, 0.5, 1, z10000, color = "#ffd500")

ax.bar3d(x, y9000, 0, 0.5, 1, z9000, color = "#ffff00")
         
ax.bar3d(x, y8000, 0, 0.5, 1, z8000, color = "#b3ff66")
         
ax.bar3d(x, y7000, 0, 0.5, 1, z7000, color = "#33ff99")
         
ax.bar3d(x, y6000, 0, 0.5, 1, z6000, color = "#00ffff")

ax.bar3d(x, y5000, 0, 0.5, 1, z5000, color = "#00bfff")
         
ax.bar3d(x, y4000, 0, 0.5, 1, z4000, color = "#005ce6"); 
         
ax.bar3d(x, y3000, 0, 0.5, 1, z3000, color = "#0033cc") 
         
ax.bar3d(x, y2000, 0, 0.5, 1, z2000, color = "#24248f") 

ax.bar3d(x, y1000, 0, 0.5, 1, z1000, color = "#202060") 


xmin, xmax = 0.5, 20
ymin, ymax = 0, 10000
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(0, 6000)
ax.set_xlabel('layer', size=24)
ax.set_ylabel('n', size=24)
ax.set_zlabel('number of operations in layer', size=20)
ax.tick_params(axis='both', which='major', labelsize=20)

ax.xaxis.labelpad=20
ax.yaxis.labelpad=30
ax.zaxis.labelpad=20
ax.xaxis.set_major_locator(MaxNLocator(integer=True))

plt.tight_layout()
plt.show() 
