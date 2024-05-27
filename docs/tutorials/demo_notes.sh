# --------------------------------------------------------------------------
# IQR demo with PrePopulated Descriptor Set
# ---------------------------------------------------------------------------

"""
May 27, 2024
The following guide provides steps to run the IQR demo with a prepopulated
descriptor set. The demo was written and run with Python version 3.11.2.
Older versions of packages flask 2.0.1 and werkzeug 2.0.0 were used.
The demo uses two werkzeug method 'pop_path_info' and 'peek_path_info' that
were removed in werkzeug 2.3.0 release that were deprecated in 2.2.0. These
methods are used by the IQR Search Dispatcher that generates the link for
each IQR instance, smqtk/smqtk_iqr/web/search_app/__init__.py.

The build_models_demo.py script is used to generate the descriptor set
without calling the methods in one of the descriptor generator
modules. Using the PrePopulatedDescriptorGenerator class, the descriptor set
is generated from a manifest file that contains the paths to the image files
and the corresponding descriptor files. The manifest file is created by the
chip_images_demo.py script that generates image chips from kwcoco images and
builds dummy descriptor files.
"""

# ---------------------------------------------------------------------------
# Steps to run the IQR demo with a prepopulated descriptor set
# ---------------------------------------------------------------------------

# A. If not merged, git pull the PR branch 'dev/PrepopulatedDescriptorSet'
# from the SMQTK-Descriptors repository.  Config files use the
# 'PrePopulatedDescriptorGenerator' class.

# B. (Optional) Remove previous directories and contents for a clean model build
# /smqtk_iqr/demodata
# /smqtk_iqr/docs/tutorials/models and /workdir

# 1. Generate image chips from kwcoco image generator
# navigate to smqtk_iqr/docs/tutorials then run:
python chip_images_demo.py

# 2. Generate the SMQTK-IQR data set, descriptor set and faiss nnindex
python build_models_demo.py -v \
  -c runApp.IqrSearchApp.json runApp.IqrRestService.json \
  -m ../../demodata/manifest.json \
  -t "GEOWATCH_DEMO"

# 3. Run mongodb service if not already started - config is set to use default
# host and port ://127.0.0.1:27017
sudo systemctl start mongodb

# 4. check the status of the service
mongo --eval "db.getMongo()"
# Should have message:
# connecting to: mongodb://127.0.0.1:27017
# 'smqtk' database will be created when the IQR service is run the first time.
# Enter a mongo shell, to view available databases:
mongo
show dbs

# 5. Run the IQR search dispatcher and IQR service.
# This script does not need to be run in the tutorials directory; however,
# the config file paths need to be provided.

# Following script provides commands to run in two tmux sessions
COMMAND="runApplication -a IqrService \
-c /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrRestService.json"
SESSION_ID="SMQTK-IQR-SERVICE"
tmux kill-session -t "$SESSION_ID" || true
tmux new-session -d -s "$SESSION_ID" "bash"
tmux send -t "$SESSION_ID" "$COMMAND" Enter

COMMAND="runApplication -a IqrSearchDispatcher \
-c /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrSearchApp.json"
SESSION_ID="SMQTK-IQR-SEARCH-DISPATCHER"
tmux kill-session -t "$SESSION_ID" || true
tmux new-session -d -s "$SESSION_ID" "bash"
tmux send -t "$SESSION_ID" "$COMMAND" Enter

# 6. Open a web-browser and navigate to 'localhost:5000'
python -c "import webbrowser; webbrowser.open('127.0.0.1:5000')"

# 7. In the web-browser, select 'GEOWATCH_DEMO' IQR instance

# 8. Both username and password are set to 'demo' by config files

# Appendix:  If you want to perform step 5 in separate terminals, run:
runApplication -a IqrService \
-c /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrRestService.json

# In second terminal run the IQRsearch dispatcher
runApplication -a IqrSearchDispatcher
-c /home/local/KHQ/paul.beasly/code/SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrSearchApp.json
