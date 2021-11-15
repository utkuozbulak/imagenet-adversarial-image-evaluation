import numpy as np

MODEL_LIST = ['alexnet', 'squeezenet', 'vgg16', 'resnet50', 'densenet','vit_base', 'vit_large']


def read_single_npy(loc):
    # Read a single transferability file
    transfer_dict = np.load(loc, allow_pickle=True).item()
    return transfer_dict


def get_m2m_transferability_data(file_loc, attack, model_list = MODEL_LIST):
    '''
    This function parses data for the model-to-model transferability matrix 
    '''
    # Define an empty transferability list which we will append invididual m2m transferability cases
    big_transfer_list = []
    for source_model in model_list:
        transfer_to = []
        for target_model in model_list:
            if source_model != target_model:
                # Read files
                file_name = attack + '_gen_from_' + source_model + '_trans_to_' + target_model + '.npy'
                transfer_file = read_single_npy(file_loc + '/' + attack + '/' + file_name)
                # How many adversarial examples achieved transferability from source to target model?
                transfer_to.append(len(transfer_file.keys()))
            else:
                # If the source and the target model is the same
                transfer_to.append(-1)
        big_transfer_list.append(transfer_to)
    return big_transfer_list
    

def get_transferability_cnt_for_each_source_image(file_loc, attack, model_list = MODEL_LIST):
    '''
    This function parses data for counting the model-to-model transferability for each source image
    '''
    # Define an empty dict for source image counts
    transfer_cnt_dict = {}
    for source_model in model_list:
        for target_model in model_list:
            if source_model != target_model:
                # Read files
                file_name = attack + '_gen_from_' + source_model + '_trans_to_' + target_model + '.npy'
                transfer_file = read_single_npy(file_loc + '/' + attack + '/' + file_name)
                # Get the names of the images that transferred
                source_images_that_transferred = list(transfer_file.keys())
                # Increment the count in the dictionary
                for im_name in source_images_that_transferred:
                    if im_name in transfer_cnt_dict:
                        transfer_cnt_dict[im_name] = transfer_cnt_dict[im_name] + 1
                    else:
                        transfer_cnt_dict[im_name] = 1
    return transfer_cnt_dict
    
    
def get_adv_perts(file_loc, attack, target_model, source_model_list = MODEL_LIST, pert_type = 'l2_pert'):
    '''
    This function parses data to get the perturbations of all adversarial examples that transferred to a target model
    '''
    # pert_type = 'l2_pert' or 'linf_pert'
    # Define an empty transferability list which we will append invididual m2m transferability cases
    big_pert_dict = {}
    for source_model in source_model_list:
        if source_model != target_model:
            # Read files
            file_name = attack + '_gen_from_' + source_model + '_trans_to_' + target_model + '.npy'
            transfer_file = read_single_npy(file_loc + '/' + attack + '/' + file_name)
            for key, value in transfer_file.items():
                big_pert_dict[key] = value[pert_type]
    return big_pert_dict


def save_to_file(file_name, list_to_write):
    '''
    To save fragile/hard images
    '''
    f = open(file_name, "w")
    for item in list_to_write:
        f.write('\''+item + '\',\n')
    f.close()
