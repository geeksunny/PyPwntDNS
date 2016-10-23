import requests

from response import ApiResponse


#####
class Dnsimple(object):

    #####
    def __init__(self, api_key, user_id, cert=None):
        self.apiKey = api_key
        self.userId = user_id
        self.cert = cert
        self.headers = {
            "Accept": "application/json",
            "content-Type": "application/json",
            "Authorization": 'Bearer {}'.format(api_key)
        }

    #####
    def _url(self, path):
        return 'https://api.dnsimple.com/v2/{}/{}'.format(self.userId, path)

    #####
    @staticmethod
    def _return(response):
        return ApiResponse(response.status_code, response.json())

    #####
    def _get(self, url):
        resp = requests.get(url, headers=self.headers, verify=self.cert)
        return self._return(resp)

    #####
    def _post(self, url, body):
        resp = requests.post(url, json=body, headers=self.headers, verify=self.cert)
        return self._return(resp)

    #####
    def _patch(self, url, body):
        resp = requests.patch(url, json=body, headers=self.headers, verify=self.cert)
        return self._return(resp)

    #####
    def _delete(self, url):
        resp = requests.delete(url, headers=self.headers, verify=self.cert)
        return self._return(resp)

    #####
    def get_domain(self, domain_name):
        return self._get(self._url('domains/{}'.format(domain_name)))

    #####
    def create_domain(self, domain_name):
        body = {"name": domain_name}
        return self._post(self._url('domains'), body)

    #####
    # def delete_domain(self, domain_name):
    #     return self._delete(self._url('domains/{}'.format(domain_name)))

    #####
    def get_zone_records(self, zone_name):
        return self._get(self._url('zones/{}/records'.format(zone_name)))

    #####
    def create_zone_record(self, zone_name, name=None, type=None, content=None, ttl=None, priority=None):
        body = {}
        if name is not None:
            body['name'] = name
        if type is not None:
            body['type'] = type
        if content is not None:
            body['content'] = content
        if ttl is not None:
            body["ttl"] = ttl
        if priority is not None:
            body["priority"] = priority
        return self._post(self._url('zones/{}/records'.format(zone_name)), body)

    #####
    def update_zone_record(self, zone_name, record_id, content=None, name=None, ttl=None):
        body = {}
        if content is not None:
            body['content'] = content
        if name is not None:
            body['name'] = name
        if ttl is not None:
            body["ttl"] = ttl
        return self._patch(self._url('zones/{}/records/{}'.format(zone_name, record_id)), body)
