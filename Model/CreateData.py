import saveCSV
import os
import random


# # Number of initial Container
# initial_con_num = 5

# # number of new container
# new_con_num = 10

# initial_con_num_list = [3, 5, 7]
# new_con_num_list = [10, 15, 20]
#--------------------------------------------
# repeat time
repeat_num = 15

# initial_con_num_list = [5, 10, 15]
# new_con_num_list = [10, 15, 20]

initial_con_num_list = [0, 3, 5, 7]
new_con_num_list = [10, 13, 15, 20]

stack_num = 6
tier_num = 5
initial_con_start_idx = 1

def get_priority(_priority_list, container_num):
    
    container_priority = []
    
    for i in range(container_num):
        # random choice in _priority_list
        priority = random.choice(_priority_list)
        
        if priority != 0:
            # remove priority from _priority_list
            _priority_list.remove(priority)
        
        container_priority.append(priority)
        
    return container_priority, _priority_list
        
    
    

def get_random_data(repeat_num, initial_con_num_list, new_con_num_list, stack_num, tier_num, initial_container_start_idx):
    if len(initial_con_num_list) ==  0 or len(new_con_num_list) == 0:
        print('Error : Check initial_con_num or new_con_num_list')
    else:    
        for initial_con_num in initial_con_num_list:
            for new_con_num in new_con_num_list:
                
                new_con_start_idx = initial_container_start_idx + initial_con_num
                folderPath = 'Data/Initial_' + str(initial_con_num) + '/New_' + str(new_con_num) + '/Input'
                print('Folder Path : ', folderPath, '\n')
                
                # Check exist folder
                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)
                    print('Create Folder : ', folderPath, '\n')
                
                total_con_num = initial_con_num + new_con_num
                # 0 ~ total_container_num
                priority_list = [i for i in range(0, total_con_num + 1)]
        
                for repeat_num_idx in range(repeat_num):
                    
                    initial_container_name = 'Initial_state_ex' + str(repeat_num_idx + 1)
                    new_container_name = 'Container_ex' + str(repeat_num_idx + 1)
                    
                    print('--------- Start Create Input Data ---------')
                    print('Initial Container Number : ', initial_con_num, '\nNew Container Number : ', new_con_num)
                    
                    initial_con_priority, updated_priority_list = get_priority(priority_list, total_con_num)
                    
                    # Save Input Data for Initial Container
                    saveCSV.InitialContainerCSV(folderPath, initial_container_name, initial_container_start_idx, initial_con_num, stack_num, tier_num, initial_con_priority)
                    
                    new_con_priority, updated_priority_list = get_priority(updated_priority_list, total_con_num)
                    
                    # Save Input Data for New Container
                    saveCSV.NewContainerCSV(folderPath, new_container_name, new_con_start_idx, new_con_num, new_con_priority)


get_random_data(repeat_num, initial_con_num_list, new_con_num_list, stack_num, tier_num, initial_con_start_idx)
