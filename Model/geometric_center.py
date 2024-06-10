import numpy as np
import get_grid

locations = [(1,0), (1,1), (2,0), (1,2), (2,1), (3,0), (1,3), (2,2), (3,1), (4,0), (1,4), (2,3), (3,2), (4,1), (5,0),
             (2,4), (3,3), (4,2), (5,1), (6,0), (3,4), (4,3), (5,2), (6,1), (4,4), (5,3), (6,2), (5,4), (6,3), (6,4)]

def create_grid(stack_num, height_num, _levels, _locations):
    grid = np.zeros((height_num, stack_num))
    sorted_levels = sorted(_levels)
    
    for i in range(len(sorted_levels)):
        column_idx = _locations[i][0] - 1
        row_idx = height_num - _locations[i][1] - 1 
        
        grid[row_idx][column_idx] = sorted_levels[i]
    
    return grid
        
    
def div_level(_weights, _level_num):
    w_min = min(_weights)
    w_max = max(_weights)

    _level_range = []
    for l_c in range(1, _level_num +1):
        _level_range.append((w_min + (l_c -1) * ((w_max - w_min) / (_level_num - 1)), w_min + l_c * ((w_max - w_min) / (_level_num -1))))
    return _level_range

def get_level(_weights, _level_range):    
    _container_level = []
    for w_i in _weights:
        level_idx = 0
        for l_min, l_max in _level_range:
            level_idx += 1
            if w_i >= l_min and w_i < l_max:
                _container_level.append(level_idx)
    return _container_level  


def set_geometric_grid(stack_num, height_num, levels):
    grid = np.zeros((height_num, stack_num))
    
    # sort weights in increasing order
    sorted_levels = sorted(levels)
    
    # Height_idx : 0 ~ 4
    height_idx = height_num - 1
    stack_idx = 0
    now_stack_max_idx = stack_idx
    now_stack_min_idx = stack_idx
    now_height_max_idx = height_idx
    now_height_min_idx = height_idx
    
    for level_idx in range(len(sorted_levels)):
        now_level = sorted_levels[level_idx]
        # print('now_level : ', now_level)
        if stack_idx == 0:
            # print('stack_idx is 0')
            # print('height_idx : ', height_idx, 'stack_idx : ', stack_idx)
            
            grid[height_idx][stack_idx] = now_level
            
            if height_idx == now_height_min_idx :
                if now_height_min_idx != 0:
                    now_height_min_idx -= 1
                    
                if now_stack_max_idx != stack_num -1:
                    now_stack_max_idx += 1
                
                    # print('Update now_stack_max_idx : ', now_stack_max_idx)
                
                else:
                    now_height_max_idx -= 1
                    # print('Update now_height_max_idx : ', now_height_max_idx)
                    
                    if height_idx == now_height_min_idx:
                        now_stack_min_idx += 1
                        # print('Update now_stack_min_idx : ', now_stack_min_idx)
         
            stack_idx = now_stack_max_idx
            height_idx = now_height_max_idx


        
        else:
            # print('height_idx : ', height_idx, 'stack_idx : ', stack_idx)
            grid[height_idx][stack_idx] = now_level
            
            if stack_idx != now_stack_min_idx:
                stack_idx -= 1
                # print('Update stack_idx : ', stack_idx)
    
            if height_idx != now_height_min_idx:
                height_idx -= 1              
                # print('Update height_idx : ', height_idx)
            
            else:    
                now_stack_min_idx += 1
                
                if now_stack_max_idx == stack_num - 1:
                    # print('now_stack_max_idx is max') 
                    now_height_max_idx -= 1
                else:
                    now_stack_max_idx += 1
                    # print('Update now_stack_max_idx : ', now_stack_max_idx)
                    
                stack_idx = now_stack_max_idx
                height_idx = now_height_max_idx          
    
    print('geometric grid by level \n', grid, '\n ------------------- \n')
    return grid


# get dictionary of geometric center
def get_geometric_dict(_grid):
    _dict = {}

    for _h in range(_grid.shape[0]):
        for _s in range(_grid.shape[1]):
            # stack : 1 ~ stack_num, height : 0 ~ tier_num - 1 
            location = (_s + 1, _grid.shape[0] - _h -1)
        
            if _grid[_h][_s] not in _dict.keys():
                # _dict[_grid[_h][_s]] = [(_h + 1, _s +1)]
                # print(_s, _h, _grid.shape[0], _grid.shape[1])
                _dict[_grid[_h][_s]] = [location]
                
            else:
                # append the same level
                # _dict[_grid[_h][_s]].append((_h +1, _s +1))
                _dict[_grid[_h][_s]].append(location)
                
    print('best locations \n', _dict, '\n')
    return _dict


# get geometric center
def get_geometric_center(_m, _h, _weights, _level_num):
    
    level_range = div_level(_weights, _level_num)
    print('level range : ', level_range, '\n')
    
    container_level = get_level(_weights, level_range)
    # geometric_grid = set_geometric_grid(_m, _h, container_level)
    geometric_grid = create_grid(_m, _h, container_level, locations)
    # geometric_grid = get_grid.place_containers_diagonally(container_level, _h, _m)
    print('geometric grid : \n', geometric_grid, '\n')
    geometric_dict = get_geometric_dict(geometric_grid)

    _geometric_center_dict = {}

    if len(_weights) == len(container_level):
        for c_l in container_level:
            x = 0
            y = 0
            for i in range(len(geometric_dict[c_l])):
                x += geometric_dict[c_l][i][0]
                y += geometric_dict[c_l][i][1]
            
            x_avg = x / len(geometric_dict[c_l])
            y_avg = y / len(geometric_dict[c_l])    
            _geometric_center_dict[c_l] = (x_avg, y_avg)
  
    else:
        print('There is a problem in dividing levels.')
        
    print('geometric_center : ', _geometric_center_dict, '\n')
    return _geometric_center_dict


# # Number of stacks
# m = 6

# # Capacity of tiers
# h = 5

# w = np.arange(1, 16)
# level_num = 9

# get_geometric_center(m, h, w, level_num)

