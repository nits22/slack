import os
import logging
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

SLACK_TOKEN=os.environ["SLACK_TOKEN"]
SIGNING_SECRET=os.environ["SIGNING_SECRET"]
logging.basicConfig(level=logging.INFO, format='Method Name --> %(funcName)s  %(asctime)s   %(message)s\n')