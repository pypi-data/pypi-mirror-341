import os
import sys
from datetime import datetime, timedelta
from pprint import pprint

from dotenv import load_dotenv

# Load env vars from a .env file
load_dotenv()

sys.path.insert(0, "")

from nacwrap import nacwrap

res = nacwrap.get_datasource_connectors()

pprint(res)

pass
