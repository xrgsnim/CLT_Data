import saveCSV
import random


# repeat time
repeat_num = 3

# Number of initial Container
initial_con_num = 5

# number of new container
new_con_num = 10

size = [20 for _ in range(new_con_num)]

priority_group_num = 5

for repeat_num_idx in range(repeat_num):
    # random initial Container
    
    initial_con_num = 5
    folderPath = 'C:/Users/USER/workspace/CLT_Data/Data/Container_' + str(new_con_num) + '/' + 'Initial_' + str(initial_con_num) + '/Input'
    fileName = 'Container_ex' + str(repeat_num_idx + 1)
    
    # random sequence : 1 ~ new_con_num 
    sequence = random.sample(range(1, new_con_num + 1), new_con_num)
    
    # random priority 0 ~ 5
    priority = random.choices(range(0, priority_group_num + 1), k = new_con_num)

    # random weight from 2.96 to 24.0 with up to 2 decimal places
    weight = [round(random.uniform(2.96, 24.0), 2) for i in range(new_con_num)]

    saveCSV.CreateCSV(folderPath, fileName, 0, sequence, priority, weight, size)
    
    print('--------- Success Create Input Data : ', fileName ,'---------')