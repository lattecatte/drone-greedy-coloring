# -*- coding: utf-8 -*-

# Import libraries 
import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits import mplot3d 
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
  
  
# Creating dataset 
x = [50,100,150,200,250,300]
y1000 = [1000,1000,1000,1000,1000,1000]
y2000 = [2000,2000,2000,2000,2000,2000]
y3000 = [3000,3000,3000,3000,3000,3000]
y4000 = [4000,4000,4000,4000,4000,4000]
y5000 = [5000,5000,5000,5000,5000,5000]
y6000 = [6000,6000,6000,6000,6000,6000]
y7000 = [7000,7000,7000,7000,7000,7000]
y8000 = [8000,8000,8000,8000,8000,8000]
y9000 = [9000,9000,9000,9000,9000,9000]
y10000 = [10000,10000,10000,10000,10000,10000]

z1000 = [0.298,0.5,0.688,0.96,1.16,1.362]
z2000 = [0.457,0.907,1.346,1.782,2.224,2.663]
z3000 = [0.683,1.353,2.042,2.705,3.343,4]
z4000 = [0.9305,1.833,2.72,3.594,4.458,5.289]
z5000 = [1.151,2.292,3.409,4.465,5.527,6.569]
z6000 = [1.365,2.755,4.101,5.368,6.619,7.813]
z7000 = [1.557,3.135,4.645,6.164,7.611,9.045]
z8000 = [1.802,3.614,5.3785,7.127,8.813,10.422]
z9000 = [2.044,4.06,6.056,8.035,9.905,11.771]
z10000 = [2.22,4.442,6.601,8.704,10.737,12.7762]


# Creating figure 
fig = plt.figure(figsize = (10,7)) 
ax = plt.axes(projection ="3d") 

xvert_11 = [50,50,100,100]
yvert_11 = [1000,2000,2000,1000]
zvert_11 = [z1000[0], z2000[0], z2000[1], z1000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#202060"))
yvert_11 = [2000,3000,3000,2000]
zvert_11 = [z2000[0], z3000[0], z3000[1], z2000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#24248f"))
yvert_11 = [3000,4000,4000,3000]
zvert_11 = [z3000[0], z4000[0], z4000[1], z3000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#0033cc"))
yvert_11 = [4000,5000,5000,4000]
zvert_11 = [z4000[0], z5000[0], z5000[1], z4000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#005ce6"))
yvert_11 = [5000,6000,6000,5000]
zvert_11 = [z5000[0], z6000[0], z6000[1], z5000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00bfff"))
yvert_11 = [6000,7000,7000,6000]
zvert_11 = [z6000[0], z7000[0], z7000[1], z6000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00ffff"))
yvert_11 = [7000,8000,8000,7000]
zvert_11 = [z7000[0], z8000[0], z8000[1], z7000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#33ff99"))
yvert_11 = [8000,9000,9000,8000]
zvert_11 = [z8000[0], z9000[0], z9000[1], z8000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#b3ff66"))
yvert_11 = [9000,10000,10000,9000]
zvert_11 = [z9000[0], z10000[0], z10000[1], z9000[1]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#ffff00"))

xvert_11 = [100,100,150,150]
yvert_11 = [1000,2000,2000,1000]
zvert_11 = [z1000[1], z2000[1], z2000[2], z1000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#202060"))
yvert_11 = [2000,3000,3000,2000]
zvert_11 = [z2000[1], z3000[1], z3000[2], z2000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#24248f"))
yvert_11 = [3000,4000,4000,3000]
zvert_11 = [z3000[1], z4000[1], z4000[2], z3000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#0033cc"))
yvert_11 = [4000,5000,5000,4000]
zvert_11 = [z4000[1], z5000[1], z5000[2], z4000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#005ce6"))
yvert_11 = [5000,6000,6000,5000]
zvert_11 = [z5000[1], z6000[1], z6000[2], z5000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00bfff"))
yvert_11 = [6000,7000,7000,6000]
zvert_11 = [z6000[1], z7000[1], z7000[2], z6000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00ffff"))
yvert_11 = [7000,8000,8000,7000]
zvert_11 = [z7000[1], z8000[1], z8000[2], z7000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#33ff99"))
yvert_11 = [8000,9000,9000,8000]
zvert_11 = [z8000[1], z9000[1], z9000[2], z8000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#b3ff66"))
yvert_11 = [9000,10000,10000,9000]
zvert_11 = [z9000[1], z10000[1], z10000[2], z9000[2]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#ffff00"))

xvert_11 = [150,150,200,200]
yvert_11 = [1000,2000,2000,1000]
zvert_11 = [z1000[2], z2000[2], z2000[3], z1000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#202060"))
yvert_11 = [2000,3000,3000,2000]
zvert_11 = [z2000[2], z3000[2], z3000[3], z2000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#24248f"))
yvert_11 = [3000,4000,4000,3000]
zvert_11 = [z3000[2], z4000[2], z4000[3], z3000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#0033cc"))
yvert_11 = [4000,5000,5000,4000]
zvert_11 = [z4000[2], z5000[2], z5000[3], z4000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#005ce6"))
yvert_11 = [5000,6000,6000,5000]
zvert_11 = [z5000[2], z6000[2], z6000[3], z5000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00bfff"))
yvert_11 = [6000,7000,7000,6000]
zvert_11 = [z6000[2], z7000[2], z7000[3], z6000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00ffff"))
yvert_11 = [7000,8000,8000,7000]
zvert_11 = [z7000[2], z8000[2], z8000[3], z7000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#33ff99"))
yvert_11 = [8000,9000,9000,8000]
zvert_11 = [z8000[2], z9000[2], z9000[3], z8000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#b3ff66"))
yvert_11 = [9000,10000,10000,9000]
zvert_11 = [z9000[2], z10000[2], z10000[3], z9000[3]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#ffff00"))

xvert_11 = [200,200,250,250]
yvert_11 = [1000,2000,2000,1000]
zvert_11 = [z1000[3], z2000[3], z2000[4], z1000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#202060"))
yvert_11 = [2000,3000,3000,2000]
zvert_11 = [z2000[3], z3000[3], z3000[4], z2000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#24248f"))
yvert_11 = [3000,4000,4000,3000]
zvert_11 = [z3000[3], z4000[3], z4000[4], z3000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#0033cc"))
yvert_11 = [4000,5000,5000,4000]
zvert_11 = [z4000[3], z5000[3], z5000[4], z4000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#005ce6"))
yvert_11 = [5000,6000,6000,5000]
zvert_11 = [z5000[3], z6000[3], z6000[4], z5000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00bfff"))
yvert_11 = [6000,7000,7000,6000]
zvert_11 = [z6000[3], z7000[3], z7000[4], z6000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00ffff"))
yvert_11 = [7000,8000,8000,7000]
zvert_11 = [z7000[3], z8000[3], z8000[4], z7000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#33ff99"))
yvert_11 = [8000,9000,9000,8000]
zvert_11 = [z8000[3], z9000[3], z9000[4], z8000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#b3ff66"))
yvert_11 = [9000,10000,10000,9000]
zvert_11 = [z9000[3], z10000[3], z10000[4], z9000[4]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#ffff00"))
                                     
xvert_11 = [250,250,300,300]

yvert_11 = [1000,2000,2000,1000]
zvert_11 = [z1000[4], z2000[4], z2000[5], z1000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#202060"))
yvert_11 = [2000,3000,3000,2000]
zvert_11 = [z2000[4], z3000[4], z3000[5], z2000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#24248f"))
yvert_11 = [3000,4000,4000,3000]
zvert_11 = [z3000[4], z4000[4], z4000[5], z3000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#0033cc"))
yvert_11 = [4000,5000,5000,4000]
zvert_11 = [z4000[4], z5000[4], z5000[5], z4000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#005ce6"))
yvert_11 = [5000,6000,6000,5000]
zvert_11 = [z5000[4], z6000[4], z6000[5], z5000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00bfff"))
yvert_11 = [6000,7000,7000,6000]
zvert_11 = [z6000[4], z7000[4], z7000[5], z6000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#00ffff"))
yvert_11 = [7000,8000,8000,7000]
zvert_11 = [z7000[4], z8000[4], z8000[5], z7000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#33ff99"))
yvert_11 = [8000,9000,9000,8000]
zvert_11 = [z8000[4], z9000[4], z9000[5], z8000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#b3ff66"))
yvert_11 = [9000,10000,10000,9000]
zvert_11 = [z9000[4], z10000[4], z10000[5], z9000[5]]
verts_11 = [list(zip(xvert_11, yvert_11, zvert_11))]
ax.add_collection3d(Poly3DCollection(verts_11, alpha=0.5, color="#ffff00"))
                                     

# Creating plot 
ax.scatter3D(x, y1000, z1000, color = "k"); 
ax.plot(x, y1000, z1000, color="k")

ax.scatter3D(x, y2000, z2000, color = "k"); 
ax.plot(x, y2000, z2000, color="k")

ax.scatter3D(x, y3000, z3000, color = "k"); 
ax.plot(x, y3000, z3000, color="k")

ax.scatter3D(x, y4000, z4000, color = "k"); 
ax.plot(x, y4000, z4000, color="k")

ax.scatter3D(x, y5000, z5000, color = "k"); 
ax.plot(x, y5000, z5000, color="k")

ax.scatter3D(x, y6000, z6000, color = "k"); 
ax.plot(x, y6000, z6000, color="k")

ax.scatter3D(x, y7000, z7000, color = "k"); 
ax.plot(x, y7000, z7000, color="k")

ax.scatter3D(x, y8000, z8000, color = "k"); 
ax.plot(x, y8000, z8000, color="k")

ax.scatter3D(x, y9000, z9000, color = "k"); 
ax.plot(x, y9000, z9000, color="k")

ax.scatter3D(x, y10000, z10000, color = "k"); 
ax.plot(x, y10000, z10000, color="k")

xmin, xmax = 300, 0
ymin, ymax = 0, 10000
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(0, 14)
ax.set_xlabel('conflict distance R [m]', size=14)
ax.set_ylabel('number of operations n', size=14)
ax.set_zlabel('average number of conflicts per operation', size=14)

ax.xaxis.labelpad=20
ax.yaxis.labelpad=20
ax.zaxis.labelpad=10

plt.tight_layout()
plt.show() 
