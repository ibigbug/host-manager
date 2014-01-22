import json

import gevent
from gevent import socket


class HostManager(object):
    '''
    generate hosts for custom domains
    get rid of gfw DNS cache poisoning
    '''

    def __init__(self, config=None):
        if isinstance(config, basestring):
            config = load_config(config)
        self.config = config

    def run(self):
        self._resolve()
        self._write()

    def _resolve(self):
        domains = self.config.domains
        jobs = [gevent.spawn(socket.gethostbyname, domain)
                for domain in domains]
        gevent.joinall(jobs, timeout=2)
        ip_result = [job.value for job in jobs]

        self.ip_result = ip_result

    def _write(self):
        domains = self.config.domains
        ip_result = self.ip_result

        target = open(self.config.output, 'wb')
        buf = ['#<Host-Manager by ibigbug>']
        for i in range(0, len(domains)):
            buf.append('%s %s' % (domains[i], ip_result[i]))
        buf.append('#<Host-Manager end>')
        print('Writing to ./hosts')
        target.write('\n'.join(buf))
        target.close()


def load_config(conf_path=None):
    if not conf_path:
        raise ValueError('No iput file.')
    c = open(conf_path, 'rb')
    config_json = json.loads(c.read())
    c.close()
    return Config.from_json(config_json)


class Config(object):
    @classmethod
    def from_json(self, json_obj):
        for k, v in json_obj.iteritems():
            setattr(self, k, v)
        return self
