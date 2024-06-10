import matplotlib.pyplot as plt
import numpy as np

def draw_figure(_column, _row, _data):
    # _column = _column -1
    # _row = _row -1
    plt.figure(figsize=(_column, _row))
    plt.imshow(np.ones((_column, _row)), cmap='Greys', origin='lower', extent=[0, _column, 0, _row], alpha=0.5)  # White background with grid at 0.5 intensity
    
    # plt.xlim(-0.5, _column)
    # plt.ylim(-0.5, _row)
    plt.xlim(0.5, _column)
    plt.ylim(-0.5, _row)
    
    # Set x-axis grid lines
    plt.xticks(np.arange(0.5, _column + 1, 1))
    # Set y-axis grid lines
    plt.yticks(np.arange(0.5, _row + 1, 1))
    plt.grid(True)
    
    # Hide tick labels
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
    

    concentrations = [i * 0.1 for i in range(1, len(_data) + 1)]
    
    # idx = 1
    for (idx, x, y), _alpha in zip(_data, concentrations):
        # plt.fill_between([x - 0.5, x + 0.5], y - 0.5, y + 0.5, color='blue', alpha=_alpha)
        plt.text(x, y, str(idx), color='black', fontsize=12, ha='center', va='center')
        # idx += 1
        # plt.scatter(x, y, marker='s', color = 'blue', alpha = _alpha, cmap='viridis', s=100)  # Plot colored square with concentration-based color
    plt.show()



def draw_figure_2(_column, _row, _data):
    # _row = _row - 1
    plt.figure(figsize=(_column, _row))
    plt.imshow(np.ones((_column, _row)), cmap='Greys', origin='lower', extent=[0, _column, 0, _row], alpha=0.5)  # White background with grid at 0.5 intensity
    
    plt.xlim(1.5, _column)
    plt.ylim(-0.5, _row)

    # Set x-axis grid lines
    plt.xticks(np.arange(0.5, _column + 1, 1))
    # Set y-axis grid lines
    plt.yticks(np.arange(0.5, _row + 1, 1))
    plt.grid(True)
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
    
    concentrations = [i * 0.1 for i in range(1, len(_data) + 1)]
    
    idx = 1
    # for (x, y), _alpha in zip(_data, concentrations):
    for (idx, x, y), _alpha in zip(_data, concentrations):
        # plt.fill_between([x - 0.5, x + 0.5], y - 0.5, y + 0.5, color='blue', alpha=_alpha)
        plt.text(x, y, str(idx), color='black', fontsize=12, ha='center', va='center')
        # idx += 1
        # plt.scatter(x, y, marker='s', color = 'blue', alpha = _alpha, cmap='viridis', s=100)  # Plot colored square with concentration-based color
    plt.show()