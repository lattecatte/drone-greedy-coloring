# -*- coding: utf-8 -*-

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

#a_const = 2
#dt_vmax = v_max / a_const
#ds_vmax = 0.5 * a_const * dt_vmax**2
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
        
        # calculations
#        self.ds_takeoff = self.z
#        self.ds_landing = self.z
        self.ds_takeoff = 0
        self.ds_landing = 0
        self.ds_horizontal = np.sqrt((self.x1 - self.x0)**2 + (self.y1 - self.y0)**2)
#        self.ds_cruise = self.ds_horizontal - 2 * ds_vmax
        self.ds = self.ds_takeoff + self.ds_horizontal + self.ds_landing
        
        self.dt_takeoff = 0 #self.ds_takeoff / v_ascent
        self.dt_landing = 0 #self.ds_landing / v_ascent
#        self.dt_cruise = self.ds_cruise / v_max
#        self.dt_horizontal = self.dt_cruise + 2 * dt_vmax
        self.dt_horizontal = self.ds_horizontal / v_max
        self.dt = self.dt_takeoff + self.dt_horizontal + self.dt_landing
        
        self.t_takeoff_done = self.t0 + self.dt_takeoff
        self.t_landing_standby = self.t_takeoff_done + self.dt_horizontal
        self.t1 = self.t_landing_standby + self.dt_landing
        
        ### PRE-FLIGHT VOLUME
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

        # self.vol_takeoff = Polygon([self.xy0_bl, self.xy0_br, self.xy0_tr, self.xy0_tl])
        # self.vol_landing = Polygon([self.xy1_bl, self.xy1_br, self.xy1_tr, self.xy1_tl])
        # self.vol_horizontal = Polygon([self.xy0_bl, self.xy0_br, self.xy1_tr, self.xy1_tl])
        
    def rel_dist(self, other, t):
        self.xnow = self.x0 + (v_max*np.cos(self.angle)) * (t - self.t0)
        self.ynow = self.y0 + (v_max*np.sin(self.angle)) * (t - self.t0)
        other.xnow = other.x0 + (v_max*np.cos(other.angle)) * (t - other.t0)
        other.ynow = other.y0 + (v_max*np.sin(other.angle)) * (t - other.t0)

        self.dr = np.sqrt((other.xnow - self.xnow)**2 + (other.ynow - self.ynow)**2)
        
        return (self.xnow, other.xnow, self.dr)
      
    def get_diag_points(self, x0, xcos, xsin, y0, ycos, ysin):                  # xcos refers to the coefficient of cos for x
        x_diag = x0 + safedist_horizontal*(xcos*np.cos(self.angle) + xsin*np.sin(self.angle))
        y_diag = y0 + safedist_horizontal*(ycos*np.cos(self.angle) + ysin*np.sin(self.angle))
        return x_diag, y_diag

    ### check xy intersection without calculating crit point
    def ccwACD(self, other):
        return (other.y1-self.y0) * (other.x0-self.x0) > (other.y0-self.y0) * (other.x1-self.x0)
    
    def ccwBCD(self,other):  
        return (other.y1-self.y1) * (other.x0-self.x1) > (other.y0-self.y1) * (other.x1-self.x1)
        
    def ccwABC(self,other):
        return (other.y0-self.y0) * (self.x1-self.x0) > (self.y1-self.y0) * (other.x0-self.x0)
        
    def ccwABD(self,other):
        return (other.y1-self.y0) * (self.x1-self.x0) > (self.y1-self.y0) * (other.x1-self.x0)
        
    # Return true if line segments AB and CD intersect
    def check_xy_intersect(self,other):
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
        #    print("dt", drone_list[n].dt_horizontal, drone_list[n].ds_horizontal / v_max, drone_list[n].t)
        #    print("t", drone_list[n].t0, drone_list[n].t_takeoff_done, drone_list[n].t_landing_standby, drone_list[n].t1)
        #    print("angle", drone_list[n].angle)

def print_lists():
    print("overlap list", len(overlap_list))
    print("allowed list", len(allowed_list))

seconds = time.time()

### ADDING DRONES
drone_list = []
n_count = 1000           # INDEPENDENT VARIBALE
m = 10

# RANDOMIZING POS AND TIME
np.random.seed(133769)
#drone_list.append(Drone(1000,1000,2000,2000, t0=0, priority=0))
random_pos = np.random.randint(0, max_range, size=4*n_count)
random_time = np.random.randint(0, max_time, size=n_count)

for n in range(n_count):
    drone_list.append(Drone(random_pos[4*n], random_pos[4*n+1], random_pos[4*n+2], random_pos[4*n+3], t0=random_time[n], priority=0, number=n))
    drone_list[n].parameters()

drone_list = sorted(drone_list, key=operator.attrgetter('t0'))
graph = np.zeros(shape=(n_count, n_count))

# PRINT INFO AND SUBDIVIDE TO HEADING-BASED ARRAYS FOR DECENTRALIZED METHOD
layer21_list, layer22_list, layer31_list, layer32_list, layer33_list = [], [], [], [], []
layer41_list, layer42_list, layer43_list, layer44_list = [], [], [], []

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
    
layer21_graph = np.zeros(shape=(len(layer21_list), len(layer21_list)))
layer22_graph = np.zeros(shape=(len(layer22_list), len(layer22_list)))
layer31_graph = np.zeros(shape=(len(layer31_list), len(layer31_list)))
layer32_graph = np.zeros(shape=(len(layer32_list), len(layer32_list)))
layer33_graph = np.zeros(shape=(len(layer33_list), len(layer33_list)))
layer41_graph = np.zeros(shape=(len(layer41_list), len(layer41_list)))
layer42_graph = np.zeros(shape=(len(layer42_list), len(layer42_list)))
layer43_graph = np.zeros(shape=(len(layer43_list), len(layer43_list)))
layer44_graph = np.zeros(shape=(len(layer44_list), len(layer44_list)))

# COLOR LIST FOR 2D AND 3D PLOTS
x = np.arange(n)
ys = [i+x+(i*x)**2 for i in range(n_count)]
color_list = cm.rainbow(np.linspace(0, 1, len(ys)))

# COMBINATIONS
combinations = []
for comb in itertools.combinations((list(range(len(drone_list)))), 2):
    combinations.append(comb)
#print("-----Combination list", combinations)

layer21_combinations, layer22_combinations = [], []
for comb in itertools.combinations((list(range(len(layer21_list)))), 2):
    layer21_combinations.append(comb)
    
for comb in itertools.combinations((list(range(len(layer22_list)))), 2):
    layer22_combinations.append(comb)

layer31_combinations, layer32_combinations, layer33_combinations = [], [], []
for comb in itertools.combinations((list(range(len(layer31_list)))), 2):
    layer31_combinations.append(comb)
    
for comb in itertools.combinations((list(range(len(layer32_list)))), 2):
    layer32_combinations.append(comb)

for comb in itertools.combinations((list(range(len(layer33_list)))), 2):
    layer33_combinations.append(comb)

layer41_combinations, layer42_combinations, layer43_combinations, layer44_combinations = [], [], [], []
for comb in itertools.combinations((list(range(len(layer41_list)))), 2):
    layer41_combinations.append(comb)
    
for comb in itertools.combinations((list(range(len(layer42_list)))), 2):
    layer42_combinations.append(comb)

for comb in itertools.combinations((list(range(len(layer43_list)))), 2):
    layer43_combinations.append(comb)

for comb in itertools.combinations((list(range(len(layer44_list)))), 2):
    layer44_combinations.append(comb)

### MAIN LOOP
for i in range(len(combinations)):
#    print("Drone", combinations[i][0], "against", combinations[i][1], drone_list[combinations[i][0]].check_intersect(drone_list[combinations[i][1]]))
#    print(combinations[i][0])
    if drone_list[combinations[i][0]].check_intersect(drone_list[combinations[i][1]]) == True:
        
        crit = drone_list[combinations[i][0]].get_intersect(drone_list[combinations[i][1]])
#        print(combinations[i][0], combinations[i][1], "crit", crit)
        
        drone_list[combinations[i][0]].t_min = min(drone_list[combinations[i][0]].t_crit, drone_list[combinations[i][0]].t_crit)
        drone_list[combinations[i][0]].t_max = max(drone_list[combinations[i][0]].t_crit, drone_list[combinations[i][0]].t_crit)
          
#        for t in range(int(drone_list[combinations[i][0]].t0), int(drone_list[combinations[i][0]].t1), 10):
        prev_rel = 100000000
        for t in range(int(drone_list[combinations[i][0]].t_min - 60), int(drone_list[combinations[i][0]].t_max + 60), 1):

            rel = drone_list[combinations[i][0]].rel_dist(drone_list[combinations[i][1]], t)
#            print(combinations[i][0], combinations[i][1], "rel", rel)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
#                print("overlap detected")
                graph[combinations[i][0]][combinations[i][1]] = 1
                graph[combinations[i][1]][combinations[i][0]] = 1
                drone_list[combinations[i][0]].overlap_count += 1
                drone_list[combinations[i][1]].overlap_count += 1
                drone_list[combinations[i][0]].overlap_friends.append(combinations[i][1])
                drone_list[combinations[i][1]].overlap_friends.append(combinations[i][0])
                break
#            else:
#                drone_list[combinations[i][0]].overlap_count = 0
#                drone_list[combinations[i][1]].overlap_count = 0
#                drone_list[combinations[i][0]].overlap_friends.clear()
#                drone_list[combinations[i][1]].overlap_friends.clear()

#for n in range(len(drone_list)):
#    print(n, drone_list[n].t0, drone_list[n].t1, drone_list[n].overlap_count, drone_list[n].overlap_friends)

for i in range(len(layer21_combinations)):
    if layer21_list[layer21_combinations[i][0]].check_intersect(layer21_list[layer21_combinations[i][1]]) == True:
        
        crit = layer21_list[layer21_combinations[i][0]].get_intersect(layer21_list[layer21_combinations[i][1]])
        
        layer21_list[layer21_combinations[i][0]].t_min = min(layer21_list[layer21_combinations[i][0]].t_crit, layer21_list[layer21_combinations[i][0]].t_crit)
        layer21_list[layer21_combinations[i][0]].t_max = max(layer21_list[layer21_combinations[i][0]].t_crit, layer21_list[layer21_combinations[i][0]].t_crit)
          
        prev_rel = 100000000
        for t in range(int(layer21_list[layer21_combinations[i][0]].t_min - 60), int(layer21_list[layer21_combinations[i][0]].t_max + 60), 1):

            rel = layer21_list[layer21_combinations[i][0]].rel_dist(layer21_list[layer21_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer21_graph[layer21_combinations[i][0]][layer21_combinations[i][1]] = 1
                layer21_graph[layer21_combinations[i][1]][layer21_combinations[i][0]] = 1
                layer21_list[layer21_combinations[i][0]].overlap_count += 1
                layer21_list[layer21_combinations[i][1]].overlap_count += 1
                layer21_list[layer21_combinations[i][0]].overlap_friends.append(layer21_combinations[i][1])
                layer21_list[layer21_combinations[i][1]].overlap_friends.append(layer21_combinations[i][0])
                break

for i in range(len(layer22_combinations)):
    if layer22_list[layer22_combinations[i][0]].check_intersect(layer22_list[layer22_combinations[i][1]]) == True:
        
        crit = layer22_list[layer22_combinations[i][0]].get_intersect(layer22_list[layer22_combinations[i][1]])
        
        layer22_list[layer22_combinations[i][0]].t_min = min(layer22_list[layer22_combinations[i][0]].t_crit, layer22_list[layer22_combinations[i][0]].t_crit)
        layer22_list[layer22_combinations[i][0]].t_max = max(layer22_list[layer22_combinations[i][0]].t_crit, layer22_list[layer22_combinations[i][0]].t_crit)
        
        
        prev_rel = 100000000
        for t in range(int(layer22_list[layer22_combinations[i][0]].t_min - 60), int(layer22_list[layer22_combinations[i][0]].t_max + 60), 1):

            rel = layer22_list[layer22_combinations[i][0]].rel_dist(layer22_list[layer22_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer22_graph[layer22_combinations[i][0]][layer22_combinations[i][1]] = 1
                layer22_graph[layer22_combinations[i][1]][layer22_combinations[i][0]] = 1
                layer22_list[layer22_combinations[i][0]].overlap_count += 1
                layer22_list[layer22_combinations[i][1]].overlap_count += 1
                layer22_list[layer22_combinations[i][0]].overlap_friends.append(layer22_combinations[i][1])
                layer22_list[layer22_combinations[i][1]].overlap_friends.append(layer22_combinations[i][0])
                break

for i in range(len(layer31_combinations)):
    if layer31_list[layer31_combinations[i][0]].check_intersect(layer31_list[layer31_combinations[i][1]]) == True:
        
        crit = layer31_list[layer31_combinations[i][0]].get_intersect(layer31_list[layer31_combinations[i][1]])
        
        layer31_list[layer31_combinations[i][0]].t_min = min(layer31_list[layer31_combinations[i][0]].t_crit, layer31_list[layer31_combinations[i][0]].t_crit)
        layer31_list[layer31_combinations[i][0]].t_max = max(layer31_list[layer31_combinations[i][0]].t_crit, layer31_list[layer31_combinations[i][0]].t_crit)
               
        prev_rel = 100000000
        for t in range(int(layer31_list[layer31_combinations[i][0]].t_min - 60), int(layer31_list[layer31_combinations[i][0]].t_max + 60), 1):

            rel = layer31_list[layer31_combinations[i][0]].rel_dist(layer31_list[layer31_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer31_graph[layer31_combinations[i][0]][layer31_combinations[i][1]] = 1
                layer31_graph[layer31_combinations[i][1]][layer31_combinations[i][0]] = 1
                layer31_list[layer31_combinations[i][0]].overlap_count += 1
                layer31_list[layer31_combinations[i][1]].overlap_count += 1
                layer31_list[layer31_combinations[i][0]].overlap_friends.append(layer31_combinations[i][1])
                layer31_list[layer31_combinations[i][1]].overlap_friends.append(layer31_combinations[i][0])
                break

for i in range(len(layer32_combinations)):
    if layer32_list[layer32_combinations[i][0]].check_intersect(layer32_list[layer32_combinations[i][1]]) == True:
        
        crit = layer32_list[layer32_combinations[i][0]].get_intersect(layer32_list[layer32_combinations[i][1]])
        
        layer32_list[layer32_combinations[i][0]].t_min = min(layer32_list[layer32_combinations[i][0]].t_crit, layer32_list[layer32_combinations[i][0]].t_crit)
        layer32_list[layer32_combinations[i][0]].t_max = max(layer32_list[layer32_combinations[i][0]].t_crit, layer32_list[layer32_combinations[i][0]].t_crit)
        
        
        prev_rel = 100000000
        for t in range(int(layer32_list[layer32_combinations[i][0]].t_min - 60), int(layer32_list[layer32_combinations[i][0]].t_max + 60), 1):

            rel = layer32_list[layer32_combinations[i][0]].rel_dist(layer32_list[layer32_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer32_graph[layer32_combinations[i][0]][layer32_combinations[i][1]] = 1
                layer32_graph[layer32_combinations[i][1]][layer32_combinations[i][0]] = 1
                layer32_list[layer32_combinations[i][0]].overlap_count += 1
                layer32_list[layer32_combinations[i][1]].overlap_count += 1
                layer32_list[layer32_combinations[i][0]].overlap_friends.append(layer32_combinations[i][1])
                layer32_list[layer32_combinations[i][1]].overlap_friends.append(layer32_combinations[i][0])
                break

for i in range(len(layer33_combinations)):
    if layer33_list[layer33_combinations[i][0]].check_intersect(layer33_list[layer33_combinations[i][1]]) == True:
        
        crit = layer33_list[layer33_combinations[i][0]].get_intersect(layer33_list[layer33_combinations[i][1]])
        
        layer33_list[layer33_combinations[i][0]].t_min = min(layer33_list[layer33_combinations[i][0]].t_crit, layer33_list[layer33_combinations[i][0]].t_crit)
        layer33_list[layer33_combinations[i][0]].t_max = max(layer33_list[layer33_combinations[i][0]].t_crit, layer33_list[layer33_combinations[i][0]].t_crit)
        
        
        prev_rel = 100000000
        for t in range(int(layer33_list[layer33_combinations[i][0]].t_min - 60), int(layer33_list[layer33_combinations[i][0]].t_max + 60), 1):

            rel = layer33_list[layer33_combinations[i][0]].rel_dist(layer33_list[layer33_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer33_graph[layer33_combinations[i][0]][layer33_combinations[i][1]] = 1
                layer33_graph[layer33_combinations[i][1]][layer33_combinations[i][0]] = 1
                layer33_list[layer33_combinations[i][0]].overlap_count += 1
                layer33_list[layer33_combinations[i][1]].overlap_count += 1
                layer33_list[layer33_combinations[i][0]].overlap_friends.append(layer33_combinations[i][1])
                layer33_list[layer33_combinations[i][1]].overlap_friends.append(layer33_combinations[i][0])
                break
            
for i in range(len(layer41_combinations)):
    if layer41_list[layer41_combinations[i][0]].check_intersect(layer41_list[layer41_combinations[i][1]]) == True:
        
        crit = layer41_list[layer41_combinations[i][0]].get_intersect(layer41_list[layer41_combinations[i][1]])
        
        layer41_list[layer41_combinations[i][0]].t_min = min(layer41_list[layer41_combinations[i][0]].t_crit, layer41_list[layer41_combinations[i][0]].t_crit)
        layer41_list[layer41_combinations[i][0]].t_max = max(layer41_list[layer41_combinations[i][0]].t_crit, layer41_list[layer41_combinations[i][0]].t_crit)
        
        
        prev_rel = 100000000
        for t in range(int(layer41_list[layer41_combinations[i][0]].t_min - 60), int(layer41_list[layer41_combinations[i][0]].t_max + 60), 1):

            rel = layer41_list[layer41_combinations[i][0]].rel_dist(layer41_list[layer41_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer41_graph[layer41_combinations[i][0]][layer41_combinations[i][1]] = 1
                layer41_graph[layer41_combinations[i][1]][layer41_combinations[i][0]] = 1
                layer41_list[layer41_combinations[i][0]].overlap_count += 1
                layer41_list[layer41_combinations[i][1]].overlap_count += 1
                layer41_list[layer41_combinations[i][0]].overlap_friends.append(layer41_combinations[i][1])
                layer41_list[layer41_combinations[i][1]].overlap_friends.append(layer41_combinations[i][0])
                break

for i in range(len(layer42_combinations)):
    if layer42_list[layer42_combinations[i][0]].check_intersect(layer42_list[layer42_combinations[i][1]]) == True:
        
        crit = layer42_list[layer42_combinations[i][0]].get_intersect(layer42_list[layer42_combinations[i][1]])
        
        layer42_list[layer42_combinations[i][0]].t_min = min(layer42_list[layer42_combinations[i][0]].t_crit, layer42_list[layer42_combinations[i][0]].t_crit)
        layer42_list[layer42_combinations[i][0]].t_max = max(layer42_list[layer42_combinations[i][0]].t_crit, layer42_list[layer42_combinations[i][0]].t_crit)
        
        
        prev_rel = 100000000
        for t in range(int(layer42_list[layer42_combinations[i][0]].t_min - 60), int(layer42_list[layer42_combinations[i][0]].t_max + 60), 1):

            rel = layer42_list[layer42_combinations[i][0]].rel_dist(layer42_list[layer42_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer42_graph[layer42_combinations[i][0]][layer42_combinations[i][1]] = 1
                layer42_graph[layer42_combinations[i][1]][layer42_combinations[i][0]] = 1
                layer42_list[layer42_combinations[i][0]].overlap_count += 1
                layer42_list[layer42_combinations[i][1]].overlap_count += 1
                layer42_list[layer42_combinations[i][0]].overlap_friends.append(layer42_combinations[i][1])
                layer42_list[layer42_combinations[i][1]].overlap_friends.append(layer42_combinations[i][0])
                break

for i in range(len(layer43_combinations)):
    if layer43_list[layer43_combinations[i][0]].check_intersect(layer43_list[layer43_combinations[i][1]]) == True:
        
        crit = layer43_list[layer43_combinations[i][0]].get_intersect(layer43_list[layer43_combinations[i][1]])
        
        layer43_list[layer43_combinations[i][0]].t_min = min(layer43_list[layer43_combinations[i][0]].t_crit, layer43_list[layer43_combinations[i][0]].t_crit)
        layer43_list[layer43_combinations[i][0]].t_max = max(layer43_list[layer43_combinations[i][0]].t_crit, layer43_list[layer43_combinations[i][0]].t_crit)
        
        
        prev_rel = 100000000
        for t in range(int(layer43_list[layer43_combinations[i][0]].t_min - 60), int(layer43_list[layer43_combinations[i][0]].t_max + 60), 1):

            rel = layer43_list[layer43_combinations[i][0]].rel_dist(layer43_list[layer43_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer43_graph[layer43_combinations[i][0]][layer43_combinations[i][1]] = 1
                layer43_graph[layer43_combinations[i][1]][layer43_combinations[i][0]] = 1
                layer43_list[layer43_combinations[i][0]].overlap_count += 1
                layer43_list[layer43_combinations[i][1]].overlap_count += 1
                layer43_list[layer43_combinations[i][0]].overlap_friends.append(layer43_combinations[i][1])
                layer43_list[layer43_combinations[i][1]].overlap_friends.append(layer43_combinations[i][0])
                break

for i in range(len(layer44_combinations)):
    if layer44_list[layer44_combinations[i][0]].check_intersect(layer44_list[layer44_combinations[i][1]]) == True:
        
        crit = layer44_list[layer44_combinations[i][0]].get_intersect(layer44_list[layer44_combinations[i][1]])
        
        layer44_list[layer44_combinations[i][0]].t_min = min(layer44_list[layer44_combinations[i][0]].t_crit, layer44_list[layer44_combinations[i][0]].t_crit)
        layer44_list[layer44_combinations[i][0]].t_max = max(layer44_list[layer44_combinations[i][0]].t_crit, layer44_list[layer44_combinations[i][0]].t_crit)
        
        
        prev_rel = 100000000
        for t in range(int(layer44_list[layer44_combinations[i][0]].t_min - 60), int(layer44_list[layer44_combinations[i][0]].t_max + 60), 1):

            rel = layer44_list[layer44_combinations[i][0]].rel_dist(layer44_list[layer44_combinations[i][1]], t)
            
            if rel[2] > prev_rel:
                break
            prev_rel = rel[2]
            
            if rel[2] <= r:
                time_delay = r - rel[2]
                layer44_graph[layer44_combinations[i][0]][layer44_combinations[i][1]] = 1
                layer44_graph[layer44_combinations[i][1]][layer44_combinations[i][0]] = 1
                layer44_list[layer44_combinations[i][0]].overlap_count += 1
                layer44_list[layer44_combinations[i][1]].overlap_count += 1
                layer44_list[layer44_combinations[i][0]].overlap_friends.append(layer44_combinations[i][1])
                layer44_list[layer44_combinations[i][1]].overlap_friends.append(layer44_combinations[i][0])
                break

### ANALYSIS OF THE NETWORK
                
#### CENTRALIZED: GREEDY COLORING METHOD
#print("--------------------------------------------")
#print("CENTRALIZED: GRAPH COLORING METHOD")
#
#G = nx.from_numpy_array(graph)
#
#print("number of nodes, edges", nx.number_of_nodes(G), nx.number_of_edges(G))
#
#degree_list = []
#for i in G:
#    degree_list.append(G.degree(i))
#average_degree = sum(degree_list) / len(degree_list)
#max_degree = max(degree_list)
#print("average degree, max degree", average_degree, max_degree)
#print("Designated layers:")
#
#while graphColouring(m) == False:
#    n -= 1
#    graphColouring(m)
##print(altitude_list)
#
#unique, counts = np.unique(altitude_list, return_counts=True)
#print(dict(zip(unique, counts)))
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
#print(dlist)
unique2, counts2 = np.unique(dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

#print("--------------------------------------------")
#print("CENTRALIZED: EQUITABLE COLORING METHOD")
#e = nx.coloring.equitable_color(G, num_colors=max_degree+1)
#
## print(d)
#print("Using m =", max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#elist = []
#for x in e.values():
#    elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#unique69, counts69 = np.unique(elist, return_counts=True)
#print(dict(zip(unique69, counts69)))

print("--------------------------------------------")
print("--------------------------------------------")

### DECENTRALIZED (2-HEADING RESTRICTED)
print("--------------------------------------------")
print("DECENTRALIZED (2-HEADING RESTRICTED): GREEDY COLORING METHOD")
print("----- 0 <= ANGLE < 180 (90 <= HEADING < 270) -----")
layer21_G = nx.from_numpy_array(layer21_graph)
print("number of nodes, edges", nx.number_of_nodes(layer21_G), nx.number_of_edges(layer21_G))

layer21_degree_list = []
for i in layer21_G:
    layer21_degree_list.append(layer21_G.degree(i))
layer21_average_degree = sum(layer21_degree_list) / len(layer21_degree_list)
layer21_max_degree = max(layer21_degree_list)
print("average degree, eq layers", layer21_average_degree, layer21_max_degree+1)

layer21_d = nx.coloring.greedy_color(layer21_G)
layer21_dlist = []
for x in layer21_d.values():
    layer21_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer21_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

print("\n")
print("----- 180 <= ANGLE < 360 (270 <= HEADING < 90) -----")
layer22_G = nx.from_numpy_array(layer22_graph)
print("number of nodes, edges", nx.number_of_nodes(layer22_G), nx.number_of_edges(layer22_G))

layer22_degree_list = []
for i in layer22_G:
    layer22_degree_list.append(layer22_G.degree(i))
layer22_average_degree = sum(layer22_degree_list) / len(layer22_degree_list)
layer22_max_degree = max(layer22_degree_list)
print("average degree, eq layers", layer22_average_degree, layer22_max_degree+1)

layer22_d = nx.coloring.greedy_color(layer22_G)
layer22_dlist = []
for x in layer22_d.values():
    layer22_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer22_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

#print("--------------------------------------------")
#print("DECENTRALIZED (2-HEADING RESTRICTED): EQUITABLE COLORING METHOD")
#print("----- 0 <= ANGLE < 180 (90 <= HEADING < 270) -----")
#layer21_e = nx.coloring.equitable_color(layer21_G, num_colors=layer21_max_degree+1)
#
## print(d)
#print("Using m =", layer21_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer21_elist = []
#for x in layer21_e.values():
#    layer21_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer21_unique, layer21_counts = np.unique(layer21_elist, return_counts=True)
#print(dict(zip(layer21_unique, layer21_counts)))
#
#
#print("\n")
#print("----- 180 <= ANGLE < 360 (270 <= HEADING < 90) -----")
#layer22_e = nx.coloring.equitable_color(layer22_G, num_colors=layer22_max_degree+1)
#
## print(d)
#print("Using m =", layer22_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer22_elist = []
#for x in layer22_e.values():
#    layer22_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer22_unique, layer22_counts = np.unique(layer22_elist, return_counts=True)
#print(dict(zip(layer22_unique, layer22_counts)))

print("--------------------------------------------")
print("--------------------------------------------")

### DECENTRALIZED (3-HEADING RESTRICTED)
print("--------------------------------------------")
print("DECENTRALIZED (3-HEADING RESTRICTED): GREEDY COLORING METHOD")
print("----- 0 <= ANGLE < 120 (<= HEADING <) -----")
layer31_G = nx.from_numpy_array(layer31_graph)
print("number of nodes, edges", nx.number_of_nodes(layer31_G), nx.number_of_edges(layer31_G))

layer31_degree_list = []
for i in layer31_G:
    layer31_degree_list.append(layer31_G.degree(i))
layer31_average_degree = sum(layer31_degree_list) / len(layer31_degree_list)
layer31_max_degree = max(layer31_degree_list)
print("average degree, eq layers", layer31_average_degree, layer31_max_degree+1)

layer31_d = nx.coloring.greedy_color(layer31_G)
layer31_dlist = []
for x in layer31_d.values():
    layer31_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer31_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

print("\n")
print("----- 120 <= ANGLE < 240 (<= HEADING <) -----")
layer32_G = nx.from_numpy_array(layer32_graph)
print("number of nodes, edges", nx.number_of_nodes(layer32_G), nx.number_of_edges(layer32_G))

layer32_degree_list = []
for i in layer32_G:
    layer32_degree_list.append(layer32_G.degree(i))
layer32_average_degree = sum(layer32_degree_list) / len(layer32_degree_list)
layer32_max_degree = max(layer32_degree_list)
print("average degree, eq layers", layer32_average_degree, layer32_max_degree+1)

layer32_d = nx.coloring.greedy_color(layer32_G)
layer32_dlist = []
for x in layer32_d.values():
    layer32_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer32_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

print("\n")
print("----- 240 <= ANGLE < 360 (<= HEADING <) -----")
layer33_G = nx.from_numpy_array(layer33_graph)
print("number of nodes, edges", nx.number_of_nodes(layer33_G), nx.number_of_edges(layer33_G))

layer33_degree_list = []
for i in layer33_G:
    layer33_degree_list.append(layer33_G.degree(i))
layer33_average_degree = sum(layer33_degree_list) / len(layer33_degree_list)
layer33_max_degree = max(layer33_degree_list)
print("average degree, eq layers", layer33_average_degree, layer33_max_degree+1)

layer33_d = nx.coloring.greedy_color(layer33_G)
layer33_dlist = []
for x in layer33_d.values():
    layer33_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer33_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

#
#print("--------------------------------------------")
#print("DECENTRALIZED (3-HEADING RESTRICTED): EQUITABLE COLORING METHOD")
#print("----- 0 <= ANGLE < 120 (<= HEADING <) -----")
#layer31_e = nx.coloring.equitable_color(layer31_G, num_colors=layer31_max_degree+1)
#
## print(d)
#print("Using m =", layer31_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer31_elist = []
#for x in layer31_e.values():
#    layer31_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer31_unique, layer31_counts = np.unique(layer31_elist, return_counts=True)
#print(dict(zip(layer31_unique, layer31_counts)))
#
#
#print("\n")
#print("----- 120 <= ANGLE < 240 (<= HEADING <) -----")
#layer32_e = nx.coloring.equitable_color(layer32_G, num_colors=layer32_max_degree+1)
#
## print(d)
#print("Using m =", layer32_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer32_elist = []
#for x in layer32_e.values():
#    layer32_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer32_unique, layer32_counts = np.unique(layer32_elist, return_counts=True)
#print(dict(zip(layer32_unique, layer32_counts)))
#
#
#print("\n")
#print("----- 240 <= ANGLE < 360 (<= HEADING <) -----")
#layer33_e = nx.coloring.equitable_color(layer33_G, num_colors=layer33_max_degree+1)
#
## print(d)
#print("Using m =", layer33_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer33_elist = []
#for x in layer33_e.values():
#    layer33_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer33_unique, layer33_counts = np.unique(layer33_elist, return_counts=True)
#print(dict(zip(layer33_unique, layer33_counts)))

print("--------------------------------------------")
print("--------------------------------------------")

### DECENTRALIZED (4-HEADING RESTRICTED)
print("--------------------------------------------")
print("DECENTRALIZED (4-HEADING RESTRICTED): GREEDY COLORING METHOD")
print("----- 0 <= ANGLE < 90 (<= HEADING <) -----")
layer41_G = nx.from_numpy_array(layer41_graph)
print("number of nodes, edges", nx.number_of_nodes(layer41_G), nx.number_of_edges(layer41_G))

layer41_degree_list = []
for i in layer41_G:
    layer41_degree_list.append(layer41_G.degree(i))
layer41_average_degree = sum(layer41_degree_list) / len(layer41_degree_list)
layer41_max_degree = max(layer41_degree_list)
print("average degree, eq layers", layer41_average_degree, layer41_max_degree+1)

layer41_d = nx.coloring.greedy_color(layer41_G)
layer41_dlist = []
for x in layer41_d.values():
    layer41_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer41_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

print("\n")
print("----- 90 <= ANGLE < 180 (<= HEADING <) -----")
layer42_G = nx.from_numpy_array(layer42_graph)
print("number of nodes, edges", nx.number_of_nodes(layer42_G), nx.number_of_edges(layer42_G))

layer42_degree_list = []
for i in layer42_G:
    layer42_degree_list.append(layer42_G.degree(i))
layer42_average_degree = sum(layer42_degree_list) / len(layer42_degree_list)
layer42_max_degree = max(layer42_degree_list)
print("average degree, eq layers", layer42_average_degree, layer42_max_degree+1)

layer42_d = nx.coloring.greedy_color(layer42_G)
layer42_dlist = []
for x in layer42_d.values():
    layer42_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer42_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

print("\n")
print("----- 180 <= ANGLE < 270 (<= HEADING <) -----")
layer43_G = nx.from_numpy_array(layer43_graph)
print("number of nodes, edges", nx.number_of_nodes(layer43_G), nx.number_of_edges(layer43_G))

layer43_degree_list = []
for i in layer43_G:
    layer43_degree_list.append(layer43_G.degree(i))
layer43_average_degree = sum(layer43_degree_list) / len(layer43_degree_list)
layer43_max_degree = max(layer43_degree_list)
print("average degree, eq layers", layer43_average_degree, layer43_max_degree+1)

layer43_d = nx.coloring.greedy_color(layer43_G)
layer43_dlist = []
for x in layer43_d.values():
    layer43_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer43_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

print("\n")
print("----- 270 <= ANGLE < 360 (<= HEADING <) -----")
layer44_G = nx.from_numpy_array(layer44_graph)
print("number of nodes, edges", nx.number_of_nodes(layer44_G), nx.number_of_edges(layer44_G))

layer44_degree_list = []
for i in layer44_G:
    layer44_degree_list.append(layer44_G.degree(i))
layer44_average_degree = sum(layer44_degree_list) / len(layer44_degree_list)
layer44_max_degree = max(layer44_degree_list)
print("average degree, eq layers", layer44_average_degree, layer44_max_degree+1)

layer44_d = nx.coloring.greedy_color(layer44_G)
layer44_dlist = []
for x in layer44_d.values():
    layer44_dlist.append(x)
print("Designated layers:")
#print(dlist)
unique2, counts2 = np.unique(layer44_dlist, return_counts=True)
print(dict(zip(unique2, counts2)))

#print("--------------------------------------------")
#print("DECENTRALIZED (4-HEADING RESTRICTED): EQUITABLE COLORING METHOD")
#print("----- 0 <= ANGLE < 90 (<= HEADING <) -----")
#layer41_e = nx.coloring.equitable_color(layer41_G, num_colors=layer41_max_degree+1)
#
## print(d)
#print("Using m =", layer41_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer41_elist = []
#for x in layer41_e.values():
#    layer41_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer41_unique, layer41_counts = np.unique(layer41_elist, return_counts=True)
#print(dict(zip(layer41_unique, layer41_counts)))
#
#
#print("\n")
#print("----- 90 <= ANGLE < 180 (<= HEADING <) -----")
#layer42_e = nx.coloring.equitable_color(layer42_G, num_colors=layer42_max_degree+1)
#
## print(d)
#print("Using m =", layer42_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer42_elist = []
#for x in layer42_e.values():
#    layer42_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer42_unique, layer42_counts = np.unique(layer42_elist, return_counts=True)
#print(dict(zip(layer42_unique, layer42_counts)))
#
#
#print("\n")
#print("----- 180 <= ANGLE < 270 (<= HEADING <) -----")
#layer43_e = nx.coloring.equitable_color(layer43_G, num_colors=layer43_max_degree+1)
#
## print(d)
#print("Using m =", layer43_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer43_elist = []
#for x in layer43_e.values():
#    layer43_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer43_unique, layer43_counts = np.unique(layer43_elist, return_counts=True)
#print(dict(zip(layer43_unique, layer43_counts)))
#
#
#print("\n")
#print("----- 270 <= ANGLE < 360 (<= HEADING <) -----")
#layer44_e = nx.coloring.equitable_color(layer44_G, num_colors=layer44_max_degree+1)
#
## print(d)
#print("Using m =", layer44_max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#
#layer44_elist = []
#for x in layer44_e.values():
#    layer44_elist.append(x)
#print("Designated layers:")
##print(dlist)
#
#layer44_unique, layer44_counts = np.unique(layer44_elist, return_counts=True)
#print(dict(zip(layer44_unique, layer44_counts)))

print("Program took", time.time() - start_time, "seconds")
# winsound.Beep(880,3000)

#print(len(graph))
#unique, counts = np.unique(graph, return_counts=True)
#print(dict(zip(unique, counts)))



### NETWORKX GREEDY COLORING
#print("--------------------------------------------")
#print("DECENTRALIZED: COLORING METHOD VANILLA")
#d = nx.coloring.greedy_color(G) #,strategy='random_sequential'
## print(d)
##print("Using m =", max_degree + 1, "(max degree + 1)")
## equitable_sol_exists = nx.algorithms.coloring.equitable_coloring.is_equitable(G, d)
## print("Solution exists", equitable_sol_exists)
#dlist = []
#for x in d.values():
#    dlist.append(x)
#print("Designated layers:")
##print(dlist)
#unique2, counts2 = np.unique(dlist, return_counts=True)
#print(dict(zip(unique2, counts2)))



###################### SINGLE LAYER
#conflicting_drone = []
#
#while 1:
#    
#    is_any_conflict = False
#    
#    # for each drone
#    for i in range(len(combinations)):
#    #    print("Drone", combinations[i][0], "against", combinations[i][1], drone_list[combinations[i][0]].check_intersect(drone_list[combinations[i][1]]))
#        if drone_list[combinations[i][0]].check_intersect(drone_list[combinations[i][1]]) == True:
#            
#            crit = drone_list[combinations[i][0]].get_intersect(drone_list[combinations[i][1]])
#            print(combinations[i][0], combinations[i][1], "crit", crit)
#            
#            for t in range(int(drone_list[combinations[i][0]].t0), int(drone_list[combinations[i][0]].t1), 5):
#                rel = drone_list[combinations[i][0]].rel_dist(drone_list[combinations[i][1]], t)
#                print(combinations[i][0], combinations[i][1], "rel", rel)
#                if rel[2] <= r:
#                    time_delay = r - rel[2]
#                    print("^^^^^^^^^^^^^^^^^^^^^^^^^overlap detected^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
#                    conflicting_drone.append(combinations[i][1]) if combinations[i][1] not in conflicting_drone else conflicting_drone
#                    print(conflicting_drone)
#                    print("delay", time_delay)
#                    is_any_conflict = True
#
#
#
##                    break
##            break
#
#    
#    for n in conflicting_drone:
#        print(n)
#        drone_list[n].t0 += time_delay
#
#
#    break
#
##        if drone_list[combinations[i][1]].overlap_count > 0:
##            conflicting_drone.remove(combinations[i][1])
#    
#    
#    
#        
##    if is_any_conflict == False:
##        break
#
#for n in range(len(drone_list)):
#    print(n, drone_list[n].t0, drone_list[n].t1, drone_list[n].overlap_count, drone_list[n].overlap_friends)
###################### SINGLE LAYER



#for n in range(len(drone_list)):
#    print(n, drone_list[n].t0, drone_list[n].t1, drone_list[n].overlap_count, drone_list[n].overlap_friends)
#
#
#n = n_count
#while graphColouring(m) == False:
#    n -= 1
#    graphColouring(m)
#
#for (n, item) in enumerate(altitude_list, start=1):
#    print(n, item)
#    if item < 5:
#        pass
##        drone_list[n].overlap_count = 0
#    else:
#        print("AHHHHHHHHH", drone_list[n].overlap_friends)
#        for f in drone_list[n].overlap_friends:
#            print(f, drone_list[f].t0, drone_list[f].t1)
#            x = drone_list[f].t1
#        print(x)
#        drone_list[n].t0 = x
#
#while graphColouring(m) == False:
#    n -= 1
#    graphColouring(m)
#
#for (n, item) in enumerate(altitude_list, start=1):
#    print(n, item)
#    if item < 5:
#        pass
##        drone_list[n].overlap_count = 0
#    else:
#        print("AHHHHHHHHH", drone_list[n].overlap_friends)
#        for f in drone_list[n].overlap_friends:
#            print(f, drone_list[f].t0, drone_list[f].t1)
#        drone_list[n].t0 = drone_list[f].t1



#for n in range(len(altitude_list)):
#    drone_list[n].z = altitude_list[n]
#    print(n, drone_list[n].t0, drone_list[n].t1, drone_list[n].overlap_count, drone_list[n].overlap_friends)

#for n in range(len(drone_list)):
#    print(n, drone_list[n].t0, drone_list[n].t1, drone_list[n].overlap_count, drone_list[n].overlap_friends)




#plot_2d()
#plot_3d()
#
#for q in range(10):
#    drone_list.pop(0)
#n_count = len(drone_list)
#print(n_count)
#n = n_count

#print(altitude_list.count(1))
#print(altitude_list.count(2))




#activate_parameters()
#get_flight_info()
#check_overlap()
#assign_list()
#plot_2d()
#plot_3d()
#print_lists()




#activate_parameters()
#get_flight_info()

#### Checking overlaps pre-flight, sorted from submitted flight plans (using permutations)
#def check_overlap():
#    
#    global combinations
#    combinations = []
#    for comb in itertools.combinations((list(range(len(drone_list)))), 2):
#        combinations.append(comb)
#    print("-----Combination list", combinations)
#
#        
#    global false_count
#    false_count = 0
#    for i in range(len(combinations)):
#        print("Drone", combinations[i][0], "against", combinations[i][1], drone_list[combinations[i][0]].check_intersect(drone_list[combinations[i][1]]))
#        if drone_list[combinations[i][0]].check_intersect(drone_list[combinations[i][1]]) == True:
#            drone_list[combinations[i][0]].overlap_count += 1
#            drone_list[combinations[i][1]].overlap_count += 1
#        else:
#            false_count += 1
#        if false_count == len(combinations):
#            print("no overlapping")
#
#def assign_list():    
#    global overlap_list
#    global allowed_list
#    overlap_list = []
#    allowed_list = []
#    for n in range(len(drone_list)):
#        print("Drone", n, "overlap count", drone_list[n].overlap_count)
#        if drone_list[n].overlap_count > 0:
#            if len(altitude_levels) > 0:
#                overlap_list.append(drone_list[n])
#        else:
#            allowed_list.append(drone_list[n])
#            
#    overlap_list = sorted(overlap_list, key=operator.attrgetter('overlap_count'), reverse=True)
#    #for m in range(len(overlap_list)):
#    #    print(overlap_list[m].overlap_count, overlap_list[m].x0)
