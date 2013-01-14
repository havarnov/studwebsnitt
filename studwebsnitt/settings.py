import os

# set the app secret from environ. var. from heroku:config
# set it to None if "APP_SECRET" var is not defined
SECRET = os.environ.get("APP_SECRET", None)

# import local settings. E.g. app secret, etc...
dir = os.path.dirname(__file__)
if os.path.exists(os.path.join(dir, "local_settings.py")):
	from local_settings import *
