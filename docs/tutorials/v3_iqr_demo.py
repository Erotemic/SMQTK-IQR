# third version that uses the json manifest file to build data set and
# descriptor set
# Uses scriptconfig rather than argparse
# Modifying iqr_app_model_generation for geowatch

# Standard libraries
import argparse
import glob
import logging
import os.path as osp
import os
import sklearn


# SMQTK specific packages
import ubelt as ub
import scriptconfig as scfg
from smqtk_iqr.utils import cli
from smqtk_dataprovider import DataSet
from smqtk_dataprovider.impls.data_element.file import DataFileElement
from smqtk_descriptors.descriptor_element_factory import DescriptorElementFactory
from smqtk_descriptors import DescriptorGenerator
from smqtk_descriptors import DescriptorSet

from smqtk_indexing import NearestNeighborsIndex
from smqtk_core.configuration import (
    from_config_dict,
)


#debuggins/printing packages
import json
import os
from PIL import Image
import numpy as np


# Define the configuration class
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
    descriptors = scfg.Value(None, short_alias=['d'], help=ub.paragraph(
            '''
            Path to the JSON descriptor metadata files.TO DO...describe
            file format...
            '''), nargs=1)
    tab = scfg.Value(None, required=True, short_alias=['t'], help=ub.paragraph(
            '''
            The configuration "tab" of the ``IqrSearchDispatcher``
            configuration to use. This informs what dataset to add the
            input data files to.
            '''))
    input_files = scfg.Value(None, position=1, required=True, help=ub.paragraph(
            '''
            Shell glob to files to add to the configured data set.
            '''), nargs='+')

# Instantiate the configuration class
args = MyConfig.cli(special_options=False)

def main() -> None:

    # Extract the paths of the image files
    image_paths = args.input_files

    # Extract the value of the descriptors argument from the cli input
    descriptor_paths = args.descriptors
    manifest_path = descriptor_paths[0]



    ## setting up config values:
    ui_config_filepath, iqr_config_filepath = args.config
    llevel = logging.DEBUG if args.verbose else logging.INFO
    tab = args.tab

    # These are the input files, images that will be processed
    #TO DO: remove this line later
    input_files_globs = args.input_files

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

    # Configure DescriptorGenerator algorithm implementation, parameters and
    # persistent model component locations (if implementation has any).
    descriptor_generator_config = iqr_plugins_config['descriptor_generator']

#    print("\n Descriptor Generator Config:", descriptor_generator_config)

    # Configure the DescriptorSet implementation and parameters
    descriptor_set_config = iqr_plugins_config['descriptor_set']

#    print("\n Descriptor Set Config:", descriptor_set_config)

    # Configure NearestNeighborIndex algorithm implementation, parameters and
    # persistent model component locations (if implementation has any).
    nn_index_config = iqr_plugins_config['neighbor_index']

    #--------------------------------------------------------------
    # Remove any existing cache files in data sets
    cache_fp = ui_config['iqr_tabs']['Ten Butterflies']['data_set']\
        ['smqtk_dataprovider.impls.data_set.memory.DataMemorySet']\
        ['cache_element']['smqtk_dataprovider.impls.data_element.file.DataFileElement']\
        ['filepath']
    # Deleting the file
    if os.path.exists(cache_fp):
        os.remove(cache_fp)
        print(f"\n File {cache_fp} deleted successfully\n")
    else:
        print(f"File {cache_fp} does not exist")

    # Remove any existing cache files in descriptor set
    desc_cache = iqr_config['iqr_service']['plugins']['descriptor_set']\
    ['smqtk_descriptors.impls.descriptor_set.memory.MemoryDescriptorSet']\
    ['cache_element']['smqtk_dataprovider.impls.data_element.file.DataFileElement']\
    ['filepath']

    # Deleting the file if it exists
    if desc_cache and os.path.exists(desc_cache):
        os.remove(desc_cache)
        print(f"File '{desc_cache}' deleted successfully")
    else:
        print(f"File '{desc_cache}' does not exist")
    #---------------------------------------------------------------
    # Initialize data/algorithms
    #
    # Constructing appropriate data structures and algorithms, needed for the
    # IQR demo application, in preparation for model training.
    #

    log.info("Instantiating plugins")

    # Creates instance of the class DataSet from the configuration
    data_set: DataSet = \
        from_config_dict(data_set_config, DataSet.get_impls())
    descriptor_elem_factory = DescriptorElementFactory \
        .from_config(descriptor_elem_factory_config)

#    print("\n Descriptor_elem_factory: ", descriptor_elem_factory)
#    factory_atts = vars(descriptor_elem_factory)
#    print("\n Descriptor_elem_factory attributes: ", factory_atts)

    # Generate a descriptor set from the config file
    descriptor_set: DescriptorSet = \
        from_config_dict(descriptor_set_config, DescriptorSet.get_impls())

#    print("\n Descriptor Set: ", descriptor_set)



#  This is where it needs caffe dependency to generate descriptors, need to
#  short-circuit this process

#    descriptor_generator: DescriptorGenerator = \
#        from_config_dict(descriptor_generator_config,
#                         DescriptorGenerator.get_impls())

    nn_index: NearestNeighborsIndex = \
       from_config_dict(nn_index_config,
                         NearestNeighborsIndex.get_impls())


#    print("what does a parser look like?", cli_parser())
#    print("parser datatype", type(cli_parser()))
#    print("what does nnindex_config look like?", nn_index_config)

#    print("Instance of DataSet", DataSet)

    # Load JSON data from the file
    with open(manifest_path, "r") as json_file:
        data = json.load(json_file)

    # Access the list of image-descriptor pairs
    image_descriptor_pairs = data['Image_Descriptor_Pairs']


    # Iterate over each pair in manifest json file
    for pair in image_descriptor_pairs:

        # Extract image path and descriptor path
        image_path = pair['image_path']
        image_path = osp.expanduser(image_path)

        desc_path = pair['desc_path']
        desc_path = osp.expanduser(desc_path)
#        print("\n Descriptor Path", desc_path)
        image_path = osp.expanduser(image_path)
        if osp.isfile(image_path):
            data_fe = DataFileElement(image_path, readonly=True)
#            print("\n uuid of data file element:", data_fe.uuid())
            data_set.add_data(data_fe)
#            print("\n is datashet growing?",data_set.__len__())
#            vector = np.load(desc_path)
            descriptor = descriptor_elem_factory.new_descriptor(data_fe.uuid())
#            descriptor.set_vector(vector)
            descriptor_set.add_descriptor(descriptor)

    print("\n what's the length of the dataset?",data_set.__len__())
    print("\n Descriptor Set after adding new descriptor:", descriptor_set)


'''
    uuid_set = data_set.uuids()
    print("\n List of uuids in the dataset:", uuid_set)
    print("\n And the type is:", type(uuid_set))

    new_vector = np.array([1, 2, 3, 4, 5])

    new_descriptor = descriptor_elem_factory.new_descriptor('38b6b4cbdf0bfaf3613de51b67fe58748b9465c9')
    new_descriptor.set_vector(new_vector)
    # print("\n Has vector? ", new_descriptor.has_vector())

    print("\n New descriptor:", new_descriptor)

    atts_new_descriptor = vars(new_descriptor)
    print("\n New descriptor attributes:", atts_new_descriptor)

    # Add the descriptor to the descriptor set
    descriptor_set.add_descriptor(new_descriptor)
    print("\n Descriptor Set after adding new descriptor:", descriptor_set)

    check_descriptor = descriptor_set.get_descriptor('38b6b4cbdf0bfaf3613de51b67fe58748b9465c9')
    print("\n Check descriptor:", check_descriptor)

    print(check_descriptor.vector())

'''

if __name__ == "__main__":
    main()
