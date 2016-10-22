from dnsimple import Dnsimple


class DomainRecordUpdater(object):

    #####
    def __init__(self, ip_address, pwnt_config):
        self.dnsimple = Dnsimple(pwnt_config['api']['api_key'], pwnt_config['api']['user_id'])
        self.domain_configs = pwnt_config['domains']
        self.ip_address = ip_address

    #####
    def run(self):
        for domain, typed_records in self.domain_configs.iteritems():
            domain_is_ready = self.verify_domain(domain)
            if domain_is_ready:
                self.review_zone_records(domain, typed_records)
            else:
                print('Domain {} is not ready!'.format(domain))

    #####
    def create_zone_record(self, zone_name, record_type, record_info):
        ttl = None
        if 'ttl' in record_info:
            ttl = record_info['ttl']
        priority = None
        if 'priority' in record_info:
            priority = record_info['priority']
        resp = self.dnsimple.create_zone_record(zone_name, name=record_info['name'], type=record_type,
                                                content=record_info['content'], ttl=ttl, priority=priority)
        return resp.status_code == 201

    #####
    def update_zone_record(self, zone_name, zone_record_id):
        resp = self.dnsimple.update_zone_record(zone_name, zone_record_id, content=self.ip_address)
        return resp.status_code == 200

    #####
    def create_domain(self, domain_name):
        print('Creating domain record for zone {}.'.format(domain_name))
        resp = self.dnsimple.create_domain(domain_name)
        return resp.status_code == 201

    #####
    def verify_domain(self, domain_name):
        print('Checking if zone {} exists.'.format(domain_name))
        resp = self.dnsimple.get_domain(domain_name)
        return resp.status_code == 200 or self.create_domain(domain_name)

    #####
    def get_records_for_zone(self, zone_name):
        record_map = {}
        resp = self.dnsimple.get_zone_records(zone_name)
        if resp.status_code == 200:
            for record in resp.body['data']:
                if record['type'] not in record_map:
                    record_map[record['type']] = {}
                record_map[record['type']][record['name']] = record
        return record_map

    #####
    def review_zone_records(self, zone_name, typed_record):
        remote_record_map = self.get_records_for_zone(zone_name)
        print('Reviewing zone records for {}.'.format(zone_name))
        for type, zone_records in typed_record.iteritems():
            print('Reviewing records for type {}.'.format(type))
            remote_records = {}
            if type in remote_record_map:
                remote_records = remote_record_map[type]
            for zoneRecord in zone_records:
                if zoneRecord['name'] in remote_records:
                    remote_record = remote_records[zoneRecord['name']]
                    if remote_record['content'] != self.ip_address:
                        print('Updating record for "{}".'.format(zoneRecord['name']))
                        result = self.update_zone_record(zone_name, remote_record['id'])
                        print(' Success > {}.'.format(result))
                    else:
                        print('"{}" is already up to date!'.format(zoneRecord['name']))
                    pass
                else:
                    print('Creating record for "{}".'.format(zoneRecord['name']))
                    result = self.create_zone_record(type, zoneRecord)
                    print(' Success > {}.'.format(result))
                    pass
