import matplotlib.pyplot as plt
import numpy as np
import os


def draw_figure(_column, _row, _data, _file_path):
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

    for weight, x, y in _data:
        plt.text(x, y, str(weight), color='black', fontsize=12, ha='center', va='center')
    
    plt.savefig(_file_path)
    plt.close()  # Close the figure to free memory