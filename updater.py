from dnsimple import Dnsimple

class DomainRecordUpdater(object):
    dnsimple = None
    domainConfigs = None
    ipAddress = None
    #
    def __init__(self, ipAddress, pwntConfig):
        self.dnsimple = Dnsimple(pwntConfig['api']['api_key'], pwntConfig['api']['user_id'])
        self.domainConfigs = pwntConfig['domains']
        self.ipAddress = ipAddress
    #
    def run(self):
        for domain, typedRecords in self.domainConfigs['domains'].iteritems():
            domainIsReady = self.verifyDomain(domain)
            if (domainIsReady):
                self.reviewZoneRecords(domain, typedRecords)
            else:
                print('Domain {} is not ready!'.format(domain))
    #
    def createZoneRecord(self, zoneName, recordType, recordInfo):
        ttl = None
        if 'ttl' in recordInfo:
            ttl = recordInfo['ttl']
        priority = None
        if 'priority' in recordInfo:
            priority = recordInfo['priority']
        resp = self.dnsimple.createZoneRecord(zoneName, name=recordInfo['name'], type=recordType,
                                              content=recordInfo['content'], ttl=ttl, priority=priority)
        return resp.statusCode == 201
    #
    def updateZoneRecord(self, zoneName, zoneRecordId):
        resp = self.dnsimple.updateZoneRecord(zoneName, zoneRecordId, content=self.ipAddress)
        return resp.statusCode == 200
    #
    def createDomain(self, domainName):
        print('Creating domain record for zone {}.'.format(domainName))
        resp = self.dnsimple.createDomain(domainName)
        return resp.statusCode == 201
    #
    def verifyDomain(self, domainName):
        print('Checking if zone {} exists.'.format(domainName))
        resp = self.dnsimple.getDomain(domainName)
        return resp.statusCode == 200 or self.createDomain(domainName)
    #
    def getRecordsForZone(self, zoneName):
        recordMap = {}
        resp = self.dnsimple.getZoneRecords(zoneName)
        if resp.statusCode == 200:
            for record in resp.body['data']:
                if record['type'] not in recordMap:
                   recordMap[record['type']] = {}
                recordMap[record['type']][record['name']] = record
        return recordMap
    #
    def reviewZoneRecords(self, zoneName, typedRecords):
        remoteRecordMap = self.getRecordsForZone(zoneName)
        print('Reviewing zone records for {}.'.format(zoneName))
        for type, zoneRecords in typedRecords.iteritems():
            print('Reviewing records for type {}.'.format(type))
            remoteRecords = {}
            if type in remoteRecordMap:
                remoteRecords = remoteRecordMap[type]
            for zoneRecord in zoneRecords:
                if zoneRecord['name'] in remoteRecords:
                    remoteRecord = remoteRecords[zoneRecord['name']]
                    if remoteRecord['content'] != self.ipAddress:
                        print('Updating record for "{}".'.format(zoneRecord['name']))
                        result = self.updateZoneRecord(zoneName, remoteRecord['id'])
                        print(' Success > {}.'.format(result))
                    else:
                        print('"{}" is already up to date!'.format(zoneRecord['name']))
                    pass
                else:
                    print('Creating record for "{}".'.format(zoneRecord['name']))
                    result = self.createZoneRecord(type, zoneRecord)
                    print(' Success > {}.'.format(result))
                    pass