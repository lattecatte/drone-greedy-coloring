# DroneGreedyColoring
*[Used in my 2020 Thesis "Unmanned Traffic Management Deconflicting Using Greedy Coloring"]*

Multicopter collision simulation using the Greedy Coloring algorithm.

## Introduction
The objective of an unmanned traffic management (UTM) is to optimize the capacity of the high-density low-level 
uncontrolled airspace. One such method for optimization is to assign different vertical layers of altitude for 
unmanned aircraft systems (UAS) flight operations that are in conflict.</br>
This study aims to analyze the deconfliction of unmanned aircraft traffic management at the high-density low-level 
uncontrolled airspace by utilizing the vertical layer assignment method. This was done by modeling the airspace 
and generating random UAS flight operations and applying the greedy coloring algorithm to resolve conflicts 
between operations. We compare the cases for the single UTM architecture where operations are managed by one 
with one UTM service provider (UTMSP), to the federated UTM architecture where operations are split among 
multiple UTMSPs based on flight headings.

## Method
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

## Results
*Average numbers of conflicts per operation and number of layers needed*</br>
For all 60 simulations, the values for the average number of conflicts per operation were plotted in Figure 1(a). A 
non-linear decrease in the average number of conflicts per operation was observed as more UTMSPs were used due 
to the “spreading effect” and the “reduction of relative velocity effect”. The values for the number of layers needed 
were plotted in Figure 1(b).</br>
![image](https://github.com/lattecatte/DroneGreedyColoring/assets/154484150/315576bb-4485-406c-a3c3-5d263667c156)![image](https://github.com/lattecatte/DroneGreedyColoring/assets/154484150/064df05d-91f0-4fd4-a677-5e880d73b35f)</br>
###### **Figure 1**, Left: (a) Average numbers of conflicts per operation as a function of n and R</br>
###### Right: (b) Number of layers needed as a function of n and R</br>
Data for average number of conflicts per operation in Figure 1(a) was plotted against data for the number of layers needed in Figure 1(b), as shown by Figure 3(a). By observing the differences between the different UTM architectures, a tradeoff between the average number of conflicts per operation and number of layers needed can be observed as the number of UTMSPs vary.</br>
</br>
*Applying the 1% cut-off point*</br>
By observing the distribution of operations among the layers, it was found that some layers were occupied by a small number of operations, resulting in an excessive use of layers, as shown by the red circles in Figure 2(a). In the case of federated UTM architecture, the idea of a shared layer to combine all layers with number of operations less than a 1% cut-off percentage of the total number of operations in each service provider was proposed. The distribution after applying the 1% cut-off point is shown in Figure 2(b), and the number of layers needed were found to be reduced, as shown by the red arrow.</br>
![image](https://github.com/lattecatte/DroneGreedyColoring/assets/154484150/91cbbf70-8cef-40d5-8fc1-9a4112600c4f)![image](https://github.com/lattecatte/DroneGreedyColoring/assets/154484150/bd36f189-4395-4574-aae2-d8d834fdb0c6)</br>
**Figure 2**, Left: (a) Distribution of operations among layers as a function of n (R = 300 m)</br>
Right: (b) Distribution of operations among layers as a function of n (R = 300 m), adjusted to the 1% cut-off point</br>
The 1% cut-off point was applied to all simulations and the reduction of number of layers needed can be seen in Figure 3. In Figure 3(b), observations that were made were: a change in concentration of the operations, and the increase in effectiveness of the cut-off point as the number of UTMSPs increases, as shown by the red arrow.</br>
![image](https://github.com/lattecatte/DroneGreedyColoring/assets/154484150/31f32beb-608b-439b-9f99-66deb7188b56)![image](https://github.com/lattecatte/DroneGreedyColoring/assets/154484150/955463e8-175e-4f46-8128-4c13a5beeb2f)</br>
**Figure 3**, (a) Average number of conflicts per operation and number of layers needed,</br>
(b) Average number of conflicts per operation and number of layers needed, adjusted to 1% cut-off point</br>
For the range of the independent variables used, because the number of layers needed for all 60 simulations remained within the acceptable 20 layers for low-level uncontrolled airspace, the tradeoff could favor the federated UTM architecture’s more UTMSPs because the benefits of lower traffic caused by a lower average number of conflicts per operation could outweigh the extra number of layers needed. Furthermore, it was shown that the federated UTM architecture could additionally benefit from the 1% cut-off point.</br>

## Conclusion
One method for optimization of UTM in the high-density low-level airspace is the vertical layer assignment deconfliction method. Simulations of the airspace and operations were modeled as a network and the vertical layer assignment was solved through the greedy coloring algorithm. The average number of conflicts per operation, number of layers needed, and the distribution of operations among layers were analyzed as a function of number of operations n and conflict distance R between the single and federated UTM architectures. As more UTMSPs were used, a non-linear decrease of the average number of conflicts per operation was observed. A tradeoff between the average number of conflicts per operation and number of layers needed was also observed. It was found that the tradeoff could benefit the federated UTM architectures in the range of n and R used. In the case of federated UTM architectures, it was found that the number of layers needed can be reduced further by introducing the concept of a 1% cut-off point, where the effectiveness of the cut-off point increases as the number of UTMSPs increases.


