#Script to chip images and create associated 'dummy' descriptors.

# Standard libraries
import matplotlib.pyplot as plt
import numpy as np
import os
import json

# Kitware specific librareis
import kwcoco
import kwarray
import kwimage
import kwplot
import ubelt as ub
import xdev

# Define the file paths to be same as bash script that generates data
DATA_FPATH = ub.Path("../../demodata/vidshapes_rgb_data/data.kwcoco.json")
DEMODATA_OUTPUT_PATH= ub.Path("../../demodata").absolute().resolve()
CHIPPED_IMAGES_DPATH = DEMODATA_OUTPUT_PATH / "chipped"
OUTPUT_FPATH=DEMODATA_OUTPUT_PATH / "manifest.json"

CHIPPED_IMAGES_DPATH.ensuredir()

# Define the dimensions of the window slider for image chips
window_size=256
frames=10
num_videos=1

# Create kwcoco Dataset
dset = kwcoco.CocoDataset.demo("vidshapes",
    num_frames=frames, num_videos=num_videos, background="amazon")

rows=[]

#TODO:  determine how to read off the number of images in a kwcoco dataset
for ii in range(dset.n_images):

    # Select image for slicing/chipping
    image_id = dset.images()[ii]

    # generate a coco_image class object from the data set using image id
    coco_image = dset.coco_image(image_id)

    input_image_path = coco_image.primary_image_filepath()

    # To display this image using kwplot bash shell command
    # result = ub.cmd(f'kwplot imshow {input_image_path}', verbose=3, shell=True)

    # Display current image using matplotlib
    # plt.imshow(plt.imread(input_image_path))
    # plt.show()

    # This method converts the image to a  <class 'numpy.ndarray'>
    # The default image is 600x600 pixels with three channels, rgb
    input_image = coco_image.imdelay('r|g|b').finalize()

    annotations = coco_image.annots()

    # Capture location and category ids for annotations in image
    annot_boxes = kwimage.Boxes(annotations.lookup('bbox'), 'xywh')
    annot_cat_ids = np.array(annotations.lookup('category_id'))

    shape = input_image.shape[0:2] # captures the first 2 dimensions, not the channels
    print("shape variable is: ", shape)

    # set the window for the slider
    window = (window_size, window_size)

    # set the slider args base upon image shape and window size.
    slider = kwarray.SlidingWindow(shape, window, allow_overshoot=True)

    # TODO: this needs to have a consistent ordering if the descriptors
    # are used with other toy datasets
    # Categories are the names for annotated objects
    categories = dset.object_categories()

    descriptor_dims = len(categories) * 2

    # index hooks in slider parameters and defines the slicing window

    for index in ub.ProgIter(slider, desc='sliding a window', verbose=3):

        # Slice out the relevant part of the image using the slider function
        # The index performs the slicer operation on the
        # first two dimensions (size of the image)
        part_image = input_image[index]

        # For debugging, view each window of the image
        # plt.imshow(part_image)
        # plt.show()

        # Get a box corresponding to the slice (so we can use its helper methods)
        # Box captures an area of the original image
        # defined by (x1, y1, x2, y2)
        box = kwimage.Box.from_slice(index)

        # Returns a non-zero number for each annotation that overlaps this sliding
        # window. This is not an efficient check, but it will work for now.

        # Intersection area of annotation boxes with current window
        # divided by the union of these areas.
        annot_overlaps = annot_boxes.ious(box.boxes)[:, 0]
        overlapping_cat_ids = annot_cat_ids[annot_overlaps > 0]

        # Look up name of category ids and indexes.
        overlapping_cat_names = dset.categories(overlapping_cat_ids).lookup('name')
        overlapping_cat_idxs = np.array([categories.node_to_idx[name] for name in overlapping_cat_names], dtype=int)

        # print("Overlapping category indices: ", overlapping_cat_idxs, type(overlapping_cat_idxs), '\n')

        # Make a random descriptor, but add an indicator based on the visible
        # annotation categories.

        # Creates an array with 6 values (2 times the number of categories)
        part_descriptor = np.random.rand(descriptor_dims)

        # Assigns descriptor values to 100 where the category index is present
        part_descriptor[overlapping_cat_idxs] = 100

        # print("Part descriptor: ", part_descriptor)

        # converts from (x1,y1), (x2, y2) dimensions to xywh
        x, y, w, h = box.to_xywh().data

        # print("output of box.to_xywh: ", box, "(", x, y, w, h, ")", '\n')

        suffix = f'img_{image_id:05d}-xywh={x:04d}_{y:04d}_{w:03d}_{h:03d}.png'

        # print("suffix is: ", suffix, '\n')

        slice_path = CHIPPED_IMAGES_DPATH / suffix
        # print(f'slice_path={slice_path}\n')

        slice_desc_path = slice_path.augment(stemsuffix="_desc", ext=".json")

        # xdev.embed()

        kwimage.imwrite(slice_path, part_image)

        # Convert the NumPy array to a Python list
        part_descriptor_list = part_descriptor.tolist()

        # Save the list to the JSON file
        with open(slice_desc_path, 'w') as json_file:
            json.dump(part_descriptor_list, json_file)

        row={"image_path":os.fspath(slice_path), "desc_path":os.fspath(slice_desc_path)}
        rows.append(row)
tables={"Image_Descriptor_Pairs":rows}
OUTPUT_FPATH.write_text(json.dumps(tables, indent="    "))
