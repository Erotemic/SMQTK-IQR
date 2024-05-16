# Modifying iqr_app_model_generation for geowatch

# Standard libraries
import argparse
import glob
import logging
import os.path as osp

# SMQTK specific packages
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



def cli_parser() -> argparse.ArgumentParser:
    # Forgoing the ``cli.basic_cli_parser`` due to our use of dual
    # configuration files for this utility.
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-v', '--verbose',
                        default=False, action='store_true',
                        help='Output additional debug logging.')
    parser.add_argument('-c', '--config',
                        metavar="PATH", nargs=2, required=True,
                        help='Path to the JSON configuration files. The first '
                             'file provided should be the configuration file '
                             'for the ``IqrSearchDispatcher`` web-application '
                             'and the second should be the configuration file '
                             'for the ``IqrService`` web-application.')

    parser.add_argument('-d', '--descriptors',
                        metavar="PATH", nargs=1, required=False,
                        help='Path to the JSON descriptor metadata files.'
                             'TO DO...describe file format... ')

    parser.add_argument("-t", "--tab",
                        default=None, required=True,
                        help="The configuration \"tab\" of the "
                             "``IqrSearchDispatcher`` configuration to use. "
                             "This informs what dataset to add the input data "
                             "files to.")
    parser.add_argument("input_files",
                        metavar='GLOB', nargs="+",
                        help="Shell glob to files to add to the configured "
                             "data set.")

    return parser


def main() -> None:
    print("Main function is called")
    # Parse command-line arguments
    parser = cli_parser()
    args = parser.parse_args()

    print("\n What does a parser look like?", parser, "\n")

    # Extract the paths of the image files
    image_paths = args.input_files


    # Extract the value of the descriptors argument
    descriptors_path = args.descriptors

    # Print the contents of the descriptors JSON file
    if descriptors_path:
        print("Descriptors path:", descriptors_path[0])
    else:
        print("Descriptors argument not provided.")

    ## setting up config values:
    args = cli_parser().parse_args()

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

    print("ui_config_filepath:", ui_config_filepath)
    print("what is tab? ", tab)

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

    # Configure DescriptorGenerator algorithm implementation, parameters and
    # persistent model component locations (if implementation has any).
    descriptor_generator_config = iqr_plugins_config['descriptor_generator']

    # Configure NearestNeighborIndex algorithm implementation, parameters and
    # persistent model component locations (if implementation has any).
    nn_index_config = iqr_plugins_config['neighbor_index']

    #
    # Initialize data/algorithms
    #
    # Constructing appropriate data structures and algorithms, needed for the
    # IQR demo application, in preparation for model training.
    #

    log.info("Instantiating plugins")

    # Creates instance of the class DataSet from the configuration
    data_set2: DataSet = \
        from_config_dict(data_set_config, DataSet.get_impls())
    descriptor_elem_factory = DescriptorElementFactory \
        .from_config(descriptor_elem_factory_config)

#  This is where it need caffe to generate descriptors, need to
# short-circuit this process

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
    log.info("Adding files to dataset '{}'".format(data_set2))

    # Add the files to the dataset
    for g in input_files_globs:
        g = osp.expanduser(g)
        if osp.isfile(g):
            data_file_element = DataFileElement(g, readonly=True)

            # Directly access attributes
    #        print("\n Filepath:", data_file_element._filepath)
    #        print("Readonly:", data_file_element._readonly)
    #        print("Explicit Mimetype:", data_file_element._explicit_mimetype, "\n")

            data_set2.add_data(data_file_element)
        else:
            log.debug("Expanding glob: %s" % g)
            for fp in glob.iglob(g):
                data_set2.add_data(DataFileElement(fp, readonly=True))

    print("\n what's the data_set look like?",type(data_set2))
    attributes = vars(data_set2)
    print("\n what are the attributes of data_set?", attributes)


if __name__ == "__main__":
    main()
