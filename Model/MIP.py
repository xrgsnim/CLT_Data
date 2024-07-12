from docplex.mp.model import Model
import geometric_center as gm
import figure
import pandas as pd
import os
import re
import csv
import time


def mip_model(initial_container_file_path, new_container_file_path, m, h, max_diff, _level_num, M, _alpha, _beta, result_folder_path, ex_idx):
    
    model = Model(name = 'IP model')
    
    initial_container_df = pd.read_csv(initial_container_file_path)
    new_container_df = pd.read_csv(new_container_file_path)
    
    initial_container_weights = initial_container_df['weight'].tolist()
    new_container_weights = new_container_df['weight'].tolist()
    
    new_container_sequence = new_container_df['seq'].tolist()
    
    initial_container_group = initial_container_df['group'].tolist()
    new_container_group = new_container_df['group'].tolist()
    
    # initial_container_emerg = initial_container_df['emerg'].tolist()
    # new_container_emerg = new_container_df['emerg'].tolist()
    
    initial_container_size = initial_container_df['size(ft)'].tolist()
    new_container_size = new_container_df['size(ft)'].tolist()
    
    
    initial_container_num = len(initial_container_weights)
    new_container_num = len(new_container_weights)
    
    # total number of containers
    n = initial_container_num + new_container_num
    
    min_d = 0
    max_d = m - 1 + h - 1
    
    # Combine two list
    all_container_weights = initial_container_weights + new_container_weights

    initial_container_sequence = [0 for _ in range(initial_container_num)]
    all_container_seq = initial_container_sequence + new_container_sequence
    
    all_container_group = initial_container_group + new_container_group

    all_container_size = initial_container_size + new_container_size
    
    all_container_score = get_scroe_list(all_container_weights, all_container_group)
    ideal_config, centroid, container_level = gm.get_geometric_center(m, h, all_container_score, _level_num)
    
    print(' --------------- Start MIP model --------------- ')
    print(f'Number of initial container : {initial_container_num}')
    print(f'Number of new container : {new_container_num}')
    print(f'Total number of containers : {n}\n')
    
    # Decision Variables
    x = model.binary_var_dict([(i,j,k) for i in range(n) for j in range(m) for k in range(h)], lb = 0, ub = 1, name = 'x')
    r = model.binary_var_dict([(j,k) for j in range(m) for k in range(h)], lb = 0, ub = 1, name = 'r')

    d = model.continuous_var_dict([i for i in range(n)], lb = 0, name = 'd')
    d_x = model.continuous_var_dict([i for i in range(n)], lb = 0, name = 'd_x')
    d_y = model.continuous_var_dict([i for i in range(n)], lb = 0, name = 'd_y')

    # Constraints
    # Constraint 1 : Container i must be assigned to exactly one stack and one tier
    for i in range(n):
        model.add_constraint(sum(x[i,j,k] for j in range(m) for k in range(h)) == 1)

    # Constraint 2 : one slot can only have one container
    for j in range(m):
        for k in range(h):
            model.add_constraint(sum(x[i,j,k] for i in range(n)) <= 1)
        
    # constraint 3 : the hight of stack j must be less than or equal to h
    for j in range(m):
        model.add_constraint(sum(x[i,j,k] for k in range(h) for i in range(n)) <= h)
        
    # constraint 4 : you can't stack a container on slot k if there is no container on slot k-1
    for j in range(m):
        for k in range(h-1):
            model.add_constraint(sum(x[i,j,k] for i in range(n)) >= sum(x[i,j,k+1] for i in range(n)))
            
    # constraint 5 : define d_i
    for i in range(n):
        model.add_constraint(d[i] == d_x[i] + d_y[i])
        model.add_constraint(d_x[i] >= sum(x[i,j,k] * j for j in range(m) for k in range(h)) - centroid[container_level[i]][0])
        model.add_constraint(d_x[i] >= -(sum(x[i,j,k] * j for j in range(m) for k in range(h)) - centroid[container_level[i]][0]))
        model.add_constraint(d_y[i] >= sum(x[i,j,k] * k for j in range(m) for k in range(h)) - centroid[container_level[i]][1])
        model.add_constraint(d_y[i] >= -(sum(x[i,j,k] * k for j in range(m) for k in range(h)) - centroid[container_level[i]][1]))
        
        
    # # Constraint 6 : prevent peak stacks
    for j in range(m-1):
        model.add_constraint(sum(x[i,j,k] for k in range(h) for i in range(n)) - sum(x[i,j+1,k] for k in range(h) for i in range(n)) <= max_diff)
        model.add_constraint(sum(x[i,j,k] for k in range(h) for i in range(n)) - sum(x[i,j+1,k] for k in range(h) for i in range(n)) >= -max_diff)
            
        
    # Constraint 7 : define r_jk
    for j in range(m):
        for k in range(h-1):
            for _k in range(k+1, h):
                model.add_constraint((sum((all_container_score[i] * x[i,j,k]) for i in range(n)) - sum((all_container_score[i] * x[i,j,_k]) for i in range(n)))/ M <= (M * (1- sum(x[i,j,_k] for i in range(n)))) + r[j,k])
                
                model.add_constraint(r[j,k] <= (M * (1 - sum(x[i,j,_k] for i in range(n))))+ r[j,_k])            
                
                # Constraint : sequence
                model.add_constraint(sum(all_container_seq[i] * x[i,j,k] for i in range(n)) <= (M * (1 - sum(x[i,j,_k] for i in range(n)))) + sum(all_container_seq[i] * x[i,j,_k] for i in range(n)))
            
                
    for j in range(m):
        for k in range(h):
            model.add_constraint(sum(x[i,j,k] for i in range(n)) >= r[j,k])
            
        
    # Set Location of Initial Container
    for idx in range(initial_container_num):
        initial_container_idx = initial_container_df['idx'][idx] - 1
        loc_x = initial_container_df['loc_x'][idx] -1
        loc_z = initial_container_df['loc_z'][idx]
        # allocate location of initial container
        model.add_constraint(x[initial_container_idx, loc_x, loc_z] == 1)
        
    # Objective Function
    model.minimize(_alpha * sum(r[j,k] for j in range(m) for k in range(h)) + _beta * sum((d[i] - min_d) / (max_d - min_d) for i in range(n)))
    

    # print('------------------', 'Information of model', '------------------')
    # model.print_information()
    
    start_time = time.time()
    
    # Solve the model
    model_solution = model.solve()

    end_time = time.time()

    # Calculate and print the elapsed time
    elapsed_time = end_time - start_time
    print('Time taken to solve the MIP model : ', elapsed_time, ' seconds\n')    
    
    result = []

    if not os.path.exists(result_folder_path):
            os.makedirs(result_folder_path)
            print('Create Result Folder : ', result_folder_path)
            
    print('\n------------------', 'Solution', '------------------')
    if model_solution:
        print('I got a Solution')
        
        
        # save to text file
        solution_file_path = os.path.join(result_folder_path, f'Solution_ex{ex_idx}.txt')
        
        with open(solution_file_path, 'w') as f:
            f.write(f'Number of initial container : {initial_container_num}\n')
            f.write(f'Number of new container : {new_container_num}\n')
            f.write(f'Total number of containers : {n}\n')
            
            f.write(f'Level_num : {_level_num}\n')
            f.write(f'Container_level : {container_level}\n')
            f.write(f"ideal_configuration : \n {ideal_config}\n")
            f.write(f"Centroid : {centroid}\n")
            
            
            f.write(f"Repeat number : {ex_idx}\n")
            f.write(f'Original weight : {all_container_weights}\n')
            f.write(f'Group : {all_container_group}\n')
            f.write(f'Sequence : {all_container_seq}\n')
            # f.write(f'Emergency : {all_container_emerg}\n')
            f.write(f'Scroe : {all_container_score}\n')
            f.write(f"Time taken to solve the MIP model : {elapsed_time:.4f} seconds\n")
        
            f.write(f'min_d : {min_d}, max_d : {max_d}\n')

            f.write("---------------------------------\n")
            f.write(model.solution.to_string())

            for i in range(n):
                f.write(f'normalized distance of container {i} : {(d[i].solution_value - min_d) / (max_d - min_d)}\n')
                
        fig_container_info = []
        
        for i in range(n):
            for j in range(m):
                for k in range(h):
                    if x[i,j,k].solution_value >= 0.99:
                        container_original_weight = all_container_weights[i]
                        container_group = all_container_group[i]
                        container_score = all_container_score[i]
                        container_sequence = all_container_seq[i]
                        container_relocation = r[j,k].solution_value
                        container_size = all_container_size[i]
                        
                        fig_container_info.append((container_original_weight, j + 1, k))
                        
                        # Output data : container index, loc_x, loc_y, loc_z, weight, group, score, sequence, relocation, size(ft) 
                        result.append((i + 1 , j + 1, 0, k, container_original_weight, container_group, container_score, container_sequence, container_relocation, container_size))
                        
        
        # Save fig
        fig_file_path = os.path.join(result_folder_path, f'Configuration_ex{ex_idx}.png')
        
        figure.draw_figure(m, h, fig_container_info, fig_file_path)
                
    else:
        print('No solution found')
        
        # save to text file
        failed_file_path = os.path.join(result_folder_path, f'Failed_ex{ex_idx}.txt')

        with open(failed_file_path, 'w') as f:
            f.write("Can't find feasible solution\n\n")
            
            f.write(f'Number of initial container : {initial_container_num}\n')
            f.write(f'Number of new container : {new_container_num}\n')
            f.write(f'Total number of containers : {n}\n')
            
            f.write(f'Level_num : {_level_num}\n')
            f.write(f'Container_level : {container_level}\n')
            f.write(f"ideal_configuration : \n {ideal_config}\n")
            f.write(f"Centroid : {centroid}\n")
            
            f.write(f"Repeat number : {ex_idx}\n")
            f.write(f'Original weight : {all_container_weights}\n')
            f.write(f'Group : {all_container_group}\n')
            f.write(f'Sequence : {all_container_seq}\n')
            f.write(f'Scroe : {all_container_score}\n')
            f.write(f"Time taken to solve the MIP model : {elapsed_time:.4f} seconds\n")
            f.write("---------------------------------\n")
            
        print('Create Failed File')
        
    return result

def get_scroe_list(weights, _group):
    
    scores = []
    
    for i in range(len(weights)):
        weight = weights[i] + (_group[i] * 100)
        scores.append(weight)
    return scores
 
def get_input_file(_folder_path):
    # Read all csv file and divide by initial and new container
    initial_file_list = []
    new_file_list = []
    ex_num = []
        
    for file_name in os.listdir(_folder_path):
        if file_name.endswith('.csv'):
            if file_name.startswith('Initial'):
                initial_file_list.append(file_name)
            elif file_name.startswith('Container'):
                new_file_list.append(file_name)
            
                match = re.search(r'ex(\d{1,2})', file_name)
                if match:
                    ex_num.append(int(match.group(1)))

    # sort ex_num
    ex_num.sort()

    print('Done Read All CSV Files')
    print('Total Number of CSV Files : ', len(initial_file_list),'\n')
    return initial_file_list, new_file_list, ex_num

def save_output_file(_file_path, _result):
    
    with open(_file_path, 'w', newline='') as csvfile:
        
        fieldnames = ['idx', 'loc_x', 'loc_y', 'loc_z', 'weight', 'group', 'score', 'seq', 'reloc', 'size(ft)']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(len(_result)):
            idx = _result[i][0]
            loc_x = _result[i][1]
            loc_y = _result[i][2]
            loc_z = _result[i][3]
            weight = _result[i][4]
            group = _result[i][5]
            score = _result[i][6]
            sequence = _result[i][7]
            relocation = _result[i][8]
            size = _result[i][9]
            
            # Write row to CSV file
            writer.writerow({'idx': idx, 'loc_x': loc_x, 'loc_y': loc_y, 'loc_z': loc_z, 'weight': weight,
                                'group' : group, 'score' : score, 'seq' : sequence, 'reloc' : relocation, 'size(ft)': size})
        print('\n--------- Success Create Output Data ---------\n', _file_path ,'\n')

  
def main():
    
    # find all folders in folder_name
    initial_folder_list = os.listdir(input_folder)

    for _initial_folder in initial_folder_list:
        
        _new_folder_list = os.listdir(os.path.join(input_folder, _initial_folder))
        
        for _new_folder in _new_folder_list:
            
            input_folder_path = os.path.join(input_folder, _initial_folder, _new_folder)
            output_folder_path = os.path.join(output_folder, 'MIP', _initial_folder, _new_folder)
            
            print('Input Folder Path : ', input_folder_path)
            print('Output Folder Path : ', output_folder_path)


            initial_file_names, new_file_names, experiment_idx_list = get_input_file(input_folder_path)
            
            initial_file_num = len(initial_file_names)

            if initial_file_num != len(new_file_names):
                print('!!! Error : Check Data folder !!!')
            
            else:
                for alpha in alpha_list:
                    beta = 1 - alpha  
                    
                    result_folder_path_by_alpha = os.path.join(output_folder_path, f'alpha_{alpha}_beta_{beta}')          
                    
                    print('!!!!!! alpha : ', alpha)
                    
                    for file_idx in range(initial_file_num):
                        
                        initial_file = os.path.join(os.getcwd(), input_folder_path, initial_file_names[file_idx])
                        new_file = os.path.join(os.getcwd(), input_folder_path, new_file_names[file_idx])
                        experiment_idx = experiment_idx_list[file_idx]
                        # print(experiment_idx)
                        initial_file = os.path.join(os.getcwd(), input_folder_path, f'Initial_state_ex{experiment_idx}.csv')
                        new_file = os.path.join(os.getcwd(), input_folder_path, f'Container_ex{experiment_idx}.csv')
                                    
                        print('---------------- Info of Input Data ----------------')
                        print('File path of initial container : ', initial_file)
                        print('File path of new container : ', new_file)
                        print(f"Now repeat time : {experiment_idx}")
                        print(f"Result Folder : {result_folder_path_by_alpha}\n")               
                        
                        
                        output_file_path = os.path.join(result_folder_path_by_alpha, f'Configuration_ex{experiment_idx}.csv')
                        print('Output File Path : ', output_file_path, '\n')
                        # Check exist file in folder
                        if not os.path.exists(output_file_path):
                            model_result = mip_model(initial_file, new_file, stack_num, tier_num, peak_limit, level_num, Big_M, alpha, beta, result_folder_path_by_alpha, experiment_idx)
                            print('---------------- Done mip model ----------------')        
                            
                            if len(model_result) != 0:
                                # save solution to csv file
                                save_output_file(output_file_path, model_result)
                            
                            else:
                                print('!!! There is no solution !!!')        

                        else:
                            print('!!! Already exist output file !!!')
                            print(output_file_path, '\n')

stack_num = 6
tier_num = 5
peak_limit = 2
container_num = 25

input_folder = f'Grouped/Input_Data_{container_num}(stack_{stack_num}_tier_{tier_num})'
output_folder = f'Grouped/Output_Data_{container_num}(stack_{stack_num}_tier_{tier_num})'

# Big M
Big_M = 100

alpha_list = [0, 0.5, 1]

level_num = 9

# parent_folder_name = 'Grouped'


main()

# def main():
    
#     # find a`ll directories in parent_folder_name
#     sub_folder_list = os.listdir(parent_folder_name)

#     for sub_folder_name in sub_folder_list:

#         # If sub_folder_name contain 'Input'
#         if 'Input' in sub_folder_name:

#             input_folder = os.path.join(parent_folder_name, sub_folder_name)
            
#             # Remove input from sub_folder_name
#             output_folder_name = sub_folder_name.replace('Input', 'Output')
#             output_folder = os.path.join(parent_folder_name, output_folder_name)

#             # find all folders in folder_name
#             initial_folder_list = os.listdir(input_folder)

#             for initial_folder_name in initial_folder_list:
                
#                 _new_folder_list = os.listdir(os.path.join(input_folder, initial_folder_name))
                
#                 for _new_folder in _new_folder_list:
                    
#                     input_folder_path = os.path.join(input_folder, initial_folder_name, _new_folder)
#                     output_folder_path = os.path.join(output_folder, 'MIP', initial_folder_name, _new_folder)
                    
#                     print('Input Folder Path : ', input_folder_path)
#                     print('Output Folder Path : ', output_folder_path)

#                     initial_file_names, new_file_names, experiment_idx_list = get_input_file(input_folder_path)
                    
#                     initial_file_num = len(initial_file_names)

#                     if initial_file_num != len(new_file_names):
#                         print('!!! Error : Check Data folder !!!')
                    
#                     else:
#                         for alpha in alpha_list:
#                             beta = 1 - alpha  
                            
#                             result_folder_path_by_alpha = os.path.join(output_folder_path, f'alpha_{alpha}_beta_{beta}')          
                            
#                             print('!!!!!! alpha : ', alpha)
                            
#                             for file_idx in range(initial_file_num):
                                
#                                 initial_file = os.path.join(os.getcwd(), input_folder_path, initial_file_names[file_idx])
#                                 new_file = os.path.join(os.getcwd(), input_folder_path, new_file_names[file_idx])
#                                 experiment_idx = experiment_idx_list[file_idx]
#                                 # print(experiment_idx)
#                                 initial_file = os.path.join(os.getcwd(), input_folder_path, f'Initial_state_ex{experiment_idx}.csv')
#                                 new_file = os.path.join(os.getcwd(), input_folder_path, f'Container_ex{experiment_idx}.csv')
                                            
#                                 print('---------------- Info of Input Data ----------------')
#                                 print('File path of initial container : ', initial_file)
#                                 print('File path of new container : ', new_file)
#                                 print(f"Now repeat time : {experiment_idx}")
#                                 print(f"Result Folder : {result_folder_path_by_alpha}\n")               
                                
                                
#                                 output_file_path = os.path.join(result_folder_path_by_alpha, f'Configuration_ex{experiment_idx}.csv')
#                                 print('Output File Path : ', output_file_path, '\n')
#                                 # Check exist file in folder
#                                 if not os.path.exists(output_file_path):
#                                     model_result = mip_model(initial_file, new_file, stack_num, tier_num, peak_limit, level_num, Big_M, alpha, beta, result_folder_path_by_alpha, experiment_idx)
#                                     print('---------------- Done mip model ----------------')        
                                    
#                                     if len(model_result) != 0:
#                                         # save solution to csv file
#                                         save_output_file(output_file_path, model_result)
                                    
#                                     else:
#                                         print('!!! There is no solution !!!')        

#                                 else:
#                                     print('!!! Already exist output file !!!')
#                                     print(output_file_path, '\n')
                


# stack_num = 6
# tier_num = 5
# peak_limit = 2
# # container_num = 27

# # input_folder = f'Grouped/Input_Data_{container_num}(stack_{stack_num}_tier_{tier_num})'
# # output_folder = f'Grouped/Output_Data_{container_num}(stack_{stack_num}_tier_{tier_num})'

# # Big M
# Big_M = 100

# alpha_list = [0, 0.5, 1]

# level_num = 9

# parent_folder_name = 'Grouped'


# main()