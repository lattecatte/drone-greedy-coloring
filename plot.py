import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D

def plot_2d():
    fig = plt.figure()
    ax = fig.gca()
    
#    for n in range(len(drone_list)):
    for n in range(10,20):
        start = ax.scatter(drone_list[n].x0, drone_list[n].y0, color=color_list[n])
        end = ax.scatter(drone_list[n].x1, drone_list[n].y1, color=color_list[n])
        vol_horizontal = ax.plot(*drone_list[n].vol_horizontal.exterior.xy, color=color_list[n])
        ax.text(drone_list[n].x0, drone_list[n].y0, n, color=color_list[n], size=14)
        ax.text(drone_list[n].x0, drone_list[n].y0, ("%.2f" % drone_list[n].t0), color=color_list[n], size=10, horizontalalignment='left', verticalalignment='top')
        ax.text(drone_list[n].x1, drone_list[n].y1, ("%.2f" % drone_list[n].t1), color=color_list[n], size=10, horizontalalignment='left', verticalalignment='top')
        crit_point = ax.scatter(crit[0], crit[1])

def plot_3d():
    fig = plt.figure()
    ax = fig.gca(projection="3d")
    
    for n in range(len(allowed_list)):
        start_ground = ax.scatter(allowed_list[n].x0, allowed_list[n].y0, 0, color=color_list[n])
        start_alt = ax.scatter(allowed_list[n].x0, allowed_list[n].y0, allowed_list[n].z, color=color_list[n])
        end_alt = ax.scatter(allowed_list[n].x1, allowed_list[n].y1, allowed_list[n].z, color=color_list[n])
        end_ground = ax.scatter(allowed_list[n].x1, allowed_list[n].y1, 0, color=color_list[n], s=100)
        
        line_takeoff = ax.plot((allowed_list[n].x0, allowed_list[n].x0), (allowed_list[n].y0, allowed_list[n].y0), zs=(0, allowed_list[n].z), color=color_list[n])
        line_AB = ax.plot((allowed_list[n].x0, allowed_list[n].x1), (allowed_list[n].y0, allowed_list[n].y1), zs=(allowed_list[n].z), color=color_list[n])
        line_landing = ax.plot((allowed_list[n].x1, allowed_list[n].x1), (allowed_list[n].y1, allowed_list[n].y1), zs=(allowed_list[n].z, 0), color=color_list[n])
    
        vol_takeoff = ax.plot(*allowed_list[n].vol_takeoff.exterior.xy, zs=0, color="k")
        vol_landing = ax.plot(*allowed_list[n].vol_landing.exterior.xy, zs=0, color="k")
#        vol_horizontal_top = ax.plot(*allowed_list[n].vol_horizontal.exterior.xy, zs=allowed_list[n].z + safedist_vertical, color=color_list[n])
#        vol_horizontal_bottom = ax.plot(*allowed_list[n].vol_horizontal.exterior.xy, zs=allowed_list[n].z - safedist_vertical, color=color_list[n])
        vol_horizontal= ax.plot(*allowed_list[n].vol_horizontal.exterior.xy, zs=allowed_list[n].z, color=color_list[n])
 
        anno_str = str(allowed_list[n].number)
        anno_str += ","
        anno_str += str(allowed_list[n].z)
        ax.text(allowed_list[n].x0, allowed_list[n].y0, allowed_list[n].z, anno_str, color="k", size=14)
        ax.text(allowed_list[n].x0, allowed_list[n].y0, allowed_list[n].z, ("%.2f" % allowed_list[n].t0), color=color_list[n], size=10, horizontalalignment='left', verticalalignment='top')
        ax.text(allowed_list[n].x1, allowed_list[n].y1, allowed_list[n].z, ("%.2f" % allowed_list[n].t1), color=color_list[n], size=10, horizontalalignment='left', verticalalignment='top')

    xmin, xmax = 0, max_range
    ymin, ymax = 0, max_range
    zmin, zmax = 0, m
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)
