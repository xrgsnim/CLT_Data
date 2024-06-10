from docplex.mp.model import Model
import geometric_center as gm
import UpdateWeight
import figure
import numpy as np

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
w = [10, 3.5, 4.54, 8.7, 9.9, 10.12]
# priority = [1,1,1,1,1]
priority = np.zeros(len(w))

new_weight = UpdateWeight.get_new_weight(w, priority)

# 1 to length of weight
sequence = np.arange(1, len(new_weight)+1)
# sequence = np.argsort(new_weight)[::-1]

size = [20 for i in range(len(w))]

# Number of Containers
n = len(w)

# Big M
M = 1000

# weight of objective function
alpha = 0.5
beta = 0.5

# Get Geometric centers
level_num = 9

centroid = gm.get_geometric_center(m, h, new_weight, level_num)
container_level = gm.get_level(new_weight, gm.div_level(new_weight, level_num))

print('Original weight : ', w)
print('Priority : ', priority)
print('sequence : ', sequence, '\n')

print('New weight : ', new_weight)
print('level_num : ', level_num)
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
    level = container_level[i - 1]
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
            model.add_constraint((sum((new_weight[i -1] * x[i,j,k]) for i in range(1, n+1)) - sum((new_weight[i -1] * x[i,j,_k]) for i in range(1, n+1)))/ M <= M * (1- sum(x[i,j,_k] for i in range(1, n+1))) + r[j,k])
            model.add_constraint(r[j,k] <= M * (1 - sum(x[i,j,_k] for i in range(1, n+1)))+ r[j,_k])            
            # Constraint : sequence
            model.add_constraint(sum(sequence[i -1] * x[i,j,k] for i in range(1, n+1)) <= M * (1 - sum(x[i,j,_k] for i in range(1, n+1))) + sum(sequence[i - 1] * x[i,j,_k] for i in range(1, n+1)))
            

for j in range(1, m+1):
    for k in range(h):
        model.add_constraint(sum(x[i,j,k] for i in range(1, n+1)) >= r[j,k])

# Objective Function
model.minimize(alpha * sum(r[j,k] for j in range(1, m+1) for k in range(h)) + beta * sum(d[i] for i in range(1, n+1)))

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
                if x[i,j,k].solution_value != 0:
                    print(x[i,j,k], ' = ', x[i,j,k].solution_value, ', weight : ',new_weight[i - 1], 'sequence : ', sequence[i-1], 'priority : ', priority[i-1], ', distance : ', d[i].solution_value, ', relocation : ', r[j,k].solution_value)
                    result.append((new_weight[i -1],j,k))
    print('-------------------------')
    # figure.draw_figure(m, h, result)
    figure.draw_figure_2(m, h, result)
    
else:
    print('No solution found')