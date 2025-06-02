import logging
from urllib.error import HTTPError

if __name__ == '__main__':
    import os, sys
    sys.path.append(os.getcwd())

from models import Result
from api.data import event
from api.requests import post_results

results = Result.from_event(event)

logging.info(f"Uploading {len(results)} results...")

post_results(results)