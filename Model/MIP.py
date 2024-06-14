from docplex.mp.model import Model
import geometric_center as gm
import UpdateWeight
import figure
import pandas as pd
import os
import re

model = Model(name = 'IP model')


def mip_model(initial_container_file_path, new_container_file_path, m, h, max_diff, _level_num, M, _alpha, _beta, result_folder_path, ex_idx):

    initial_container_df = pd.read_csv(initial_container_file_path)
    new_container_df = pd.read_csv(new_container_file_path)
    
    initial_container_weights = initial_container_df['weight'].tolist()
    new_container_weights = new_container_df['weight'].tolist()
    
    new_container_priority = new_container_df['priority'].tolist()
    new_container_sequence = new_container_df['seq'].tolist()
    
    initial_container_size = initial_container_df['size(ft)'].tolist()
    new_container_size = new_container_df['size(ft)'].tolist()
    
    initial_container_num = len(initial_container_weights)
    new_container_num = len(new_container_weights)
    # total number of containers
    n = initial_container_num + new_container_num

    # Combine two list
    initial_container_sequence = [0 for _ in range(initial_container_num)]
    all_container_sequence = initial_container_sequence + new_container_sequence
    
    initial_container_priority = initial_container_df['priority'].tolist()
    all_container_priority = initial_container_priority + new_container_priority
    
    all_container_weight = initial_container_weights + new_container_weights
    
    all_container_size = initial_container_size + new_container_size
    
    new_weight = UpdateWeight.get_new_weight(all_container_weight, all_container_priority)

    
    centroid = gm.get_geometric_center(m, h, new_weight, _level_num)
    container_level = gm.get_level(new_weight, gm.div_level(new_weight, _level_num))
    
    print(' --------------- Start MIP model --------------- ')
    print('Number of initial container : ', initial_container_num)
    print('Number of new container : ', new_container_num)
    print('Original weight : ', new_container_weights)
    print('Priority : ', new_container_priority)
    print('sequence : ', new_container_sequence, '\n')
    print('New weight : ', new_weight)
    print('level_num : ', _level_num)
    print('container_level : ', container_level, '\n')

    # Decision Variables
    x = model.binary_var_dict([(i,j,k) for i in range(1, n+1) for j in range(max_diff, m+1) for k in range(h)], lb = 0, ub = 1, name = 'x')
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
        model.add_constraint(sum(x[i,j,k] for k in range(h) for i in range(1, n+1)) - sum(x[i,j+1,k] for k in range(h) for i in range(1, n+1)) <= max_diff)
        model.add_constraint(sum(x[i,j,k] for k in range(h) for i in range(1, n+1)) - sum(x[i,j+1,k] for k in range(h) for i in range(1, n+1)) >= -max_diff)
            
        
    # Constraint 7 : define r_jk
    for j in range(1, m+1):
        for k in range(h-1):
            for _k in range(k+1, h):
                model.add_constraint((sum((new_weight[i-1] * x[i,j,k]) for i in range(1, n+1)) - sum((new_weight[i-1] * x[i,j,_k]) for i in range(1, n+1)))/ M <= M * (1- sum(x[i,j,_k] for i in range(1, n+1))) + r[j,k])
                model.add_constraint(r[j,k] <= M * (1 - sum(x[i,j,_k] for i in range(1, n+1)))+ r[j,_k])            
                # Constraint : sequence
                model.add_constraint(sum(new_container_sequence[i-1] * x[i,j,k] for i in range(1, n+1)) <= M * (1 - sum(x[i,j,_k] for i in range(1, n+1))) + sum(new_container_sequence[i-1] * x[i,j,_k] for i in range(1, n+1)))
                
    for j in range(1, m+1):
        for k in range(h):
            model.add_constraint(sum(x[i,j,k] for i in range(1, n+1)) >= r[j,k])
            
    
    # Set Location of Initial Container
    for idx in range(initial_container_num):
        initial_container_idx = initial_container_df['idx'][idx]
        loc_x = initial_container_df['loc_x'][idx]
        loc_z = initial_container_df['loc_z'][idx]
        # allocate location of initial container
        model.add_constraint(x[initial_container_idx, loc_x, loc_z] == 1)
        # allocate relocation of initial container
        model.add_constraint(r[loc_x, loc_z] == 0)
        
    
    # Objective Function
    model.minimize(_alpha * sum(r[j,k] for j in range(1, m+1) for k in range(h)) + _beta * sum(d[i] for i in range(1, n+1)))

    print('------------------', 'Information of model', '------------------')
    model.print_information()
    # Solve the model
    solution = model.solve()

    print('\n------------------', 'Solution', '------------------')
    if solution:
        model.print_solution()
        
        fig_container_info = []
        
        for i in range(1, n+1):
            for j in range(1, m+1):
                for k in range(h):
                    if x[i,j,k].solution_value >= 0.99:
                        container_original_weight = all_container_weight[i-1]
                        container_sequence = all_container_sequence[i-1]
                        container_priority = all_container_priority[i-1]
                        container_size = all_container_size[i-1]
                        container_relocation = r[j,k].solution_value
                        print(x[i,j,k], ' = ', x[i,j,k].solution_value, ', weight : ',container_original_weight, 'sequence : ', container_sequence, 'priority : ', container_priority, ', distance : ', d[i].solution_value, ', relocation : ', r[j,k].solution_value)
                        fig_container_info.append((container_original_weight, j, k))
                        # Output data : container index, loc_x, loc_y, loc_z, weight, sequence, priority, relocation, size(ft) 
                        # result.append((i, j, 0, k, container_original_weight, container_sequence, container_priority, container_relocation, container_size))
        print('-------------------------')
        # Save fig
        fig_file_path = result_folder_path + 'Configuration_ex' + str(ex_idx)
        figure.draw_figure(m, h, fig_container_info)
        
    else:
        print('No solution found')
 
 
def get_input_file(_folder_path):
    # Read all csv file and divide by initial and new container
    initial_file_list = []
    new_file_list = []
    ex_num = []
        
    for file_name in os.listdir(_folder_path):
        if file_name.startswith('Initial'):
            initial_file_list.append(file_name)
        elif file_name.startswith('Container'):
            new_file_list.append(file_name)
        
        match = re.search(r'ex(\d{1,2})', file_name)
        if match:
            ex_num.append(int(match.group(1)))

    print('Done Read All CSV Files\n')
    return initial_file_list, new_file_list, ex_num

def main():
    
    input_folder_path = folder_path + 'Input/'
    output_folder_path = folder_path + 'Ouput/'
    
    initial_file_names, new_file_names, experiment_idx = get_input_file(input_folder_path)
    # print('Initial files : ', initial_file_names, '\n', 'New files : ', new_file_names, '\n')

    initial_file_num = len(initial_file_names)
    
    if initial_file_num != len(new_file_names):
        print('!!! Error : Check Data folder !!!')
    
    else:
        for file_idx in range(initial_file_num):
            
            initial_file = folder_path + initial_file_names[file_idx]
            new_file = folder_path + new_file_names[file_idx]
            
            print('---------------- Info of Input Data ----------------')
            print('File path of initial container : ', initial_file)
            print('File path of new container : ', new_file, '\n')
            
            for alpha in alpha_list:
                beta = 1 - alpha            
                
                result_folder_path_by_alpha = output_folder_path + 'alpha_' + str(alpha) + '_beta_' + str(beta) + '/'
                mip_model(initial_file, new_file, stack_num, tier_num, peak_limit, level_num, Big_M, alpha, beta, result_folder_path_by_alpha, experiment_idx)

        
    
    
# Parameters
folder_path = 'Data/Initial_5/New_10/'

stack_num = 10
tier_num = 6
peak_limit = 2

# Big M
Big_M = 1000

# weight of objective function
# alpha = 0.5
# beta = 0.5

alpha_list = [0, 0.5, 1]

# Get Geometric centers
level_num = 9

main()
