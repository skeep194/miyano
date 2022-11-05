import requests
import json
from conf import conf

def get_request(path: str):
    req = requests.get(conf['endpoint'] + path, headers=conf['header']).text
    req = json.loads(req)
    if req['code'] != 200:
        raise Exception(req)
    return req