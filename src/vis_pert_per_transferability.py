import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Ubuntu"
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D

from prep_data import get_adv_perts, get_transferability_cnt_for_each_source_image


def filter_source_image(trans_data, pert_data, trans_cnt_filter):
    # Filter images from pert_data that have transferability less than trans_cnt_filter times 
    for key in trans_data:
        if trans_data[key] < trans_cnt_filter:
            try:
                del pert_data[key]
            except:
                pass


def next_100(num):
    # A helper function to determine the next number that ends with two zeros after the given number
    while num % 100 !=0:
        num = int(num) + 1
    return num


def plt_l2_histogram(list_to_vis, model_name, bins=[], y_axis=None, dense_factor = 92000, have_legend=False, attack='PGD'):
    # Define the plot
    fig, ax = plt.subplots(figsize=(6, 1.1))

    # Median line
    plt.axvline(x=np.median(list_to_vis), color='green', linewidth=3, alpha=0.8, ls='-')
    # Plot 25th and 75th percentile
    twentyfifth, seventyfifth = np.percentile(list_to_vis, [25, 75])
    plt.axvline(x=twentyfifth, color='red', linewidth=3, alpha=0.8, ls='-')
    plt.axvline(x=seventyfifth, color='blue', linewidth=3, alpha=0.8, ls='-')

    # If bins are given, use those bins, otherwise just plot with the appropriate bins
    if len(bins) == 0:
        counts, bins, patches = plt.hist(list_to_vis, edgecolor='black', linewidth=2, color='whitesmoke')
    else:
        counts, bins, patches = plt.hist(list_to_vis, edgecolor='black', bins=bins, linewidth=2, color='whitesmoke')

    # Set the ticks to be at the edges of the bins
    ax.set_xticks(bins)
    # Set the xaxis's tick labels to be formatted with 1 decimal place
    ax.xaxis.set_major_formatter(FormatStrFormatter('%0.0f'))

    # Find the upper limit of the chart dynamically
    ytop = next_100(max(counts)*1.1)
    plt.ylim([0, ytop])
    # Have only one ytick in the middle
    yticks = [0 , ytop/2, ytop]
    ax.set_yticks(yticks)

    # Y label
    plt.ylabel('Image\ncount', fontsize=14)
    ax.xaxis.set_label_coords(0.5, -0.25)
    # X label
    plt.xlabel('$d_{2}(\mathcal{x}, \widehat{\mathcal{X}}^{('+attack+')})$', fontsize=14)
    # Grid
    ax.grid(axis='y', linewidth=0.25)
    
    # Depending on have_legend variable, the chart will either have legend or not
    if have_legend:
        # Legend for the percentiles
        custom_lines = [Line2D([0], [0], color='red', lw=1, ls ='-'),
                        Line2D([0], [0], color='green', lw=1, ls ='-'),
                        Line2D([0], [0], color='blue', lw=1, ls ='-')]
        legend1=plt.legend(custom_lines, ["25th percentile",
                                          'Median',
                                          '75th percentile'],
                               framealpha=0.5, handlelength=1.5, loc=1, fontsize=8)
        legend1.get_frame().set_edgecolor('black')
        plt.gca().add_artist(legend1)

    plt.savefig(model_name +'_'+attack+'_pert.png', dpi=500, bbox_inches='tight', pad_inches=0)
    return bins


if __name__ == '__main__':
    attack = 'PGD'
    model = 'vit_base'
    # Get transferability data
    transferability_data = get_transferability_cnt_for_each_source_image('../data', 'PGD')
    # Get perturbation data
    pert_data = get_adv_perts('../data', attack, model)
    
    # Use all source images
    pert_data_as_list = list(pert_data.values())
    plt_l2_histogram(pert_data_as_list, model, [], y_axis= [0, 500, 1000, 1500, 2000], dense_factor = 5000, have_legend = True, attack=attack)
    # Changing L2 hist to Linf is trivial, just change the limits and anumbers appropriately

    # Use source images that transferred more than 20 times with PGD
    filter_source_image(transferability_data, pert_data, 30)
    pert_data_as_list = list(pert_data.values())
    plt_l2_histogram(pert_data_as_list, model, [], y_axis= [0, 500, 1000, 1500, 2000], dense_factor = 5000, have_legend = True, attack=attack)
    # In the paper, we did not filter for each attack but used the average transferability for all attacks
