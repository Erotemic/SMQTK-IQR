#  script to debug the prepolulated descriptor generator plugin

try:
    from smqtk_descriptors.impls.descriptor_generator.prepopulated import PrePopulatedDescriptorGenerator
    print("PrePopulatedDescriptorGenerator is available.")
except ImportError as e:
    print("PrePopulatedDescriptorGenerator is not available.")
    print(e)

from smqtk_descriptors import DescriptorGenerator

# List all available implementations
available_impls = DescriptorGenerator.get_impls()
print("Available DescriptorGenerator implementations:")
for impl in available_impls:
    print(impl)


import logging
from smqtk_core.configuration import from_config_dict
from smqtk_descriptors import DescriptorGenerator

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Example configuration dictionary for PrePopulatedDescriptorGenerator
descriptor_generator_config = {
    "type": "smqtk_descriptors.impls.descriptor_generator.prepopulated.PrePopulatedDescriptorGenerator",
    # Add other necessary configuration parameters specific to PrePopulatedDescriptorGenerator
}

# Print the configuration
print("Configuration:", descriptor_generator_config)

# Get and print available implementations
available_impls = DescriptorGenerator.get_impls()
print("Available DescriptorGenerator implementations:")
for impl in available_impls:
    print(impl)

# Attempt to initialize the DescriptorGenerator
try:
    descriptor_generator = from_config_dict(descriptor_generator_config, available_impls)
    print("DescriptorGenerator initialized successfully.")
except ValueError as e:
    print("Error initializing DescriptorGenerator:")
    print(e)
