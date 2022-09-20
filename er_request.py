import requests
import json
from conf import conf

def get_request(path: str):
    req = requests.get(conf['endpoint'] + path, headers=conf['header'])
    return json.loads(req.text)