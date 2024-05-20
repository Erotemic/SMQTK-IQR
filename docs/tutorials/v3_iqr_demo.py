# third version that uses the json manifest file to build data set and
# descriptor set
# Uses scriptconfig rather than argparse
# Modifying iqr_app_model_generation for geowatch

# Standard libraries
import glob
import logging
import os.path as osp
import os
import sklearn
import json
import os
import numpy as np

# SMQTK specific packages
import ubelt as ub
import scriptconfig as scfg
from smqtk_iqr.utils import cli
from smqtk_dataprovider import DataSet
from smqtk_dataprovider.impls.data_element.file import DataFileElement
from smqtk_descriptors.descriptor_element_factory import DescriptorElementFactory
from smqtk_descriptors import DescriptorSet
from smqtk_indexing import NearestNeighborsIndex
from smqtk_indexing import LshFunctor
from smqtk_core.configuration import (
    from_config_dict,
)

#---------------------------------------------------------------
# Define the configuration class using the scriptconfig package
# to process the cli arguments
class MyConfig(scfg.DataConfig):
    verbose = scfg.Value(False, isflag=True, short_alias=['v'], help='Output additional debug logging.')
    config = scfg.Value(None, required=True, short_alias=['c'], help=ub.paragraph(
            '''
            Path to the JSON configuration files. The first file
            provided should be the configuration file for the
            ``IqrSearchDispatcher`` web-application and the second
            should be the configuration file for the ``IqrService`` web-
            application.
            '''), nargs=2)
    metadata = scfg.Value(None, short_alias=['m'], help=ub.paragraph(
            '''
            Path to the JSON descriptor metadata files. Contains pairs of
            image and descriptor file paths.
            '''), nargs=1)
    tab = scfg.Value(None, required=True, short_alias=['t'], help=ub.paragraph(
            '''
            The configuration "tab" of the ``IqrSearchDispatcher``
            configuration to use. This informs what dataset to add the
            input data files to.
            '''))

#---------------------------------------------------------------
def remove_cache_files(ui_config, iqr_config) -> None:
    # Remove any existing cache files in data set config file path
    data_cache = ui_config['iqr_tabs']['Geowatch Chipped']['data_set']\
        ['smqtk_dataprovider.impls.data_set.memory.DataMemorySet']\
        ['cache_element']['smqtk_dataprovider.impls.data_element.file.DataFileElement']\
        ['filepath']
    # Deleting the file
    if os.path.exists(data_cache):
        os.remove(data_cache)
        print(f"\n File {data_cache} deleted successfully\n")
    else:
        print(f"File {data_cache} does not exist - will be generated")

    # Remove any existing cache files in descriptor set config file path
    descriptor_cache = iqr_config['iqr_service']['plugins']['descriptor_set']\
    ['smqtk_descriptors.impls.descriptor_set.memory.MemoryDescriptorSet']\
    ['cache_element']['smqtk_dataprovider.impls.data_element.file.DataFileElement']\
    ['filepath']

    # Deleting the file if it exists
    if descriptor_cache and os.path.exists(descriptor_cache):
        os.remove(descriptor_cache)
        print(f"File '{descriptor_cache}' deleted successfully")
    else:
        print(f"File '{descriptor_cache}' does not exist - will be generated")

#---------------------------------------------------------------
# Load metadata from the JSON file and generate data and descriptor sets
def generate_sets(manifest_path, data_set, descriptor_set, descriptor_elem_factory):
    # Load JSON data from the file
    with open(manifest_path, "r") as json_file:
        data = json.load(json_file)

    # Access the list of image-descriptor pairs
    image_descriptor_pairs = data['Image_Descriptor_Pairs']

    # Initialize an empty list to store descriptors for NNindex algorithm
    # Not sure if this is really needed
    descr_list = []

    # Iterate over each pair to build the data set and descriptor set
    for pair in image_descriptor_pairs:

        # Extract image path and descriptor path
        image_path = pair['image_path']
        image_path = osp.expanduser(image_path)

        desc_path = pair['desc_path']
        desc_path = osp.expanduser(desc_path)

        if osp.isfile(image_path) and osp.isfile(desc_path):
            data_fe = DataFileElement(image_path, readonly=True)
#            current_uuid = data_fe.uuid()
            data_set.add_data(data_fe)

            # Load the descriptor vector - it's a json file
            with open(desc_path, "rb") as f:
                json_vec = json.load(f)

            vector = np.array(json_vec)

            descriptor = descriptor_elem_factory.new_descriptor(data_fe.uuid())
            descriptor.set_vector(vector)
            descr_list.append(descriptor)

            # Add the descriptor to the descriptor set
            descriptor_set.add_descriptor(descriptor)
        else:
            print("\n Image or descriptor file paths not found")

    return data_set, descriptor_set, descr_list

#---------------------------------------------------------------
# A simple function to get the nth descriptor from the descriptor set
# Displays the UUID and vector of the descriptor
def get_nth_descriptor(descriptor_set, n):
    desc_iter = descriptor_set.descriptors()
    for i in range(n):
        desc = next(desc_iter)
    print(f"\nDescriptor {n} info, uuid: {desc.uuid()}, vector: {desc.vector()}")
    return desc



#---------------------------------------------------------------
def main() -> None:

    # Instantiate the configuration class and gather the arguments
    args = MyConfig.cli(special_options=False)

    #--------------------------------------------------------------
    ## setting up config values:
    ui_config_filepath, iqr_config_filepath = args.config
    llevel = logging.DEBUG if args.verbose else logging.INFO
    manifest_path = (args.metadata)[0]
    tab = args.tab

    # Not using `cli.utility_main_helper`` due to deviating from single-
    # config-with-default usage.
    cli.initialize_logging(logging.getLogger('smqtk_iqr'), llevel)
    cli.initialize_logging(logging.getLogger('__main__'), llevel)
    log = logging.getLogger(__name__)

    log.info("Loading UI config: '{}'".format(ui_config_filepath))
    ui_config, ui_config_loaded = cli.load_config(ui_config_filepath)
    log.info("Loading IQR config: '{}'".format(iqr_config_filepath))
    iqr_config, iqr_config_loaded = cli.load_config(iqr_config_filepath)
    if not (ui_config_loaded and iqr_config_loaded):
        raise RuntimeError("One or both configuration files failed to load.")

    # Ensure the given "tab" exists in UI configuration.
    if tab is None:
        log.error("No configuration tab provided to drive model generation.")
        exit(1)
    if tab not in ui_config["iqr_tabs"]:
        log.error("Invalid tab provided: '{}'. Available tags: {}"
                  .format(tab, list(ui_config["iqr_tabs"])))
        exit(1)

#    print("\n ui_config_filepath:", ui_config_filepath)
#    print("\n iqr_config_filepath:", iqr_config_filepath)
#    print("\n what is tab? ", tab)

    #----------------------------------------------------------------
    # Gather Configurations
    #
    log.info("Extracting plugin configurations")

    ui_tab_config = ui_config["iqr_tabs"][tab]
    iqr_plugins_config = iqr_config['iqr_service']['plugins']

    # Configure DataSet implementation and parameters
    data_set_config = ui_tab_config['data_set']

    # Configure DescriptorElementFactory instance, which defines what
    # implementation of DescriptorElement to use for storing generated
    # descriptor vectors below.
    descriptor_elem_factory_config = iqr_plugins_config['descriptor_factory']

#    print("\n Descriptor Element Config:", descriptor_elem_factory_config)

    # Configure the DescriptorSet instance into which the descriptor elements
    # are added.
    descriptor_set_config = iqr_plugins_config['descriptor_set']

#    print("\n Descriptor Set Config:", descriptor_set_config)

    # Configure NearestNeighborIndex algorithm implementation, parameters and
    # persistent model component locations (if implementation has any).
    nn_index_config = iqr_plugins_config['neighbor_index']

    #--------------------------------------------------------------
    # Remove any existing cache files in data set config file path
    remove_cache_files(ui_config, iqr_config)

    #---------------------------------------------------------------
    # Initialize data/algorithms
    #
    # Constructing appropriate data structures and algorithms, needed for the
    # IQR demo application, in preparation for model training.
    #

    log.info("Instantiating plugins")

    # Create instance of the class DataSet from the configuration
    data_set: DataSet = \
        from_config_dict(data_set_config, DataSet.get_impls())
    descriptor_elem_factory = DescriptorElementFactory \
        .from_config(descriptor_elem_factory_config)

#    print("\n Descriptor_elem_factory: ", descriptor_elem_factory)
#    factory_atts = vars(descriptor_elem_factory)
#    print("\n Descriptor_elem_factory attributes: ", factory_atts)

    # Create instance of the class DescriptorSet from the configuration
    descriptor_set: DescriptorSet = \
        from_config_dict(descriptor_set_config, DescriptorSet.get_impls())

#    print("\n Descriptor Set: ", descriptor_set)

    # Create instance of the class NearestNeighborsIndex from the configuration
    nn_index: NearestNeighborsIndex = \
       from_config_dict(nn_index_config, NearestNeighborsIndex.get_impls())

#    print("\n What does nnindex_config look like?", nn_index)

    # Generate data set and descriptor set from the JSON manifest file
    data_set, descriptor_set, descr_list =  \
        generate_sets(manifest_path, data_set, descriptor_set, descriptor_elem_factory)

#    print("\n View data set", data_set)
#    print("\nDescriptor list: ", descr_list)

    print("\nData set with {} elements created successfully".format(data_set.count()))
    print("\nDescriptor set with {} elements created successfully".format(descriptor_set.count()))
    print("\nDescriptor list with {} elements created successfully".format(descr_list.__len__()))
#    print("\n Descriptor Set after adding new descriptor:", descriptor_set)
#    dataset_attributes = vars(data_set)
#    print("\n what are the attributes of data_set?", dataset_attributes)
#    desc_set_attributes = vars(descriptor_set)
#    print("\n what are the attributes of descriptor_set?", desc_set_attributes)

    desc_test = get_nth_descriptor(descriptor_set, 4)

#    vec_list = descriptor_set.get_many_vectors(['b62bff3628864ed164c7727e67d13f9ca8d20aba', '9f8d18ebdb9952a3d0aaaa995b922a17f2a62459'])
#    print("\n Vector list:", vec_list)


    log.info("Building nearest neighbors index {}".format(nn_index))
    nn_index.build_index(descriptor_set)
    print("\nNearest Neighbors Index", nn_index)

#    atts_nnindex = vars(nn_index)
#    print("\n Nearest Neighbors Index attributes: ", atts_nnindex)

    nn_test = nn_index.nn(desc_test, 3)
    print("\nNearest Neighbors: ", nn_test)

#    atts_nnindex = vars(nn_index)
#    print("\n Nearest Neighbors Index attributes: ", atts_nnindex)




if __name__ == "__main__":
    main()
