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
# Generate image chips from kwcoco images
python chip_images.py

# Generate the SMQTK-IQR data set and descriptor set
python v3_iqr_demo.py \
  -c runApp.IqrSearchApp.json runApp.IqrRestService.json \
  -d /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/manifest.json \
  -t "Geowatch Chipped" /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/demodata/chipped/*.png

 # path to config file to run web -service (if not using shortcut script)
runApplication -a IqrService \
-c /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrRestService_faiss.json
# In second terminal run the IQRsearch dispatcher
runApplication -a IqrSearchDispatcher -c /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrSearchApp.json

#------------------------------------------------------
# Debugging with xdev, place in code to debug
import xdev
xdev.embed()


# --------------------------------------------------------------------------
# Steps to run IQR demo with prepopulated descriptor set
# ---------------------------------------------------------------------------
# 1A Remove previous directories and contents for a clean model build
# /smqtk_iqr/demodata
# /smqtk_iqr/docs/tutorials/models and /workdir

# 1. Generate image chips from kwcoco images
# navigate to smqtk_iqr/docs/tutorials
python chip_images_demo.py

# 2. Generate the SMQTK-IQR data set and descriptor set and faiss nnindex
python v3_iqr_demo.py -v \
  -c runApp.IqrSearchApp.json runApp.IqrRestService_faiss.json \
  -m ../../demodata/manifest.json \
  -t "GEOWATCH_DEMO"

# 3. Run mongodb service if not already started - check that config uses defatult port 27017
sudo systemctl start mongodb
# check the status of the service
mongo --eval "db.getMongo()"
# should have:
# connecting to: mongodb://127.0.0.1:27017


# shortcut to running IQR
COMMAND="runApplication -a IqrService \
-c /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrRestService_faiss.json"
SESSION_ID="SMQTK-IQR-SERVICE"
tmux kill-session -t "$SESSION_ID" || true
tmux new-session -d -s "$SESSION_ID" "bash"
tmux send -t "$SESSION_ID" "$COMMAND" Enter

COMMAND="runApplication -a IqrSearchDispatcher -c /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrSearchApp.json"
SESSION_ID="SMQTK-IQR-SEARCH-DISPATCHER"
tmux kill-session -t "$SESSION_ID" || true
tmux new-session -d -s "$SESSION_ID" "bash"
tmux send -t "$SESSION_ID" "$COMMAND" Enter


# Open the web
python -c "import webbrowser; webbrowser.open('127.0.0.1:5000')"
