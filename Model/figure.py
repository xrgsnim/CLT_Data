import matplotlib.pyplot as plt
import numpy as np
import os


def draw_figure(_column, _row, _data, _file_path):
    
    plt.figure(figsize=(_column, _row))
    plt.imshow(np.ones((_row, _column)), cmap='Greys', origin='lower', extent=[0.5, _column + 0.5, -0.5, _row - 0.5], alpha=0.5)  # White background with grid at 0.5 intensity

    plt.xlim(0.5, _column + 0.5)    
    plt.ylim(-0.5, _row - 1)
    
    plt.xticks(np.arange(0.5, _column + 1, 1))
#     # Set y-axis grid lines
    plt.yticks(np.arange(0.5, _row, 1))
    plt.grid(True)
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)

    for weight, x, y in _data:
        plt.text(x, y, str(weight), color='black', fontsize=12, ha='center', va='center')
    
    # Add x-axis labels
    for i in range(1, _column + 1):
        plt.text(i, -0.75, str(i), color='black', fontsize=12, ha='center', va='center')

    # Add y-axis labels
    for j in range(_row):
        plt.text(0.25, j, str(j), color='black', fontsize=12, ha='center', va='center')

    # plt.show()
    plt.savefig(_file_path)
    plt.close()  # Close the figure to free memory
 
# # Example usage
# _column = 5
# _row = 4
# _data = [(5, 1, 0), (3, 2, 1), (7, 3, 2), (2, 4, 3)]  # (weight, x, y)
# _file_path = 'path/to/your/figure.png'

# draw_figure(_column, _row, _data, _file_path)
