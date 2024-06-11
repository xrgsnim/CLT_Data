from docplex.mp.model import Model
import geometric_center as gm
import UpdateWeight
import figure
import numpy as np
import pandas as pd

model = Model(name = 'IP model')

# Parameters

# Number of stacks
m = 6

# Capacity of tiers
h = 5

# limit of peak stacks
l = 2

# Weight of containers
# w = np.random.randint(1, 5, 10)
# w = [1,2,3,4,5,6,7,8,9,10]
# w = [3.5, 4.54, 8.7, 9.9, 10.12]
# w = [10, 3.5, 4.54, 8.7, 9.9, 10.12]
# # priority = [1,1,1,1,1]
# priority = np.zeros(len(w))


# # 1 to length of weight
# sequence = np.arange(1, len(new_weight)+1)
# # sequence = np.argsort(new_weight)[::-1]

# size = [20 for i in range(len(w))]

# Number of Containers
# n = len(w)

# Big M
M = 1000

# weight of objective function
alpha = 0.5
beta = 0.5

# Get Geometric centers
level_num = 9



def mip_model(initial_container_file_path, new_container_file_path, _stack_num, _tier_num, _level_num, Big_M, _alpha, _beta):

    initial_container_df = pd.read_csv(initial_container_file_path)
    new_container_df = pd.read_csv(new_container_file_path)
    
    initial_container_weights = initial_container_df['weight'].tolist()
    new_container_weights = new_container_df['weight'].tolist()
    
    new_container_priority = new_container_df['priority'].tolist()
    new_container_sequence = new_container_df['seq'].tolist()
    
    new_weight = UpdateWeight.get_new_weight(new_container_weights, new_container_priority)
    
    initial_container_num = len(initial_container_weights)
    new_container_num = len(new_container_weights)
    # total number of containers
    n = initial_container_num + new_container_num
    
    centroid = gm.get_geometric_center(_stack_num, _tier_num, new_weight, _level_num)
    container_level = gm.get_level(new_weight, gm.div_level(new_weight, _level_num))

    print('Original weight : ', new_container_weights)
    print('Priority : ', new_container_priority)
    print('sequence : ', new_container_sequence, '\n')

    print('New weight : ', new_weight)
    print('level_num : ', _level_num)
    print('container_level : ', container_level, '\n')

    # Decision Variables
    x = model.binary_var_dict([(i,j,k) for i in range(1, n+1) for j in range(1, m+1) for k in range(h)], lb = 0, ub = 1, name = 'x')
    r = model.binary_var_dict([(j,k) for j in range(1, m+1) for k in range(h)], lb = 0, ub = 1, name = 'r')

    d = model.continuous_var_dict([i for i in range(1, n+1)], lb = 0, name = 'd')
    d_x = model.continuous_var_dict([i for i in range(1, n+1)], lb = 0, name = 'd_x')
    d_y = model.continuous_var_dict([i for i in range(1, n+1)], lb = 0, name = 'd_y')

    # max_d = model.continuous_var(name = 'max_d')

    # Constraints
    # Constraint 1 : Container i must be assigned to exactly one stack and one tier
    for i in range(1, n+1):
        model.add_constraint(sum(x[i,j,k] for j in range(1, m+1) for k in range(h)) == 1)

    # Constraint 2 : one slot can only have one container
    for j in range(1, m+1):
        for k in range(h):
            model.add_constraint(sum(x[i,j,k] for i in range(1, n+1)) <= 1)
        
    # constraint 3 : the hight of stack j must be less than or equal to h
    for j in range(1, m+1):
        model.add_constraint(sum(x[i,j,k] for k in range(h) for i in range(1, n+1)) <= h)
        
    # constraint 4 : you can't stack a container on slot k if there is no container on slot k-1
    for j in range(1, m+1):
        for k in range(h-1):
            model.add_constraint(sum(x[i,j,k] for i in range(1, n+1)) >= sum(x[i,j,k+1] for i in range(1, n+1)))
            
    # constraint 5 : define d_i
    for i in range(1, n+1):
        level = container_level[i-1]
        model.add_constraint(d[i] == d_x[i] + d_y[i])
        model.add_constraint(d_x[i] >= sum(x[i,j,k] * j for j in range(1, m+1) for k in range(h)) - centroid[level][0])
        model.add_constraint(d_x[i] >= -(sum(x[i,j,k] * j for j in range(1, m+1) for k in range(h)) - centroid[level][0]))
        model.add_constraint(d_y[i] >= sum(x[i,j,k] * k for j in range(1, m+1) for k in range(h)) - centroid[level][1])
        model.add_constraint(d_y[i] >= -(sum(x[i,j,k] * k for j in range(1, m+1) for k in range(h)) - centroid[level][1]))
        

    # # Constraint 6 : prevent peak stacks
    for j in range(1, m):
        model.add_constraint(sum(x[i,j,k] for k in range(h) for i in range(1, n+1)) - sum(x[i,j+1,k] for k in range(h) for i in range(1, n+1)) <= l)
        model.add_constraint(sum(x[i,j,k] for k in range(h) for i in range(1, n+1)) - sum(x[i,j+1,k] for k in range(h) for i in range(1, n+1)) >= -l)
            
        
    # Constraint 7 : define r_jk
    for j in range(1, m+1):
        for k in range(h-1):
            for _k in range(k+1, h):
                model.add_constraint((sum((new_weight[i-1] * x[i,j,k]) for i in range(1, n+1)) - sum((new_weight[i-1] * x[i,j,_k]) for i in range(1, n+1)))/ Big_M <= Big_M * (1- sum(x[i,j,_k] for i in range(1, n+1))) + r[j,k])
                model.add_constraint(r[j,k] <= Big_M * (1 - sum(x[i,j,_k] for i in range(1, n+1)))+ r[j,_k])            
                # Constraint : sequence
                model.add_constraint(sum(new_container_sequence[i-1] * x[i,j,k] for i in range(1, n+1)) <= Big_M * (1 - sum(x[i,j,_k] for i in range(1, n+1))) + sum(new_container_sequence[i-1] * x[i,j,_k] for i in range(1, n+1)))
                
    for j in range(1, m+1):
        for k in range(h):
            model.add_constraint(sum(x[i,j,k] for i in range(1, n+1)) >= r[j,k])
            
    
    # Set Location of Initial Container
    for idx in range(initial_container_num):
        initial_container_idx = initial_container_df['idx'][idx]
        loc_x = initial_container_df['loc_x'][idx]
        loc_z = initial_container_df['loc_z'][idx]
        model.add_constraint(x[initial_container_idx, loc_x, loc_z] == 1)

    # Objective Function
    model.minimize(_alpha * sum(r[j,k] for j in range(1, m+1) for k in range(h)) + _beta * sum(d[i] for i in range(1, n+1)))

    print('------------------', 'Information of model', '------------------')
    model.print_information()
    # Solve the model
    solution = model.solve()

    print('\n------------------', 'Solution', '------------------')
    if solution:
        model.print_solution()
        
        result = []
        
        for i in range(1, n+1):
            for j in range(1, m+1):
                for k in range(h):
                    if x[i,j,k].solution_value >= 0.99:
                        container_original_weight = new_container_weights[i-1]
                        container_sequence = new_container_sequence[i-1]
                        container_priority = new_container_priority[i-1]
                        print(x[i,j,k], ' = ', x[i,j,k].solution_value, ', weight : ',container_original_weight, 'sequence : ', container_sequence, 'priority : ', container_priority, ', distance : ', d[i].solution_value, ', relocation : ', r[j,k].solution_value)
                        result.append((container_original_weight,j,k))
        print('-------------------------')
        figure.draw_figure_2(m, h, result)
        
    else:
        print('No solution found')