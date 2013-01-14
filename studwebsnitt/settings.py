import os

try:
	SECRET = os.environ["APP_SECRET"]
except KeyError:
	SECRET = None

dir = os.path.dirname(__file__)
if os.path.exists(os.path.join(dir, "local_settings.py")):
	from local_settings import *
