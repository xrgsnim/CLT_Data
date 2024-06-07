

def get_new_weight(weights, priority):
    
    new_weight = []
    
    for i in range(len(weights)):
        if priority[i] != 0:
            weight = max(weights) + priority[i]
        else:
            weight = weights[i]
        
        new_weight.append(weight)
    
    return new_weight