# code to test and understand the script_config package
import ubelt as ug
import scriptconfig as scfg
import argparse


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

parser.add_argument('-v', '--verbose',
                    default=False, action='store_true',
                    help='Output additional debug logging.')
parser.add_argument('-c', '--config1',
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

autogen_text = scfg.DataConfig.port_from_argparse(parser)
print(autogen_text)
