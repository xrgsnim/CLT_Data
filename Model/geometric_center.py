import numpy as np


# Number of stacks
m = 6

# Capacity of tiers
h = 5

# w = [1, 2, 3, 4, 5, 6, 7, 8, 9]
w = [9, 8, 7, 6, 5, 4, 3, 2, 1]

level_num = 9

# Create h by m grid
# def set_geometric_center(stack, height, levels):
#     grid = np.zeros((height, stack))
    
#     # sort weights in increasing order
#     sorted_levels = sorted(levels)
#     print(sorted_levels)
    
#     height_idx = height - 1
#     height_bottom_idx = height - 1
#     stack_idx = 0
    
#     for level in sorted_levels:    
#         if height_idx == height_bottom_idx & stack_idx == 0:
#             if grid[height_idx][stack_idx] == 0:
#                 grid[height_idx][stack_idx] = level
#                 stack_idx += 1
                
#         elif height_idx == height_bottom_idx:
            

                
#     # for i in range(h):
#     #     for j in range(m):
#     #         grid[i][j] = m + i - j
#     return grid

def div_level(_weights, _level_num):
    w_min = min(_weights)
    w_max = max(_weights)
    print('level_num : ', _level_num)
    _level_range = []
    for l_c in range(1, _level_num +1):
        _level_range.append((w_min + (l_c -1) * ((w_max - w_min) / (_level_num - 1)), w_min + l_c * ((w_max - w_min) / (_level_num -1))))
    return _level_range

def get_level(_weights, _levels):    
    _container_level = []
    for w_i in _weights:
        level_idx = 0
        for l_min, l_max in _levels:
            level_idx += 1
            if w_i >= l_min and w_i < l_max:
                _container_level.append(level_idx)
    return _container_level  

set_geometric_center(6, 5, w)

# level_range = div_level(w, level_num)
# print(level_range)

# container_level = get_level(w, level_range)
# print(container_level)



# # set geometric conter
# def set_geometric_center(_stack, _height, _level_num):
#     # create matrix stack by height with zeros
#     _grid = np.zeros((_height, _stack))    

#     # for _h in range(_height):
#     #     now_max_level = _level_num - _h
#     #     for _s in range(_stack):
#     #         _grid[_h][_s] = now_max_level - _s
    
#     for _h in range(_height):
#         now_height_idx = _height - _h - 1
#         now_max_level = _stack + _h
#         # print('now_max_level : ', now_max_level)
#         if now_max_level <= _level_num:
#             for _s in range(_stack):
#                 # _grid[now_height_idx][_s] = now_max_level - _s 
#                 _grid[now_height_idx][_s] = _h + _s + 1             
                            
#     return _grid
    

# # get dictionary of geometric center
# def get_geometric_dict(_grid):
#     _dict = {}
#     for _h in range(_grid.shape[0]):
#         for _s in range(_grid.shape[1]):
#             location = (_s, _grid.shape[0] - _h -1)
        
#             if _grid[_h][_s] not in _dict.keys():
#                 # _dict[_grid[_h][_s]] = [(_h + 1, _s +1)]
#                 # print(_s, _h, _grid.shape[0], _grid.shape[1])
#                 _dict[_grid[_h][_s]] = [location]
                
#             else:
#                 # append the same level
#                 # _dict[_grid[_h][_s]].append((_h +1, _s +1))
#                 _dict[_grid[_h][_s]].append(location)
                
#     print(_dict)
#     return _dict





 


# # get geometric center
# def get_geometric_center(_m, _h, _weights, _level_num):
    
#     grid = set_geometric_center(_m, _h, _level_num)
#     print(grid)

#     geometric_dict = get_geometric_dict(grid)

#     _levels = div_level(_weights, _level_num)
#     print('standard of level : ', _levels)
     
#     _geometric_center = []
#     container_level = get_level(_weights, _levels)
#     if len(_weights) == len(container_level):
#             print('container_level : ',container_level)
            
#             for c_l in container_level:
#                 x = 0
#                 y = 0
#                 for i in range(len(geometric_dict[c_l])):
#                     x += geometric_dict[c_l][i][0]
#                     y += geometric_dict[c_l][i][1]
                
#                 x_avg = x / len(geometric_dict[c_l])
#                 y_avg = y / len(geometric_dict[c_l])    
#                 _geometric_center.append((x_avg, y_avg))
  
#     else:
#         print('There is a problem in dividing levels.')
#     print('geometric_center : ', _geometric_center)
#     return _geometric_center



# level_num = 9

# # set_geometric_center(m, h, level_num)
# get_geometric_center(m, h, w, level_num)