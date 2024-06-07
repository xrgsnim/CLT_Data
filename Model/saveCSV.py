import csv
import os
# Create CSV file
def CreateCSV(folderpath, fileName, start_idx, sequences, piroritys, weights, sizes):
    # Column Name : idx,seq,priority,weight,size(ft)
    
    # Check exist folder
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    
    with open(os.path.join(folderpath, fileName + '.csv'), 'w', newline='') as csvfile:
        fieldnames = ['idx', 'seq', 'priority', 'weight', 'size(ft)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(len(sequences)):
            idx = start_idx + i
            seq = sequences[i]
            priority = piroritys[i]
            weight = weights[i]
            size = sizes[i]
            
            # Write row to CSV file
            writer.writerow({'idx': idx, 'seq': seq, 'priority': priority, 'weight': weight, 'size(ft)': size})
        