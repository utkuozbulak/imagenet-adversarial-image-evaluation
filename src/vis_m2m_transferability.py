import numpy as np

import matplotlib
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Ubuntu"

from prep_data import get_m2m_transferability_data


def plt_m2m_transferability(transfer_data, attack, vmax, total_ims, detailed_flag, file_name):
    # Define figure size
    fig, ax = plt.subplots(figsize=(5, 5))
    # Get color maps
    viridis_cmap = matplotlib.cm.viridis
    viridis_cmap.set_under(color='white')
    # Plot data
    plt.imshow(transfer_data, cmap=viridis_cmap, interpolation='nearest',vmin = 0, vmax = vmax)
    # Labels    
    plt.ylabel('('+attack+') Generated from', fontsize=15)
    plt.xlabel('Tested on', fontsize=15)
    # Tick labels
    ax.set_yticklabels(['', 'AlexNet', 'SqueezeNet', 'VGG-16', 'ResNet-50', 'Dense-121', 'ViT-B', 'ViT-L'], rotation=30, minor=False)
    ax.set_xticklabels(['', 'AlexNet', 'SqueezeNet', 'VGG-16', 'ResNet-50', 'Dense-121', 'ViT-B', 'ViT-L'], rotation=30, minor=False)
    # Numbers inside
    for i in range(len(transfer_data)):
        for j in range(len(transfer_data)):
            if i != j:
                percentage = transfer_data[i][j]/ total_ims
                if detailed_flag:
                    percentage = "{0:.01%}".format(percentage)
                    # Add detailed text                    
                    ax.text(j, i-0.2, str(transfer_data[i][j]), ha="center", va="center", color="white", fontsize=12)
                    ax.text(j, i+0.2, percentage, ha="center", va="center", color="white", fontsize=12)
                else:
                    percentage = "{0:.00%}".format(percentage)
                    # Add percentage text
                    ax.text(j, i, str(percentage), ha="center", va="center", color="white", fontsize=17)

    plt.savefig(attack + '_' + str(detailed_flag) + '_' + file_name + '_transferability_matrix.png',
                dpi=500, bbox_inches='tight', pad_inches=0)


if __name__ == '__main__':
    attack = 'PGD'
    # Get data
    trans_data = get_m2m_transferability_data('../data', attack)
    # Visualize only percentage data
    plt_m2m_transferability(trans_data, attack,
                            vmax=np.max(trans_data),
                            total_ims=19025,
                            detailed_flag=True,
                            file_name=attack+'_m2m_trans')
    # Visualize detailed data
    plt_m2m_transferability(trans_data, attack,
                            vmax=np.max(trans_data),
                            total_ims=19025,
                            detailed_flag=False,
                            file_name=attack+'_m2m_trans')