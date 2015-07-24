# -*- coding: utf-8 -*-
class BaseConnection(object):
    def fetch(self, *args, **kwargs):
        raise ValueError("You need to define a fetch method on your runner.")


class MockJSONConnection(BaseConnection):
    def __init__(self, settings, cmd=None):
        pass
        #self.file = settings['']

    def fetch(self, *args, **kwargs):
        return {'error': 'This was an error on the server side :('}

class JSONConnection(BaseConnection):
    def __init__(self, settings, cmd=None):
        self.url = settings['URL']
        self.key = settings['KEY']
        self.code = settings['CODE']
        self.cmd = cmd

    def fetch(self, **kwargs):
        if self.cmd:
            self.cmd.stdout.write("  Connecting to %s" % self.url)

        values = {'key': self.key,
                  'code': self.code}
        values.update(kwargs)

        data = urllib.urlencode(values)

        request = urllib2.Request(self.url, data)
        opener = urllib2.build_opener()
        f = opener.open(request)
        hash_table = json.load(f)
        return hash_table
