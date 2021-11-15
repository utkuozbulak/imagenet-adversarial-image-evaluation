import copy
from matplotlib import colors
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Ubuntu"

from prep_data import get_transferability_cnt_for_each_source_image, save_to_file


def plt_transferability_cnt(data, attack):
    # Plot
    fig, ax = plt.subplots(figsize=(5,2.1))
    N, bins, patches = plt.hist(data,
                                bins=[x for x in range(1, 42)],
                                density=False,
                                histtype='bar',
                                color='whitesmoke',
                                edgecolor='black',
                                linewidth=1.5)
                                
    # Coloring
    fracs = N / N.max()
    # Normalize the data betwen 0 and 1
    # Below is purely aesthetics, play it according to your desire
    max_color_bar = fracs.max()+0.25
    min_color_bar = fracs.min()
    norm = colors.Normalize(min_color_bar, max_color_bar)
    max_color_bar = fracs.max()+0.3
    min_color_bar = fracs.min()+0.2
    # Set color for bars
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis_r(norm(thisfrac))
        thispatch.set_facecolor(color)
    
    # Axis labels
    plt.ylabel('Source image count', fontsize=10)
    plt.xlabel('$T(Θ, \widehat{\mathcal{{X}}}^{('+attack+')}, \mathcal{y})$', fontsize=11)
    
    # Enable grid
    ax.grid('--', axis='y', linewidth=0.25, alpha=0.75)
    # Ticks and limit
    ax.set_yticks([0, 500, 1000, 1500, 2000])
    plt.xlim([0.82, 41])
    plt.xticks([1.5, 10, 20, 30, 40], [1, 10, 20, 30, 40])
    
    # Save
    plt.savefig(attack+'_im_trans_cnt.png',
                dpi=500, bbox_inches='tight', pad_inches=0)



if __name__ == '__main__':
    # Get data
    attack = 'PGD'
    pgd_data = get_transferability_cnt_for_each_source_image('../data', attack)
    # Use only the values of the dict
    plt_transferability_cnt(list(pgd_data.values()), attack)
    
    # Get data
    attack = 'CW'
    cw_data = get_transferability_cnt_for_each_source_image('../data', attack)
    # Use only the values of the dict
    plt_transferability_cnt(list(cw_data.values()), attack)
    
    # Get data
    attack = 'MI-FGSM'
    mi_data = get_transferability_cnt_for_each_source_image('../data', attack)
    # Use only the values of the dict
    plt_transferability_cnt(list(mi_data.values()), attack)

    # Merge all attacks
    all_keys = []
    all_keys.extend(pgd_data.keys())
    all_keys.extend(cw_data.keys())
    all_keys.extend(mi_data.keys())
    all_keys = set(all_keys)
    
    merged_data = {}
    
    for key in all_keys:
        try:
            pgd_val = pgd_data[key]
        except:
            pgd_val = 0
        try:
            cw_val = cw_data[key]
        except:
            cw_val = 0
        try:
            mi_val = mi_data[key]
        except:
            mi_val = 0
        div = sum(x > 0 for x in [pgd_val, cw_val, mi_val])
        tot = sum([pgd_val, cw_val, mi_val])
        merged_data[key] = int(tot/div)

    # Visualize
    plt_transferability_cnt(list(merged_data.values()), 'A')
    
    # Fragile images: Transferability > 30
    fragile_images = copy.deepcopy(merged_data)
    for key in all_keys:
        if merged_data[key] < 30:
            del fragile_images[key]
    # save_to_file('fragile_images.py', fragile_images.keys())
    
    # Hard images: Transferability < 5
    hard_images = copy.deepcopy(merged_data)
    for key in all_keys:
        if merged_data[key] > 5:
            del hard_images[key]
    # save_to_file('hard_images.py', fragile_images.keys())
    