

def get_new_weight(weights, priority):
    
    print('Update weight')
    print('Original weight : ', weights)
    print('Priority : ', priority)
    
    new_weight = []
    
    for i in range(len(weights)):
        if priority[i] != 0:
            weight = max(weights) + priority[i]
        else:
            weight = weights[i]
        
        new_weight.append(weight)
    
    print('New weight : ', new_weight , '\n')
    
    return new_weight