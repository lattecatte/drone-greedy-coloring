# DroneGreedyColoring
*[Used in my 2020 Thesis "Unmanned Traffic Management Deconflicting Using Greedy Coloring"]*

Multicopter collision simulation using the Greedy Coloring algorithm.

# Introduction
The objective of an unmanned traffic management (UTM) is to optimize the capacity of the high-density low-level 
uncontrolled airspace. One such method for optimization is to assign different vertical layers of altitude for 
unmanned aircraft systems (UAS) flight operations that are in conflict.</br>
This study aims to analyze the deconfliction of unmanned aircraft traffic management at the high-density low-level 
uncontrolled airspace by utilizing the vertical layer assignment method. This was done by modeling the airspace 
and generating random UAS flight operations and applying the greedy coloring algorithm to resolve conflicts 
between operations. We compare the cases for the single UTM architecture where operations are managed by one 
with one UTM service provider (UTMSP), to the federated UTM architecture where operations are split among 
multiple UTMSPs based on flight headings.

# Method
Python was used to model the airspace and operations. Operations were randomly generated in the airspace and 
allocated into UTMSPs based on their flight headings. For n number of operations, the minimum relative distances
between all combinations of two operations were calculated to determine whether they are smaller than the assigned 
conflict distance R or not at any given time. A simulation was performed for each combination of the independent 
variables n and R. Once a conflict arises, the operation that causes the conflict will be moved to a new vertical layer 
to resolve the conflict. Conflict data for all operations in a simulation was then modeled as a network in order to 
solve the vertical layer assignment problem by treating it as a graph coloring problem. The greedy coloring 
algorithm was used.</br>
60 simulations were performed by varying the independent variables number of operations n from 1000 to
10 000, and conflict distance R from 50 m to 300 m. The effects on average number of conflicts per operation, 
number of layers needed, and the distribution of operations among these layers were analyzed. The performance of 
different UTM architectures were compared against each other.

# Results
Average numbers of conflicts per operation and number of layers needed</br>
For all 60 simulations, the values for the average number of conflicts per operation were plotted in Figure 1(a). A 
non-linear decrease in the average number of conflicts per operation was observed as more UTMSPs were used due 
to the “spreading effect” and the “reduction of relative velocity effect”. The values for the number of layers needed 
were plotted in Figure 1(b).
![image](https://github.com/lattecatte/DroneGreedyColoring/assets/154484150/315576bb-4485-406c-a3c3-5d263667c156)![image](https://github.com/lattecatte/DroneGreedyColoring/assets/154484150/064df05d-91f0-4fd4-a677-5e880d73b35f)

