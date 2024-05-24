
# Code to run container from image to perform butterfly demo.
docker run -v \
  "/home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies:/home/smqtk/data/mnt_butterflies/" \
  --gpus all \
  -p 5000:5000 \
  --name smqtk \
  -it 1eed980552ae


# code to run container directly from web-service. This now runs with different nvidia driver
docker run --gpus all -p 5000:5000 gitlab.kitware.com:4567/smqtk-public/smqtk-iqr-docker/iqr_playground:latest-cuda9.2-cudnn7-runtime-ubuntu18.04

# command to run the demo with the mounted drive in docker container
iqr_app_model_generation \
    -c config.IqrSearchApp.json config.IqrRestService.json \
    -t "LEEDS Butterflies" /leedsbutterfly_dataset_v1.1/leedsbutterfly/images/*.jpg


# another idea to use existing config files, but point to images in the mounted drive.  Same command but perform in this containter directory
smqtk/data/configs

iqr_app_model_generation \
    -c runApp.IqrSearchDispatcher.json runApp.IqrRestService.json \
    -t "LEEDS Butterflies" /leedsbutterfly_dataset_v1.1/leedsbutterfly/images/*.jpg


# Invocation that should work
kwcoco toydata --key=vidshapes8 --bundle_dpath="$HOME"/tmp/demo_data

docker run \
    --gpus all \
    -p 5000:5000 \
    -v "$HOME"/tmp/demo_data/_assets/images:/images \
    gitlab.kitware.com:4567/smqtk-public/smqtk-iqr-docker/iqr_playground:latest-cuda9.2-cudnn7-runtime-ubuntu18.04 \
    --build

#Try another with different images
docker run \
    --gpus all \
    -p 5000:5000 \
    -v "$HOME"/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/leedsbutterfly_dataset_v1.1/leedsbutterfly/images \
    gitlab.kitware.com:4567/smqtk-public/smqtk-iqr-docker/iqr_playground:latest-cuda9.2-cudnn7-runtime-ubuntu18.04 \
    --build


# Try using the downloaded image

docker run \
    --gpus all \
    -p 5000:5000 \
    -v "$HOME"/tmp/demo_data/_assets/images:/images \
    1eed980552ae


# practicing using the argparser
python v1_iqr_demo.py \
 -c /home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/config.IqrSearchApp.json \
 /home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/config.IqrRestService.json \
 -t /home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/leedsbutterfly_dataset_v1.1/leedsbutterfly/images/*.png

 # practicing using the cli with different configurations. Use in script v1_iqr_demo.py
python v1_iqr_demo.py \
 -c /home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/config.IqrSearchApp.json \
 /home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/config.IqrRestService.json \
 -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
 -t /home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/leedsbutterfly_dataset_v1.1/leedsbutterfly/images/*.png


  # Use config in docker image. Use in script v1_iqr_demo.py
python v1_iqr_demo.py \
 -c ../../data_docker_image/configs/runApp.IqrSearchDispatcher.json \
 ../../data_docker_image/configs/runApp.IqrService.json \
 -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
-t "Ten Butterflies" /home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/10_images/*.png

# Use script_config rather than argparse. --Currently using this one
python v2_iqr_demo.py \
 -c ../../data_docker_image/configs/runApp.IqrSearchDispatcher.json \
 ../../data_docker_image/configs/runApp.IqrService.json \
 -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
 -t "Ten Butterflies" /home/local/KHQ/paul.beasly/wrkspce/leeds_butterflies/leedsbutterfly_dataset_v1.1/leedsbutterfly/images/*.png

 # Use script_config rather than argparse. --Currently using this one with smaller set of images
python v2_iqr_demo.py \
 -c ../../data_docker_image/configs/runApp.IqrSearchDispatcher.json \
 ../../data_docker_image/configs/runApp.IqrService.json \
 -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
 -t "Ten Butterflies" /home/local/KHQ/paul.beasly/data/ten_butterflies/*.png

  # Use file system for descriptor elements.
python v2_iqr_demo.py \
 -c ../../data_docker_image/configs/runApp.IqrSearchDispatcher.json \
 ../../data_docker_image/configs/run.IqrService_file.json \
 -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
 -t "Ten Butterflies" /home/local/KHQ/paul.beasly/data/ten_butterflies/*.png

# command to run the demo with the mounted drive
iqr_app_model_generation \
    -c runApp.IqrSearchApp.json runApp.IqrRestService.json \
    -t "LEEDS Butterflies" /leedsbutterfly_dataset_v1.1/leedsbutterfly/images/*.jpg


  # Use config files with file saving instead of psql
python v2_iqr_demo.py \
 -c runApp.IqrSearchApp.json runApp.IqrRestService_file.json \
 -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
 -t "Ten Butterflies" /home/local/KHQ/paul.beasly/data/ten_butterflies/*.png


  # Try with v1
python v1_iqr_demo.py \
 -c runApp.IqrSearchApp.json runApp.IqrRestService_file.json \
 -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
 -t "Ten Butterflies" /home/local/KHQ/paul.beasly/data/ten_butterflies/*.png


  # Using standard demo code
iqr_app_model_generation \
 -c runApp.IqrSearchApp.json runApp.IqrRestService_file.json \
 -t "Ten Butterflies" /home/local/KHQ/paul.beasly/data/ten_butterflies/*.png

# This is how the classifier users descriptors
    # Load state into an empty IqrSession instance.
    with open(iqr_state_fp, 'rb') as f:
        state_bytes = f.read().strip()
    descr_factory = DescriptorElementFactory(DescriptorMemoryElement, {})
    rank_relevancy = mock.MagicMock(spec=RankRelevancy)
    iqrs = IqrSession(rank_relevancy)
    iqrs.set_state_bytes(state_bytes, descr_factory)

# Code to generate the descriptor list used in iqr_app_model_generation
    # Generate descriptors of data for building NN index.


    descr_list = list(descriptor_generator.generate_elements(
        data_set, descr_factory=descriptor_elem_factory
    ))
