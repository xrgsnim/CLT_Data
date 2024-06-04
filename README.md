# CLT_Data
Input &amp; Output Data for MIP, Heuristic Algorithm

## Input Data
### File for Initial State
- Folder Path : '/Container_15/Initial_3/Input/Initial_state_ex1'
    - /Conatiner_ + total number of container + Initial_ + number of initial container/Input/
- Setting for file name : Initial_state_ex + experiment repeat number
    - ex ) Initial_state_ex1, ... , Initial_state_ex10
- idx : Index of container
- loc_x : x-axis of container
- loc_y : y-axis of container
    - Single bay : loc_y = 0
- loc_z : z-axis of container
- weight : Weight of container
    - Random number from 2.96 to 24.0 with up to 2 decimal places
- size(ft) : Size of container
    - Default value : 20
    
### File for New Container
- Folder Path : '/Container_15/Initial_3/Input/Container_ex1'
    - /Conatiner_ + total number of container + Initial_ + number of initial container/Input/
- Setting for file name : Container_ex + experiment repeat number
    - ex ) Container_ex1, ..., Container_ex10
- idx : Index of container
- seq : Sequence of container
    - seq has 1 to number of container
- priority : priority of container
    - priority has 0 to number of group(g)
- weight : Weight of container
    - Random number from 2.96 to 24.0 with up to 2 decimal places
- size(ft) : Size of container
    - Default value : 20

※ Require distinction between the initial state container index and the index of a new container 

[ Example ]
- Container index of initial state has from 1 to 9
- Index of new container has from 10 to 40

## Output Data
Data for initial and new Containers
- Folder Path : '/Container_15/Initial_3/Output/Congiguration_ex1'
    - /Conatiner_ + total number of container + Initial_ + number of initial container/Output/
- Setting for file name : Configuration_ex + experiment repeat number
- idx : Index of container
- loc_x : x-axis of container
- loc_y : y-axis of container
    - Single bay : loc_y = 0
- loc_z : z-axis of container
- weight : Weight of container
    - Random number from 2.96 to 24.0 with up to 2 decimal places
- size(ft) : Size of container
    - Default value : 20
