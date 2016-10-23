import json
import os

import requests

from updater import DomainRecordUpdater

PROXY_CERT_PATH = None
# PROXY_CERT_PATH = os.path.expanduser('~/charles-ssl-proxying-certificate.pem')


#####
def get_ip_address(cert=None):
    resp = requests.get("https://api.ipify.org/?format=text", verify=cert)
    if resp.status_code != 200:
        raise EnvironmentError('GET / {}'.format(resp.status_code))
    return resp.text


#####
config = None
with open('config.json') as configFile:
    config = json.load(configFile)
if config is None:
    exit(-1)
ip_address = get_ip_address(PROXY_CERT_PATH)
updater = DomainRecordUpdater(ip_address, config, PROXY_CERT_PATH)
updater.run()
