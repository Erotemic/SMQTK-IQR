# notes on file locations that use flask $ grep -r Flask .
./SMQTK-Indexing/.gitignore:# Flask stuff:
./SMQTK-Dataprovider/.gitignore:# Flask stuff:
./SMQTK-Descriptors/.gitignore:# Flask stuff:
./SMQTK-Classifier/.gitignore:# Flask stuff:
./SMQTK-Core/.gitignore:# Flask stuff:
./SMQTK-Image-IO/.gitignore:# Flask stuff:
./SMQTK-Relevancy/.gitignore:# Flask stuff:
./SMQTK-Detection/.gitignore:# Flask stuff:
./SMQTK-IQR/smqtk_iqr/pyproject.toml:Flask = "^2.0.1"
./SMQTK-IQR/smqtk_iqr/pyproject.toml:Flask-Cors = "^3.0.10"
./SMQTK-IQR/smqtk_iqr/pyproject.toml:Flask-BasicAuth = "^0.2.0"
./SMQTK-IQR/smqtk_iqr/.gitignore:# Flask stuff:
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/iqr_service/iqr_server.py:        Setup Flask URL rules.
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/__init__.py:class SmqtkWebApp (flask.Flask, Plugfigurable):
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/file_upload/FileUploadMod.py:    Flask blueprint for file uploading.
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/file_upload/FileUploadMod.py:        :param parent_app: Parent Flask app
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/login/LoginMod.py:        self, name: str, parent_app: flask.Flask,
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/iqr/iqr_search.py:class IqrSearch (flask.Flask, Configurable):
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__init__.py:        # -> This allows session modification during Flask methods called from
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__init__.py:        #    AJAX routines (default Flask sessions do not)
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__init__.py:        # -> Note that 'type: ignore' is used because the parent class Flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__init__.py:    def _apply_csrf_protect(app: flask.Flask) -> flask.Flask:
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/web.py:    :return: Flask response and HTTP status code pair.
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/mongo_sessions.py:    def open_session(self, app: flask.Flask, request: Request) -> MongoSession:


# notes on file locations that use flask $ grep -r flask .
./SMQTK-Indexing/docs/examples/nnss_incremental_update/2d.config.nnss_app.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/.mypy.ini:[mypy-flask_cors.*]
./SMQTK-IQR/smqtk_iqr/.mypy.ini:[mypy-flask_basicauth.*]
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/iqr_service/iqr_server.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/iqr_service/iqr_server.py:) -> flask.Response:
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/iqr_service/iqr_server.py:    return flask.jsonify(**r)

./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/__init__.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/__init__.py:class SmqtkWebApp (flask.Flask, Plugfigurable):
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/__init__.py:            "flask_app": {
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/classifier_service/classifier_server.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/classifier_service/classifier_server.py:    def is_ready(self) -> Tuple[flask.Response, int]:
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/file_upload/FileUploadMod.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/file_upload/FileUploadMod.py:class FileUploadMod (flask.Blueprint):
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/file_upload/FileUploadMod.py:            form = flask.request.form
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/static_host.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/static_host.py:class StaticDirectoryHost (flask.Blueprint):
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/login/LoginMod.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/login/LoginMod.py:class LoginMod (flask.Blueprint):
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/login/LoginMod.py:        self, name: str, parent_app: flask.Flask,
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/iqr/iqr_search.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/iqr/iqr_search.py:class IqrSearch (flask.Flask, Configurable):
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/modules/iqr/iqr_search.py:        :param parent_app: Parent containing flask app instance
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__init__.py:Top level flask application
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__init__.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__init__.py:from flask_cors import cross_origin
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__init__.py:            # LOG.info("Session: %s", flask.session.items())
Binary file ./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__pycache__/__init__.cpython-38.pyc matches
Binary file ./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/__pycache__/__init__.cpython-311.pyc matches
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/sample_configs/config.IqrRestService.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/sample_configs/runApp.IqrSearchDispatcher.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/sample_configs/config.IqrSearchApp.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/web/search_app/sample_configs/runApp.IqrService.json:    "flask_app": {
Binary file ./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/__pycache__/runApplication.cpython-311.pyc matches
Binary file ./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/__pycache__/web.cpython-311.pyc matches
Binary file ./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/__pycache__/mongo_sessions.cpython-311.pyc matches
Binary file ./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/__pycache__/mongo_sessions.cpython-38.pyc matches
Binary file ./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/__pycache__/web.cpython-38.pyc matches
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/runApplication.py:from flask_basicauth import BasicAuth
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/runApplication.py:from flask_cors import CORS
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/runApplication.py:                                   "flask-cors: https://flask-cors.readthedocs"
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/runApplication.py:                             help='Turn on flask app logger namespace '
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/runApplication.py:                                  'effectively enabled if the flask app is '
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/web.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/web.py:) -> Tuple[flask.Response, int]:
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/web.py:    Basic message constructor for returning JSON from a flask routing function
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/web.py:    return flask.jsonify(**r), return_code
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/mongo_sessions.py:Taken from: http://flask.pocoo.org/snippets/110/
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/mongo_sessions.py:import flask
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/mongo_sessions.py:from flask.sessions import SessionInterface, SessionMixin
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/mongo_sessions.py:from flask.wrappers import Request, Response
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/mongo_sessions.py:    def open_session(self, app: flask.Flask, request: Request) -> MongoSession:
./SMQTK-IQR/smqtk_iqr/smqtk_iqr/utils/mongo_sessions.py:        self, app: flask.Flask, session: SessionMixin, response: Response
./SMQTK-IQR/smqtk_iqr/docker/smqtk_classifier_service/default_server.gpu.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/docker/smqtk_classifier_service/default_server.cpu.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/docker/smqtk_iqr_playground/default_confs/cpu/runApp.IqrService.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/docker/smqtk_iqr_playground/default_confs/gpu/runApp.IqrService.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/docker/smqtk_iqr_playground/default_confs/runApp.IqrSearchDispatcher.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/tests/web/iqr_service/test_iqr_service.py:        Make an instance of the IqrService flask application with stub
./SMQTK-IQR/smqtk_iqr/tests/web/classifier_service/test_classifier_server.py:        self.config['flask_app'] = {}
./SMQTK-IQR/smqtk_iqr/tests/web/classifier_service/test_classifier_server.py:            #: :type: flask.wrappers.Response
./SMQTK-IQR/smqtk_iqr/poetry.lock:name = "flask"
./SMQTK-IQR/smqtk_iqr/poetry.lock:name = "flask-basicauth"
./SMQTK-IQR/smqtk_iqr/poetry.lock:name = "flask-cors"
./SMQTK-IQR/smqtk_iqr/poetry.lock:flask = [
./SMQTK-IQR/smqtk_iqr/poetry.lock:flask-basicauth = [
./SMQTK-IQR/smqtk_iqr/poetry.lock:flask-cors = [
./SMQTK-IQR/smqtk_iqr/docs/webservices/iqrdemonstration.rst:Present in both configuration files are the ``flask_app`` and ``server`` sections which control Flask web server application parameters.
./SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrRestService.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrRestService_faiss.json:  "flask_app": {
./SMQTK-IQR/smqtk_iqr/docs/tutorials/docker_runApp.IqrSearchDispatcher.json:  "flask_app": {
./SMQTK-IQR/smqtk_iqr/docs/tutorials/runApp.IqrSearchApp.json:    "flask_app": {
./SMQTK-IQR/smqtk_iqr/docs/tutorials/docker_runApp.IqrRestService.json:  "flask_app": {


# Notes about the web application code
# Base class for SMQTK web applications
smqtk_iqr/smqtk_iqr/web/__init__.py: SmqtkWebApp application base class, inherits from flask.Flask

smqtk_iqr/smqtk_iqr/web/search_app/__init__.py: Top level IqrSearchApp, inherits from SmqtkWebApp
# Bais routing happens lines 133-167

smqtk_iqr/smqtk_iqr/web/iqr_service/iqr_server.py: Top level IqrServiceApp, inherits from SmqtkWebApp

# invoked by calling hte main function in:

# How IQR is setup
# The command runApplication: runs the main() function in smqt_iqr/smqtk_iqr/utils/runApplication.py
# This parsers the cli inputs gathering the web app arg and configuration
# The line "app: smqtk_iqr.web.SmqtkWebApp = app_class.from_config(config)"
# creates an instance of the service app, in this case IqrServiceApp, and will perform the __init__ methods.
# The superclasses __init__ method is called, which is the SmqtWeb __init__ method, which in turn
# calls the Flask __init__ method.

# The runApplication function then calls the run method on the app instance, which is the Flask run method
# Flask starts a development server, which listens for incoming HTTP requests
# and routes them to the appropriate view functions within your application.
