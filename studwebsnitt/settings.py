import os


SECRET = os.environ.get("APP_SECRET", None)

dir = os.path.dirname(__file__)
if os.path.exists(os.path.join(dir, "local_settings.py")):
	from local_settings import *
