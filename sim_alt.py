import numpy as np
import time
import sys
# from shapely.geometry import Polygon
import itertools
import operator
from operator import attrgetter
# import winsound
import networkx as nx
from collections import Counter

from plot import *
from coloring import *

sys.setrecursionlimit(100000)
start_time = time.time()

max_time = 10000
max_range = 10000       # INDEPENDENT VARIBALE
r = 150                 # INDEPENDENT VARIBALE
v_max = 20              # INDEPENDENT VARIBALE
safedist_horizontal = 30 * v_max
v_ascent = 2
safedist_vertical = 5 * v_ascent
altitude_default = 4 #20
altitude_levels = [140, 120, 100, 80, 60, 40]

class Drone:
    # parameters from flight plan
    def __init__(self, x0, y0, x1, y1, t0, priority, number):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.t0 = t0
        self.priority = priority
        self.number = number
        self.z = altitude_default
        self.z_top = self.z + safedist_vertical
        self.z_bottom = self.z - safedist_vertical
 
    def parameters(self):        
        self.overlap_count = 0
        self.overlap_friends = []
        
        # displace and time
        self.ds_takeoff = 0
        self.ds_landing = 0
        self.ds_horizontal = np.sqrt((self.x1 - self.x0)**2 + (self.y1 - self.y0)**2)
        self.ds = self.ds_takeoff + self.ds_horizontal + self.ds_landing
        self.dt_takeoff = 0     # self.ds_takeoff / v_ascent
        self.dt_landing = 0     # self.ds_landing / v_ascent
        self.dt_horizontal = self.ds_horizontal / v_max
        self.dt = self.dt_takeoff + self.dt_horizontal + self.dt_landing
        self.t_takeoff_done = self.t0 + self.dt_takeoff
        self.t_landing_standby = self.t_takeoff_done + self.dt_horizontal
        self.t1 = self.t_landing_standby + self.dt_landing
        
        # pre-flight volumes
        self.dx = self.x1 - self.x0
        self.dy = self.y1 - self.y0
        if self.dx != 0:
            self.grad = self.dy / self.dx
        else:
            self.grad = 0
        self.b = self.y0 - self.grad * self.x0
        self.angle = np.arctan(self.grad)
        
        # angle adjustments for vectors in 2nd, 3rd quadrants
        if self.dx < 0:
            self.angle += np.pi
        elif self.dy < 0 and self.dx > 0:
            self.angle += 2*np.pi
        elif self.dx == 0 and self.dy >= 0:
            self.angle = 0.5*np.pi
        elif self.dx == 0 and self.dy < 0:
            self.angle = 1.5*np.pi
            
        # volume points
        self.xy0_bl = self.get_diag_points(self.x0,-1,-1, self.y0, 1,-1)
        self.xy0_br = self.get_diag_points(self.x0,-1, 1, self.y0,-1,-1)
        self.xy0_tl = self.get_diag_points(self.x0, 1,-1, self.y0, 1, 1)
        self.xy0_tr = self.get_diag_points(self.x0, 1, 1, self.y0,-1, 1)       
        self.xy1_bl = self.get_diag_points(self.x1,-1,-1, self.y1, 1,-1)
        self.xy1_br = self.get_diag_points(self.x1,-1, 1, self.y1,-1,-1)
        self.xy1_tl = self.get_diag_points(self.x1, 1,-1, self.y1, 1, 1)
        self.xy1_tr = self.get_diag_points(self.x1, 1, 1, self.y1,-1, 1)
        
    def rel_dist(self, other, t):
        self.xnow = self.x0 + (v_max*np.cos(self.angle)) * (t - self.t0)
        self.ynow = self.y0 + (v_max*np.sin(self.angle)) * (t - self.t0)
        other.xnow = other.x0 + (v_max*np.cos(other.angle)) * (t - other.t0)
        other.ynow = other.y0 + (v_max*np.sin(other.angle)) * (t - other.t0)
        self.dr = np.sqrt((other.xnow - self.xnow)**2 + (other.ynow - self.ynow)**2)
        return (self.xnow, other.xnow, self.dr)
      
    def get_diag_points(self, x0, xcos, xsin, y0, ycos, ysin):  # xcos refers to the coefficient of cos for x
        x_diag = x0 + safedist_horizontal*(xcos*np.cos(self.angle) + xsin*np.sin(self.angle))
        y_diag = y0 + safedist_horizontal*(ycos*np.cos(self.angle) + ysin*np.sin(self.angle))
        return x_diag, y_diag

    # check xy intersection without calculating crit point
    def ccwACD(self, other):
        return (other.y1-self.y0) * (other.x0-self.x0) > (other.y0-self.y0) * (other.x1-self.x0)
    
    def ccwBCD(self, other):  
        return (other.y1-self.y1) * (other.x0-self.x1) > (other.y0-self.y1) * (other.x1-self.x1)
        
    def ccwABC(self, other):
        return (other.y0-self.y0) * (self.x1-self.x0) > (self.y1-self.y0) * (other.x0-self.x0)
        
    def ccwABD(self, other):
        return (other.y1-self.y0) * (self.x1-self.x0) > (self.y1-self.y0) * (other.x1-self.x0)
        
    def check_xy_intersect(self, other):     #return true if line segments AB and CD intersect
        return self.ccwACD(other) != self.ccwBCD(other) and self.ccwABC(other) != self.ccwABD(other)

    def check_intersect(self, other):
        if (self.t1 > other.t0):
            if  (self.check_xy_intersect(other) == True) and (self.z == other.z):
                return True
            else:
                return False
        else:
            return False
    
    def get_intersect(self, other):
        self.x_crit = (self.b - other.b) / (other.grad - self.grad)
        other.x_crit = self.x_crit
        self.y_crit = self.grad * self.x_crit + self.b 
        other.y_crit = self.y_crit
        self.t_crit = self.t0 + (self.x_crit - self.x0) / (v_max*np.cos(self.angle))
        other.t_crit = other.t0 + (other.x_crit - other.x0) / (v_max*np.cos(other.angle))
        return (self.x_crit, self.y_crit, self.t_crit, other.t_crit)

def activate_parameters():
    for n in range(len(drone_list)):
        drone_list[n].parameters()
    
def get_flight_info():
    for n in range(len(drone_list)):
        print("Drone", n, "dt takeoff", drone_list[n].dt_takeoff, "dt hotizontal", drone_list[n].dt_horizontal, "dt", drone_list[n].dt)
        print("Drone", n, "ds takeoff", drone_list[n].ds_takeoff, "ds horizontal", drone_list[n].ds_horizontal, "ds", drone_list[n].ds)
    print("Sum dt", sum(drone.dt for drone in drone_list))

def print_lists():
    print("overlap list", len(overlap_list))
    print("allowed list", len(allowed_list))

seconds = time.time()

# adding drones
drone_list = []
n_count = 1000  # INDEPENDENT VARIBALE
m = 10

# randomizing position and time
np.random.seed(133769)  # input random seed
random_pos = np.random.randint(0, max_range, size=4*n_count)
random_time = np.random.randint(0, max_time, size=n_count)

for n in range(n_count):
    drone_list.append(Drone(random_pos[4*n], random_pos[4*n+1], random_pos[4*n+2], random_pos[4*n+3], t0=random_time[n], priority=0, number=n))
    drone_list[n].parameters()

drone_list = sorted(drone_list, key=operator.attrgetter('t0'))
graph = np.zeros(shape=(n_count, n_count))

# print info and subdivide to heading-based arrays for decentralized method
# make layer_list
layer21_list, layer22_list, layer31_list, layer32_list, layer33_list = [], [], [], [], []
layer41_list, layer42_list, layer43_list, layer44_list = [], [], [], []
layer_list = [layer21_list, layer22_list, layer31_list, layer32_list, layer33_list, layer41_list, layer42_list, layer43_list, layer44_list]

for n in range(n_count):    
    print(n, "POS", drone_list[n].x0, drone_list[n].y0, drone_list[n].x1, drone_list[n].y1, "m", drone_list[n].grad, "b", drone_list[n].b)
    print(n, "TIME", drone_list[n].t0, drone_list[n].t1)
    
    if (drone_list[n].angle >= 0) and (drone_list[n].angle < np.pi):
        layer21_list.append(drone_list[n])
    else:
        layer22_list.append(drone_list[n])
    
    if (drone_list[n].angle >= 0) and (drone_list[n].angle < 2/3*np.pi):
        layer31_list.append(drone_list[n])
    elif (drone_list[n].angle >= 2/3*np.pi) and (drone_list[n].angle < 4/3*np.pi):
        layer32_list.append(drone_list[n])
    else:
        layer33_list.append(drone_list[n])
        
    if (drone_list[n].angle >= 0) and (drone_list[n].angle < 1/2*np.pi):
        layer41_list.append(drone_list[n])
    elif (drone_list[n].angle >= 1/2*np.pi) and (drone_list[n].angle < np.pi):
        layer42_list.append(drone_list[n])
    elif (drone_list[n].angle >= np.pi) and (drone_list[n].angle < 3/2*np.pi):
        layer43_list.append(drone_list[n])
    else:
        layer44_list.append(drone_list[n])

# make layer_graph
layer_graph = []
for ll in layer_list:
    layer_graph.append(np.zeros(shape=(len(ll), len(ll))))    

# color list for 2d and 3d plots
x = np.arange(n)
ys = [i+x+(i*x)**2 for i in range(n_count)]
color_list = cm.rainbow(np.linspace(0, 1, len(ys)))

# combinations
combinations = []
for comb in itertools.combinations((list(range(len(drone_list)))), 2):
    combinations.append(comb)

# make layer_combinations
layer_combinations = []
for ll in layer_list:
    for comb in itertools.combinations((list(range(len(ll)))), 2):
        layer_combinations.append(comb)
print(layer_combinations[0])
### MAIN LOOP
for i in range(len(combinations)):
    if drone_list[combinations[i][0]].check_intersect(drone_list[combinations[i][1]]) == True:
        crit = drone_list[combinations[i][0]].get_intersect(drone_list[combinations[i][1]])
        drone_list[combinations[i][0]].t_min = min(drone_list[combinations[i][0]].t_crit, drone_list[combinations[i][0]].t_crit)
        drone_list[combinations[i][0]].t_max = max(drone_list[combinations[i][0]].t_crit, drone_list[combinations[i][0]].t_crit)
          
        prev_rel = 100000000
        for t in range(int(drone_list[combinations[i][0]].t_min - 60), int(drone_list[combinations[i][0]].t_max + 60), 1):
            rel = drone_list[combinations[i][0]].rel_dist(drone_list[combinations[i][1]], t)
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                graph[combinations[i][0]][combinations[i][1]] = 1
                graph[combinations[i][1]][combinations[i][0]] = 1
                drone_list[combinations[i][0]].overlap_count += 1
                drone_list[combinations[i][1]].overlap_count += 1
                drone_list[combinations[i][0]].overlap_friends.append(combinations[i][1])
                drone_list[combinations[i][1]].overlap_friends.append(combinations[i][0])
                break
#######
for i in range(len(layer_list)):
    if layer_list[i][layer_combinations[i][i][0]].check_intersect(layer_list[i][layer_combinations[i][i][1]]) == True:
        crit = layer_list[i][layer_combinations[i][i][0]].get_intersect(layer_list[i][layer_combinations[i][i][1]])
        layer_list[i][layer_combinations[i][i][0]].t_min = min(layer_list[i][layer_combinations[i][i][0]].t_crit, layer_list[i][layer_combinations[i][i][0]].t_crit)
        layer_list[i][layer_combinations[i][i][0]].t_max = max(layer_list[i][layer_combinations[i][i][0]].t_crit, layer_list[i][layer_combinations[i][i][0]].t_crit)  
        prev_rel = 100000000

        for t in range(int(layer_list[i][layer_combinations[i][i][0]].t_min - 60), int(layer_list[i][layer_combinations[i][i][0]].t_max + 60), 1):
            rel = layer_list[i][layer_combinations[i][i][0]].rel_dist(layer_list[i][layer_combinations[i][i][1]], t)
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer_graph[i][layer_combinations[i][i][0]][layer_combinations[i][i][1]] = 1
                layer_graph[i][layer_combinations[i][i][1]][layer_combinations[i][i][0]] = 1
                layer_list[i][layer_combinations[i][i][0]].overlap_count += 1
                layer_list[i][layer_combinations[i][i][1]].overlap_count += 1
                layer_list[i][layer_combinations[i][i][0]].overlap_friends.append(layer_combinations[i][i][1])
                layer_list[i][layer_combinations[i][i][1]].overlap_friends.append(layer_combinations[i][i][0])
                break

print("---------------------------", v_max, r, n_count, "---------------------------")

### CENTRALIZED
print("--------------------------------------------")
print("CENTRALIZED: GREEDY COLORING METHOD")
G = nx.from_numpy_array(graph)
print("number of nodes, edges", nx.number_of_nodes(G), nx.number_of_edges(G))

degree_list = []
for i in G:
    degree_list.append(G.degree(i))
average_degree = sum(degree_list) / len(degree_list)
max_degree = max(degree_list)
print("average degree, eq layers", average_degree, max_degree+1)

d = nx.coloring.greedy_color(G)
dlist = []
for x in d.values():
    dlist.append(x)
print("Designated layers:")
unique2, counts2 = np.unique(dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

print("--------------------------------------------")
print("--------------------------------------------")

### DECENTRALIZED (2-HEADING RESTRICTED)
# making layer_heading=count and layer_angle
layer_heading_count = [2, 2, 3, 3, 3, 4, 4, 4, 4]
layer_angle = [[0,180], [180,360], [0,120], [120, 240], [240,360], [0,90], [90,180], [180,270], [270,360]]
for ll in layer_list:
    print("--------------------------------------------")
    print(f"DECENTRALIZED ({layer_heading_count[ll]}-HEADING RESTRICTED): GREEDY COLORING METHOD")
    print(f"----- {layer_angle[ll][0]} <= ANGLE < {layer_angle[ll][1]} -----")
    network = nx.from_numpy_array(layer_graph[ll])
    print("number of nodes, edges", nx.number_of_nodes(network), nx.number_of_edges(network))

    degree_list = []
    for i in network:
        degree_list.append(network.degree(i))
    average_degree = sum(degree_list) / len(degree_list)
    max_degree = max(degree_list)
    print("average degree, eq layers", average_degree, max_degree + 1)

    colors = nx.coloring.greedy_color(network)
    color_list = []
    for c in colors.values():
        color_list.append(c)
    print("Designated layers:")
    unique2, counts2 = np.unique(color_list, return_counts=True)
    print(dict(zip(unique2, counts2)))

print("\n")

print("Program took", time.time() - start_time, "seconds")
# winsound.Beep(880,3000)