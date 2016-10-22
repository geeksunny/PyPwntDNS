import json
import requests
from updater import DomainRecordUpdater


#####
def get_ip_address():
    resp = requests.get("https://api.ipify.org/?format=text")
    if resp.status_code != 200:
        raise EnvironmentError('GET / {}'.format(resp.status_code))
    return resp.text


#####
config = None
with open('config.json') as configFile:
    config = json.load(configFile)
if config is None:
    exit(-1)
ip_address = get_ip_address()
updater = DomainRecordUpdater(ip_address, config)
updater.run()
