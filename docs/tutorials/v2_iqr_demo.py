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
    print("Main function is called")
    # Parse command-line arguments
    # args = config

    # print("\n What does a parser look like?", "\n")

    # Extract the paths of the image files
    image_paths = args.input_files


    # Extract the value of the descriptors argument from the cli input
    descriptors_path = args.descriptors

    # Print the contents of the descriptors JSON file
    if descriptors_path:
        print("Descriptors path:", descriptors_path[0])
    else:
        print("Descriptors argument not provided.")

    ## setting up config values:
    # args = cli_parser().parse_args()

    ui_config_filepath, iqr_config_filepath = args.config
    llevel = logging.DEBUG if args.verbose else logging.INFO
    tab = args.tab

    # These are the input files, images that will be processed
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

    print("\n ui_config_filepath:", ui_config_filepath)
    print("\n iqr_config_filepath:", iqr_config_filepath)
    print("\n what is tab? ", tab)
    print("\n What is ui_config look like?", ui_config)



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

    print("\n Descriptor Element Config:", descriptor_elem_factory_config)

    # Configure DescriptorGenerator algorithm implementation, parameters and
    # persistent model component locations (if implementation has any).
    descriptor_generator_config = iqr_plugins_config['descriptor_generator']

    print("\n Descriptor Generator Config:", descriptor_generator_config)

    # Configure NearestNeighborIndex algorithm implementation, parameters and
    # persistent model component locations (if implementation has any).
    nn_index_config = iqr_plugins_config['neighbor_index']


    #--------------------------------------------------------------
    # Remove any existing cache in config data_set file path
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

    print("\n Descriptor_elem_factory: ", descriptor_elem_factory)
    factory_atts = vars(descriptor_elem_factory)
    print("\n Descriptor_elem_factory attributes: ", factory_atts)


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


    #----------------------------------------------------------------
    # Build models
    # log that files are being added to dataset
    log.info("Adding files to dataset '{}'".format(data_set))

    # Add the files to the dataset
    for g in input_files_globs:
        g = osp.expanduser(g)
        if osp.isfile(g):
            data_file_element = DataFileElement(g, readonly=True)

            # Directly access attributes
            # print("\n Filepath:", data_file_element._filepath)
            # print("Readonly:", data_file_element._readonly)
            # print("Explicit Mimetype:", data_file_element._explicit_mimetype, "\n")

            data_set.add_data(data_file_element)
        else:
            log.debug("Expanding glob: %s" % g)
            for fp in glob.iglob(g):
                data_set.add_data(DataFileElement(fp, readonly=True))

    print("\n what's the data_set look like?",data_set)
    print("\n what's the length of the dataset?",data_set.__len__())

    attributes = vars(data_set)
    # print("\n what are the attributes of data_set?", attributes)

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


if __name__ == "__main__":
    main()
