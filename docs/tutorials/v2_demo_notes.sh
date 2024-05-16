# Record of config files and scripts to run

# use config files with file elements and standard demo code
# reaches error due to Caffe not be installed and out-of-date
iqr_app_model_generation \
  -c runApp.IqrSearchApp.json runApp.IqrRestService.json \
  -t "Ten Butterflies" /home/local/KHQ/paul.beasly/data/ten_butterflies/*.png


# use config files with file elements and standard demo code
python v2_iqr_demo.py \
  -c runApp.IqrSearchApp.json runApp.IqrRestService.json \
  -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
  -t "Ten Butterflies" /home/local/KHQ/paul.beasly/data/ten_butterflies/*.png


# Next step use chipped kwcoco images from geowatch as image file inputs
python v2_iqr_demo.py \
  -c runApp.IqrSearchApp.json runApp.IqrRestService.json \
  -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
  -t "Ten Butterflies" /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/chipped/*.png

  # Next version builds dataset and descriptor set using json_manifests
python v3_iqr_demo.py \
  -c runApp.IqrSearchApp.json runApp.IqrRestService.json \
  -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
  -t "Ten Butterflies" /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/chipped/*.png
