# notes on debugging the error to connect to the iqr server
# to check the status of a port use in ipython:

In [1]: import requests
   ...: response = requests.get('127.0.0.1:5000/is_ready')
# or
response = requests.get('http://127.0.0.1:5000')

response = requests.get('http://127.0.0.1:5000/is_ready')
response = requests.get('http://127.0.0.1:5001/is_ready')
response.text
response.status_code


# Changed version of Flask and Wergzeug to older versions
flask 2.0.1
werkzeug 2.0.0


# Error occurs in searchapp file with 'pop_path_info'

# check status of iqr service on browser by navigating to:
# localhost:5001/is_ready or other /<add_url> methods


#    Disabled this function because pop_path_info has been removed
#     from werkzeug and there is no clear migration plan.
#    Installed older version of werkzeug (2.0.0) to get this to work.
    """
    def __call__(self, environ: Dict, start_response: Callable) -> Callable:
        try:
            from werkzeug.wsgi import pop_path_info
        except ImportError:
            pop_path_info = None
        path_prefix = get_path_info(environ)
        LOG.debug(f"Base application __call__ path prefix {path_prefix}")
        LOG.debug(f"pop_path_info: {pop_path_info}")
        LOG.debug(f"environ: {environ}")
        LOG.debug(f"start_respnsse: {start_response}")

        if (pop_path_info is not None) and path_prefix and (path_prefix not in self.PREFIX_BLACKLIST):
            app = self.get_application(path_prefix)
            if app is not None:
                pop_path_info(environ)
            else:
                LOG.debug(f"No IQR application registered for prefix: {path_prefix}")
                app = NotFound()  # type: ignore
        else:
            LOG.debug("No prefix or prefix in blacklist. Using dispatcher app.")
            app = self.wsgi_app  # type: ignore

        return app(environ, start_response)  # type: ignore
    """
