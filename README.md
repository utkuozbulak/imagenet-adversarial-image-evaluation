# ImageNet Adversarial Image Evaluation

This repository contains the code and some materials used in the experimental work presented in the following papers:

[1] [Selection of Source Images Heavily Influences Effectiveness of Adversarial Attacks](https://arxiv.org/abs/2106.07141) <br> British Machine Vision Conference (BMVC), 2021.

 
[2] [Evaluating Adversarial Attacks on ImageNet: A Reality Check on Misclassification Classes](https://arxiv.org/abs/2111.11056) <br> Conference on Neural Information Processing Systems (NeurIPS), Workshop on ImageNet: Past, Present, and Future, 2021.


## Fragile Source images

**Paper [1] TLDR**: A number of source images easily become *adversarial examples* with relatively low perturbation levels and achieve high model-to-model transferability successes compared to other source images.

In **src** folder, we shared a number of cleaned source code that can be used to generate the figures used in the paper with the usage of adversarial examples generated with PGD, CW, and MI-FGSM. You can download the data [here](https://www.dropbox.com/s/06vgoaqg5qu2fzr/data.zip?dl=0). Below are some of the visualizations used in the paper and their descriptions.

### Model-to-model transferability matrix
Model-to-model transferability matrix can be generated with the usage of <i> vis_m2m_transferability.py</i>. This visualization has two modes, an overview one where only the transfer success percentage is shown and a detailed view where both the absolute amount and the percentage is shown. The visualization for this experiment is given below:

<p align="center">
<img src="https://raw.githubusercontent.com/utkuozbulak/imagenet-adversarial-image-evaluation/master/vis_examples/PGD_True_PGD_m2m_trans_transferability_matrix.png" width="430" height="400">
</p>

### Source image transferability count

In the paper [1], we counted the model-to-model transferability of adversarial examples as they are generated from source images. This experiment can be reproduced with <i> vis_transferability_cnt.py</i>. The visualization for this experiment is given below:

<p align="center">
<img src="https://raw.githubusercontent.com/utkuozbulak/imagenet-adversarial-image-evaluation/master/vis_examples/PGD_im_trans_cnt.png" width="430" height="175">
</p>

### Perturbation distribution

In the paper [1], we counted the model-to-model transferability of adversarial examples as they are generated from source images. This experiment can be reproduced with <i> vis_transferability_cnt.py</i>. The visualization for this experiment is given below:

<p align="center">
<img src="https://raw.githubusercontent.com/utkuozbulak/imagenet-adversarial-image-evaluation/master/vis_examples/vit_base_PGD_pert.png" width="530" height="120">
</p>


## Untargeted misclassification for adversarial examples

**Paper [2] TLDR**: Adversarial examples that achieve untargeted model-to-model transferability are often misclassified into categories that are similar to the category of their origin.

<p align="center">
<img src="https://raw.githubusercontent.com/utkuozbulak/imagenet-adversarial-image-evaluation/master/vis_examples/collection_transferability.png" width="830" height="550">
</p>

We share the imagenet hierarchy used in the paper in the dictionary format in  <i>imagenet_hier.py</i>. 



## Citation
If you find the code in this repository useful for your research, consider citing our paper. Also, feel free to use any visuals available here.

    @inproceedings{ozbulak2021selection,
        title={Selection of Source Images Heavily Influences the Effectiveness of Adversarial Attacks},
        author={Ozbulak, Utku and Timothy Anzaku, Esla and De Neve, Wesley and Van Messem, Arnout},
        booktitle={British Machine vision Conference (BMVC)},
        year={2021}
    }
    
    @inproceedings{ozbulak2021evaluating,
      title={Evaluating Adversarial Attacks on ImageNet: A Reality Check on Misclassification Classes},
      author={Ozbulak, Utku and Pintor, Maura and Van Messem, Arnout and De Neve, Wesley},
      booktitle={NeurIPS 2021 Workshop on ImageNet: Past, Present, and Future},
      year={2021}
    }

## Requirements
```
python > 3.5
torch >= 0.4.0
torchvision >= 0.1.9
numpy >= 1.13.0
PIL >= 1.1.7
```
