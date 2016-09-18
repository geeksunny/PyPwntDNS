import requests
from response import ApiResponse

class Dnsimple(object):
    apiKey = ""
    userId = ""
    headers = {
        "Accept":"application/json",
        "content-Type":"application/json"
    }
    #
    def __init__(self, apiKey, userId):
        self.apiKey = apiKey
        self.userId = userId
        self.headers["Authorization"] = 'Bearer {}'.format(apiKey)
    #
    def _url(self, path):
        return 'https://api.dnsimple.com/v2/{}/{}'.format(self.userId, path)
    #
    def _return(self, response):
        return ApiResponse(response.status_code, response.json())
    #
    def _get(self, url):
        resp = requests.get(url, headers=self.headers)
        return self._return(resp)
    #
    def _post(self, url, body):
        resp = requests.post(url, data=body, headers=self.headers)
        return self._return(resp)
    #
    def _patch(self, url, body):
        resp = requests.patch(url, data=body, headers=self.headers)
        return self._return(resp)
    #
    def _delete(self, url):
        resp = requests.delete(url, headers=self.headers)
        return self._return(resp)
    #
    def getDomain(self, domainName):
        return self._get(self._url('domains/{}'.format(domainName)))
    #
    def createDomain(self, domainName):
        body = {"name":domainName}
        return self._post(self._url('domains'), body)
    #
    # def deleteDomain(self, domainName):
    #     return self._delete(self._url('domains/{}'.format(domainName)))
    #
    def getZoneRecords(self, zoneName):
        return self._get(self._url('zones/{}/records'.format(zoneName)))
    #
    def createZoneRecord(self, zoneName, name = None, type = None, content = None, ttl = None, priority = None):
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
        return self._post(self._url('zones/{}/records'.format(zoneName)), body)
    #
    def updateZoneRecord(self, zoneName, recordId, content = None, name = None, ttl = None):
        body = {}
        if content is not None:
            body['content'] = content
        if name is not None:
            body['name'] = name
        if ttl is not None:
            body["ttl"] = ttl
        return self._patch(self._url('zones/{}/records/{}'.format(zoneName, recordId)), body)